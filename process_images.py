from __future__ import annotations

import json
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

from problems.lookup import ProblemLookup


ROOT_DIR = Path(__file__).resolve().parent
IMG_DIR = ROOT_DIR / "img"
REPORT_PATH = ROOT_DIR / ".cache" / "image_lookup_report.json"


def main() -> int:
    ocr = RapidOCR()
    lookup = ProblemLookup()
    results = []

    for image_path in sorted(path for path in IMG_DIR.iterdir() if path.is_file()):
        ocr_result, _ = ocr(str(image_path))
        text_lines = [item[1] for item in ocr_result] if ocr_result else []
        ocr_text = "\n".join(text_lines).strip()
        filename_query = image_path.stem.replace("_", " ")

        lookup_result = None
        query_source = None
        for candidate, source in (
            (ocr_text, "ocr"),
            (f"{filename_query}\n{ocr_text}".strip(), "filename+ocr"),
            (filename_query, "filename"),
        ):
            if not candidate:
                continue
            lookup_result = lookup.lookup(candidate)
            if lookup_result is not None:
                query_source = source
                break

        results.append(
            {
                "image": image_path.name,
                "ocr_length": len(ocr_text),
                "match_found": lookup_result is not None,
                "problem_id": lookup_result.problem_id if lookup_result else None,
                "title": lookup_result.title if lookup_result else None,
                "score": round(lookup_result.score, 3) if lookup_result else None,
                "match_type": lookup_result.match_type if lookup_result else None,
                "cache_hit": lookup_result.metadata.get("cache_hit", False) if lookup_result else False,
                "query_source": query_source,
                "ocr_preview": ocr_text[:400],
            }
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
