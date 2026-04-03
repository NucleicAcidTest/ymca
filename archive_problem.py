from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from problems.lookup import ProblemLookup, normalize_text


ROOT_DIR = Path(__file__).resolve().parent
INDEX_PATH = ROOT_DIR / "problems" / "index.json"
SECTION_HEADERS = {"question", "input", "output", "constraint", "constraints", "example", "explanation"}
NOISE_PATTERNS = (
    "current selected programming language",
    "current selected programming language is",
    "we emphasize the submission of a fully working code",
    "once submitted",
    "you cannot review this problem again",
    "you can use print",
    "you can use system.out.println",
    "the version of",
    "warning: printing unwanted",
    "output of the compiled code will be displayed here",
    "from 小红书",
)
STOPWORDS = {
    "a",
    "an",
    "the",
    "of",
    "to",
    "for",
    "and",
    "or",
    "in",
    "on",
    "at",
    "by",
    "with",
    "from",
    "into",
    "after",
    "before",
    "then",
    "that",
    "this",
    "these",
    "those",
    "is",
    "are",
    "was",
    "were",
    "be",
    "being",
    "been",
    "it",
    "its",
    "as",
    "if",
    "all",
    "any",
    "each",
    "given",
    "write",
    "algorithm",
    "find",
    "print",
    "determine",
    "list",
    "number",
    "numbers",
}


@dataclass(frozen=True)
class ArchiveResult:
    status: str
    query_text: str
    query_source: str
    title: str | None = None
    problem_id: str | None = None
    slug: str | None = None
    path: str | None = None
    score: float | None = None
    match_type: str | None = None


def resolve_input_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.exists():
        return path.resolve()

    repo_relative = (ROOT_DIR / raw_path).resolve()
    if repo_relative.exists():
        return repo_relative

    return path


def load_ocr_text(image_path: Path) -> str:
    from rapidocr_onnxruntime import RapidOCR

    ocr = RapidOCR()
    ocr_result, _ = ocr(str(image_path))
    text_lines = [item[1] for item in ocr_result] if ocr_result else []
    return "\n".join(text_lines).strip()


def clean_ocr_text(text: str) -> str:
    lines = []
    previous = None
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for raw_line in normalized.splitlines():
        raw_line = " ".join(raw_line.split())
        line = raw_line.strip(" .:-")
        if not line:
            continue
        lowered = line.lower()
        if any(pattern in lowered for pattern in NOISE_PATTERNS):
            continue
        if line == previous:
            continue
        previous = line
        lines.append(line)
    return "\n".join(lines)


def extract_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"body": []}
    current = "body"

    for line in clean_ocr_text(text).splitlines():
        lowered = line.lower().rstrip(":")
        if lowered in SECTION_HEADERS:
            if lowered == "question":
                current = "body"
            elif lowered == "constraint":
                current = "constraints"
            else:
                current = lowered
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return sections


def _sentence_split(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [part.strip(" .") for part in parts if part.strip(" .")]


def infer_title(text: str, fallback_name: str | None = None) -> str:
    sections = extract_sections(text)
    candidate_lines = sections.get("body", []) + sections.get("input", []) + sections.get("output", [])
    candidate_text = " ".join(candidate_lines).lower()

    if ("duplicate" in candidate_text or "distinct number" in candidate_text) and (
        "same order" in candidate_text or "appear in the input list" in candidate_text
    ):
        return "Remove Duplicates Preserve Order"
    if "alternate sort" in candidate_text:
        return "Alternate Sort Of List"
    if "perfect number" in candidate_text:
        return "Perfect Number Check"
    if "connected clusters" in candidate_text or "city clusters" in candidate_text:
        return "Connected City Clusters"

    for line in candidate_lines:
        lowered = line.lower()
        if lowered in SECTION_HEADERS or len(line) < 12:
            continue

        words = re.findall(r"[a-z0-9]+", lowered)
        keywords = [word for word in words if word not in STOPWORDS]
        if keywords:
            return " ".join(word.capitalize() for word in keywords[:5])

    if fallback_name:
        words = re.findall(r"[a-z0-9]+", fallback_name.lower())
        keywords = [word for word in words if word not in STOPWORDS]
        if keywords:
            return " ".join(word.capitalize() for word in keywords[:5])

    return "Untitled Problem"


def slugify(title: str) -> str:
    words = re.findall(r"[a-z0-9]+", title.lower())
    slug = "_".join(words[:8]).strip("_")
    return slug or "untitled_problem"


def collect_match_hints(text: str) -> list[str]:
    hints = []
    for sentence in _sentence_split(clean_ocr_text(text)):
        if len(sentence) < 18:
            continue
        hints.append(sentence)
        if len(hints) == 4:
            break
    return hints


def collect_sample_input_prefix(sections: dict[str, list[str]]) -> list[str]:
    example_lines = sections.get("example", [])
    sample_input = []
    capture = False

    for line in example_lines:
        lowered = line.lower().rstrip(":")
        if lowered == "input":
            capture = True
            continue
        if lowered == "output":
            break
        if capture:
            sample_input.append(line)
            if len(sample_input) == 4:
                break

    if sample_input:
        return sample_input

    input_lines = [line for line in sections.get("input", []) if re.search(r"\d", line)]
    return input_lines[:4]


def collect_sample_output(sections: dict[str, list[str]]) -> str:
    example_lines = sections.get("example", [])
    capture = False
    output_lines = []

    for line in example_lines:
        lowered = line.lower().rstrip(":")
        if lowered == "output":
            capture = True
            continue
        if lowered == "explanation":
            break
        if capture:
            output_lines.append(line)

    if output_lines:
        return " ".join(output_lines[:2])

    output_lines = [line for line in sections.get("output", []) if re.search(r"\d", line)]
    return " ".join(output_lines[:2]) if output_lines else "see statement"


def build_problem_markdown(problem_id: str, title: str, text: str, source_name: str | None) -> str:
    sections = extract_sections(text)
    body_sentences = _sentence_split("\n".join(sections.get("body", [])))
    summary_lines = body_sentences[:3] or ["OCR extracted statement for this problem."]
    match_hints = collect_match_hints(text)
    sample_input_prefix = collect_sample_input_prefix(sections)
    sample_output = collect_sample_output(sections)

    notes = [
        "This draft was generated automatically from OCR text.",
        "Review the statement wording before relying on it for future fuzzy matches.",
    ]
    if source_name:
        notes.append("Source image: `{}`.".format(source_name))

    summary_block = "\n\n".join(summary_lines)
    hints_block = "\n".join(f"- {hint}" for hint in match_hints) or "- OCR hint extraction was empty."
    notes_block = "\n".join(f"- {note}" for note in notes)

    sample_lines = ""
    if sample_input_prefix:
        sample_lines += "## Sample Input Prefix\n\n"
        sample_lines += "\n".join(f"- `{line}`" for line in sample_input_prefix)
        sample_lines += "\n\n"
    if sample_output:
        sample_lines += "## Sample Output\n\n"
        sample_lines += f"`{sample_output}`\n\n"

    return (
        f"# {problem_id.upper()} {title}\n\n"
        "## Summary\n\n"
        f"{summary_block}\n\n"
        "## Matching Hints\n\n"
        f"{hints_block}\n\n"
        f"{sample_lines}"
        "## Notes\n\n"
        f"{notes_block}"
    )


def build_solution_stub(title: str) -> str:
    return (
        "import sys\n\n\n"
        "def main():\n"
        f"    # TODO: implement solution for: {title}\n"
        "    data = sys.stdin.buffer.read().split()\n"
        "    if not data:\n"
        "        return\n"
        "    raise NotImplementedError('Solution draft not implemented yet.')\n\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n"
    )


def next_problem_number(index_items: list[dict[str, object]]) -> int:
    numbers = []
    for item in index_items:
        problem_id = str(item.get("problem_id", ""))
        match = re.fullmatch(r"p(\d+)", problem_id)
        if match:
            numbers.append(int(match.group(1)))
    return (max(numbers) if numbers else 0) + 1


def ensure_unique_slug(slug: str, index_items: list[dict[str, object]]) -> str:
    existing = {str(item.get("slug", "")) for item in index_items}
    if slug not in existing:
        return slug

    suffix = 2
    while f"{slug}_{suffix}" in existing:
        suffix += 1
    return f"{slug}_{suffix}"


def build_index_entry(
    problem_id: str,
    slug: str,
    title: str,
    text: str,
    source_name: str | None,
) -> dict[str, object]:
    sections = extract_sections(text)
    entry = {
        "problem_id": problem_id,
        "slug": slug,
        "title": title,
        "status": "draft",
        "tags": ["ocr", "draft"],
        "match_hints": collect_match_hints(text),
        "sample_input_prefix": collect_sample_input_prefix(sections),
        "sample_output": collect_sample_output(sections),
        "notes": [
            "Auto-generated OCR archive.",
            "Review title, hints, and examples before treating this as canonical.",
        ],
        "path": f"problems/{problem_id}_{slug}/solution.py",
    }
    if source_name:
        entry["notes"].append(f"Source image: {source_name}.")
    return entry


def read_query(args: argparse.Namespace) -> tuple[str, str]:
    if args.query:
        return args.query, "inline-query"
    if args.query_file:
        path = resolve_input_path(args.query_file)
        return path.read_text(encoding="utf-8"), f"query-file:{path.name}"
    if args.image:
        image_path = resolve_input_path(args.image)
        ocr_text = load_ocr_text(image_path)
        if not ocr_text.strip():
            raise SystemExit(f"OCR did not extract any text from {image_path}.")
        return ocr_text, f"image:{image_path.name}"
    raise SystemExit("Pass --image, --query, or --query-file.")


def lookup_problem(query_text: str, query_source: str) -> ArchiveResult | None:
    lookup = ProblemLookup()
    filename_hint = ""
    if query_source.startswith("image:"):
        filename_hint = Path(query_source.split(":", 1)[1]).stem.replace("_", " ")

    for candidate, source in (
        (query_text, "ocr"),
        (f"{filename_hint}\n{query_text}".strip(), "filename+ocr"),
        (filename_hint, "filename"),
    ):
        if not candidate.strip():
            continue
        result = lookup.lookup(candidate)
        if result is None:
            continue
        return ArchiveResult(
            status="matched",
            query_text=query_text,
            query_source=source,
            title=result.title,
            problem_id=result.problem_id,
            path=result.path,
            score=result.score,
            match_type=result.match_type,
        )
    return None


def archive_problem(
    query_text: str,
    query_source: str,
    title: str | None = None,
    dry_run: bool = False,
    solution_source: str | None = None,
) -> ArchiveResult:
    index_items = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    problem_number = next_problem_number(index_items)
    problem_id = f"p{problem_number:03d}"

    inferred_title = title or infer_title(query_text, fallback_name=query_source)
    slug = ensure_unique_slug(slugify(inferred_title), index_items)
    folder_name = f"{problem_id}_{slug}"
    problem_dir = ROOT_DIR / "problems" / folder_name
    source_name = query_source.split(":", 1)[1] if ":" in query_source else query_source

    entry = build_index_entry(problem_id, slug, inferred_title, query_text, source_name)
    problem_md = build_problem_markdown(problem_id, inferred_title, query_text, source_name)

    if not dry_run:
        problem_dir.mkdir(parents=True, exist_ok=False)
        (problem_dir / "__init__.py").write_text("# Problem package marker.\n", encoding="utf-8")
        (problem_dir / "problem.md").write_text(problem_md + "\n", encoding="utf-8")

        if solution_source:
            solution_text = Path(solution_source).read_text(encoding="utf-8")
        else:
            solution_text = build_solution_stub(inferred_title)
        (problem_dir / "solution.py").write_text(solution_text, encoding="utf-8")

        index_items.append(entry)
        INDEX_PATH.write_text(json.dumps(index_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return ArchiveResult(
        status="archived",
        query_text=query_text,
        query_source=query_source,
        title=inferred_title,
        problem_id=problem_id,
        slug=slug,
        path=f"problems/{folder_name}",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OCR an image, look up matching archived problems, and optionally create a new draft archive."
    )
    parser.add_argument("--image", help="Problem screenshot path.")
    parser.add_argument("--query", help="Problem statement text passed inline.")
    parser.add_argument("--query-file", help="Path to a text file containing the problem statement.")
    parser.add_argument("--archive-on-miss", action="store_true", help="Create a new draft archive when no match is found.")
    parser.add_argument("--title", help="Override the auto-generated title used for new archives.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be archived without writing files.")
    parser.add_argument("--solution-source", help="Optional Python solution file to copy into the new archive.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--copy-image", action="store_true", help="Copy the source image into the new problem directory.")
    return parser


def _print_result(result: ArchiveResult, as_json: bool) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "status": result.status,
                    "problem_id": result.problem_id,
                    "title": result.title,
                    "slug": result.slug,
                    "path": result.path,
                    "score": round(result.score, 3) if result.score is not None else None,
                    "match_type": result.match_type,
                    "query_source": result.query_source,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if result.status == "matched":
        print(f"Matched {result.problem_id} {result.title}")
        print(f"score: {result.score:.3f}")
        print(f"path: {result.path}")
        return

    print(f"Archived {result.problem_id} {result.title}")
    print(f"path: {result.path}")


def maybe_copy_image(args: argparse.Namespace, result: ArchiveResult) -> None:
    if not args.copy_image or not args.image or result.status != "archived" or args.dry_run:
        return

    image_path = resolve_input_path(args.image)
    destination = ROOT_DIR / result.path / image_path.name
    shutil.copy2(image_path, destination)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    query_text, query_source = read_query(args)
    matched = lookup_problem(query_text, query_source)
    if matched is not None:
        _print_result(matched, args.json)
        return 0

    if not args.archive_on_miss:
        print("No matching archived problem found.")
        return 1

    archived = archive_problem(
        query_text=query_text,
        query_source=query_source,
        title=args.title,
        dry_run=args.dry_run,
        solution_source=args.solution_source,
    )
    maybe_copy_image(args, archived)
    _print_result(archived, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
