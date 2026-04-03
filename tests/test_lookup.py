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
        self.assertIn("aeiouAEIOU", result.solution_text)

    def test_finds_remove_vowels_houses_variant(self) -> None:
        lookup = self._make_lookup()
        query = """
        In a town, the houses are marked with English letters. Because funds are limited,
        the committee decides to renovate only the houses marked with vowels and asks the members
        to identify the list of houses that will not be renovated.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p010")
        self.assertIn("houses = input().strip()", result.solution_text)

    def test_finds_two_circle_intersection_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        A student must solve an entire workbook of problems related to finding the area of intersection of two circles.
        The first line of the input consists of three space-separated integers x1, y1 and r1 where x1 and y1 represent
        the x and y coordinates of the center of the first circle and r1 represents the radius of the first circle.
        The second line of the input consists of three space-separated integers x2, y2 and r2 where x2 and y2 represent
        the x and y coordinates of the center of the second circle and r2 represents the radius of the second circle.
        Print a real number representing the area of intersection of two circles rounded up to 6 decimal places.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p015")
        self.assertIn("math.hypot", result.solution_text)

    def test_finds_maximum_internship_salary_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        Stephen is doing an internship in a company for N days. Each day, he may choose either an easy task
        or a difficult task. He may also choose to perform no task at all. He can only choose a difficult task
        on the first day of the internship or the day when he did not perform any work on the previous day.
        The amount paid by the company for both tasks can vary each day. Calculate the maximum salary he can get.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p016")
        self.assertIn("new_dp2 = dp0 + hard", result.solution_text)

    def test_finds_minimum_straight_line_pickup_routes_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        A company wants to start its transportation service in the city of Nazeriana.
        It has a base location and some pickup locations. Identify the straight line routes
        starting from the base location such that the number of routes are minimized and all
        the pickup locations are covered.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p017")
        self.assertIn("lines.add((dx, dy))", result.solution_text)

    def test_finds_minimum_juice_stalls_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        John misses his bus and has to walk all his way from home to school.
        The distance between home and school is D units. He starts with initial energy K.
        There are N juice stalls on the way, with distances dist_i and juice liters lit_i.
        Find the minimum number of juice stalls he should stop at to reach school, or output -1.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p018")
        self.assertIn("heapq.heappush", result.solution_text)

    def test_finds_kth_soldier_after_range_reversals_problem(self) -> None:
        lookup = self._make_lookup()
        query = """
        There are N soldiers standing in a line with IDs from 1 to N.
        Each action round gives Li and Ri and reverses the whole segment from Li to Ri.
        After Q rounds, find the ID of the soldier at the Kth position.
        """

        result = lookup.lookup(query)

        self.assertIsNotNone(result)
        self.assertEqual(result.problem_id, "p019")
        self.assertIn("left + right - k", result.solution_text)


if __name__ == "__main__":
    unittest.main()
