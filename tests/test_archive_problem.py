from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import archive_problem


class ArchiveProblemTests(unittest.TestCase):
    def test_extract_sections_reads_example_blocks(self) -> None:
        text = """
        Question
        An alternate sort of a list consists of alternate elements after sorting.
        Input
        The first line contains N.
        Example
        Input:
        8
        3 5 1 5 9 10 2 6
        Output:
        1 3 5 9
        """

        sections = archive_problem.extract_sections(text)

        self.assertIn("An alternate sort of a list consists of alternate elements after sorting", sections["body"][0])
        self.assertEqual(archive_problem.collect_sample_input_prefix(sections), ["8", "3 5 1 5 9 10 2 6"])
        self.assertEqual(archive_problem.collect_sample_output(sections), "1 3 5 9")

    def test_infer_title_handles_known_problem_patterns(self) -> None:
        text = """
        You are given a list of numbers. Write an algorithm to remove all the duplicate numbers
        of the given list so that the list contains only distinct numbers in the same order.
        """

        title = archive_problem.infer_title(text)

        self.assertEqual(title, "Remove Duplicates Preserve Order")

    def test_archive_problem_dry_run_allocates_next_problem_id(self) -> None:
        temp_dir = Path(tempfile.mkdtemp())
        problems_dir = temp_dir / "problems"
        problems_dir.mkdir()
        index_path = problems_dir / "index.json"
        index_path.write_text(
            json.dumps(
                [
                    {
                        "problem_id": "p001",
                        "slug": "sample_problem",
                        "title": "Sample Problem",
                        "path": "problems/p001_sample_problem/solution.py",
                    }
                ],
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        with mock.patch.object(archive_problem, "ROOT_DIR", temp_dir), mock.patch.object(
            archive_problem, "INDEX_PATH", index_path
        ):
            result = archive_problem.archive_problem(
                query_text="A perfect number is a number which is equal to the sum of all its factors.",
                query_source="inline-query",
                dry_run=True,
            )

        self.assertEqual(result.problem_id, "p002")
        self.assertEqual(result.slug, "perfect_number_check")
        self.assertEqual(result.status, "archived")


if __name__ == "__main__":
    unittest.main()
