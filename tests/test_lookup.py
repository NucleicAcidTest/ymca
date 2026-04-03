from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from problems.lookup import ProblemLookup


class ProblemLookupTests(unittest.TestCase):
    def _make_lookup(self) -> ProblemLookup:
        temp_dir = Path(tempfile.mkdtemp())
        cache_path = temp_dir / "problem_lookup_cache.json"
        return ProblemLookup(cache_path=cache_path)

    def test_finds_problem_from_hints(self) -> None:
        lookup = self._make_lookup()
        query = """
        In a virtual memory management system using Least Recently Used (LRU) cache,
        count the number of cache misses for a sequence of page requests.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p009")
        self.assertIn("countCacheMisses", result.solution_text)

    def test_repeated_query_hits_cache(self) -> None:
        lookup = self._make_lookup()
        query = """
        remove all the duplicate numbers and print the list in the same order as they
        appear in the input list, keeping only distinct numbers
        """

        first_result = lookup.lookup(query)
        second_result = lookup.lookup(query)

        self.assertIsNotNone(first_result)
        self.assertIsNotNone(second_result)
        self.assertEqual(second_result.match_type, "cached-query")
        self.assertTrue(second_result.metadata["cache_hit"])

    def test_cache_file_is_persisted(self) -> None:
        temp_dir = Path(tempfile.mkdtemp())
        cache_path = temp_dir / "problem_lookup_cache.json"
        lookup = ProblemLookup(cache_path=cache_path)

        result = lookup.lookup("car racing game registration number smallest permutation never starts with zero")

        self.assertIsNotNone(result)
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        self.assertEqual(len(payload["query_cache"]), 1)

    def test_finds_remove_vowels_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        The vowels of the English alphabet are a, e, i, o, u, A, E, I, O, U.
        Write an algorithm to eliminate all vowels from a given string.
        Print a string that excludes all the vowels of the given input string.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p010")
        self.assertIn("removeVowels", result.solution_text)


if __name__ == "__main__":
    unittest.main()
