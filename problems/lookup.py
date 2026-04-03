from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "problems" / "index.json"
DEFAULT_CACHE_PATH = ROOT_DIR / ".cache" / "problem_lookup_cache.json"
WORD_RE = re.compile(r"[a-z0-9]+")


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).lower()
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(" ".join(line.split()) for line in normalized.splitlines()).strip()


def normalize_phrase(text: str) -> str:
    return " ".join(WORD_RE.findall(normalize_text(text)))


def tokenize(text: str) -> set[str]:
    return set(WORD_RE.findall(normalize_text(text)))


def hash_query(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ProblemRecord:
    problem_id: str
    title: str
    path: str
    searchable_text: str
    searchable_phrase: str
    normalized_title: str
    normalized_hints: tuple[str, ...]
    normalized_sample_lines: tuple[str, ...]
    tokens: frozenset[str]
    data: dict[str, Any]


@dataclass(frozen=True)
class LookupResult:
    problem_id: str
    title: str
    path: str
    score: float
    match_type: str
    solution_text: str
    metadata: dict[str, Any]


class ProblemLookup:
    def __init__(
        self,
        index_path: Path = INDEX_PATH,
        cache_path: Path = DEFAULT_CACHE_PATH,
    ) -> None:
        self.index_path = index_path
        self.cache_path = cache_path
        self.records = self._load_records()
        self.records_by_id = {record.problem_id: record for record in self.records}
        self.cache = self._load_cache()

    def _load_records(self) -> list[ProblemRecord]:
        raw_items = json.loads(self.index_path.read_text(encoding="utf-8"))
        records: list[ProblemRecord] = []
        for item in raw_items:
            sections = [
                item.get("title", ""),
                *item.get("tags", []),
                *item.get("match_hints", []),
                *item.get("sample_input_prefix", []),
                item.get("sample_output", ""),
                *item.get("notes", []),
            ]
            searchable_text = "\n".join(section for section in sections if section).strip()
            records.append(
                ProblemRecord(
                    problem_id=item["problem_id"],
                    title=item["title"],
                    path=item["path"],
                    searchable_text=normalize_text(searchable_text),
                    searchable_phrase=normalize_phrase(searchable_text),
                    normalized_title=normalize_phrase(item["title"]),
                    normalized_hints=tuple(
                        normalize_phrase(hint) for hint in item.get("match_hints", []) if hint
                    ),
                    normalized_sample_lines=tuple(
                        normalize_phrase(line)
                        for line in item.get("sample_input_prefix", []) + [item.get("sample_output", "")]
                        if line
                    ),
                    tokens=frozenset(tokenize(searchable_text)),
                    data=item,
                )
            )
        return records

    def _load_cache(self) -> dict[str, Any]:
        if not self.cache_path.exists():
            return {"query_cache": {}}
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"query_cache": {}}

    def _write_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.cache, ensure_ascii=False, indent=2)
        self.cache_path.write_text(payload, encoding="utf-8")

    def lookup(self, query: str) -> LookupResult | None:
        normalized_query = normalize_text(query)
        if not normalized_query:
            return None

        query_key = hash_query(normalized_query)
        cached = self.cache.get("query_cache", {}).get(query_key)
        if cached:
            record = self.records_by_id.get(cached.get("problem_id"))
            if record:
                return self._build_result(
                    record=record,
                    score=1.0,
                    match_type="cached-query",
                    metadata={
                        "cache_hit": True,
                        "cached_at": cached.get("updated_at"),
                    },
                )

        best_record: ProblemRecord | None = None
        best_score = 0.0
        best_match_type = "no-match"
        query_phrase = normalize_phrase(normalized_query)
        query_tokens = tokenize(normalized_query)

        for record in self.records:
            score, match_type = self._score_record(record, query_phrase, query_tokens)
            if score > best_score:
                best_score = score
                best_record = record
                best_match_type = match_type

        if best_record is None or best_score < 0.45:
            return None

        self.cache.setdefault("query_cache", {})[query_key] = {
            "problem_id": best_record.problem_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._write_cache()
        return self._build_result(
            record=best_record,
            score=best_score,
            match_type=best_match_type,
            metadata={"cache_hit": False},
        )

    def _score_record(
        self,
        record: ProblemRecord,
        query_phrase: str,
        query_tokens: set[str],
    ) -> tuple[float, str]:
        if not query_phrase:
            return 0.0, "empty-query"

        if query_phrase == record.normalized_title:
            return 0.99, "exact-title"

        if query_phrase and query_phrase in record.searchable_phrase:
            return 0.95, "exact-body"

        hint_hits = sum(1 for hint in record.normalized_hints if hint and hint in query_phrase)
        sample_hits = sum(1 for line in record.normalized_sample_lines if line and line in query_phrase)
        token_overlap = (
            len(query_tokens & record.tokens) / len(query_tokens)
            if query_tokens
            else 0.0
        )
        title_tokens = tokenize(record.title)
        title_overlap = (
            len(query_tokens & title_tokens) / len(title_tokens)
            if title_tokens
            else 0.0
        )

        score = 0.0
        match_type = "fuzzy"

        if hint_hits:
            score += min(0.54, 0.18 * hint_hits)
            match_type = "hint-match"
        if sample_hits:
            score += min(0.24, 0.12 * sample_hits)
            match_type = "sample-match"

        score += 0.32 * token_overlap
        score += 0.18 * title_overlap

        if token_overlap >= 0.8 and hint_hits:
            score += 0.1
            match_type = "high-confidence-fuzzy"

        return min(score, 0.94), match_type

    def _build_result(
        self,
        record: ProblemRecord,
        score: float,
        match_type: str,
        metadata: dict[str, Any],
    ) -> LookupResult:
        solution_path = ROOT_DIR / record.path
        return LookupResult(
            problem_id=record.problem_id,
            title=record.title,
            path=record.path,
            score=score,
            match_type=match_type,
            solution_text=solution_path.read_text(encoding="utf-8"),
            metadata=metadata,
        )


def _read_query(args: argparse.Namespace) -> str:
    if args.query_file:
        return Path(args.query_file).read_text(encoding="utf-8")
    if args.query:
        return args.query
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Please pass --query, a file path, or pipe the problem statement via stdin.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find a matching archived problem and print its saved Python solution."
    )
    parser.add_argument("query_file", nargs="?", help="Path to a text file that contains the problem statement.")
    parser.add_argument("--query", help="Problem statement passed inline.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a human-friendly summary.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    query = _read_query(args)

    lookup = ProblemLookup()
    result = lookup.lookup(query)
    if result is None:
        print("No matching archived problem found.", file=sys.stderr)
        return 1

    if args.json:
        payload = {
            "problem_id": result.problem_id,
            "title": result.title,
            "path": result.path,
            "score": round(result.score, 3),
            "match_type": result.match_type,
            "cache_hit": result.metadata.get("cache_hit", False),
            "solution": result.solution_text,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"[{result.match_type}] {result.problem_id} {result.title}")
    print(f"score: {result.score:.3f}")
    print(f"solution: {result.path}")
    print()
    print(result.solution_text.rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
