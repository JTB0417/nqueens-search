import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nqueens_search import is_valid_solution, solve_nqueens


class NQueensTests(unittest.TestCase):
    def test_eight_queens(self):
        solution, _, _ = solve_nqueens(8, time_limit=2.0)
        self.assertIsNotNone(solution)
        self.assertTrue(is_valid_solution(solution))

    def test_unsolvable_sizes(self):
        for size in (2, 3):
            solution, _, _ = solve_nqueens(size)
            self.assertIsNone(solution)

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            solve_nqueens(0)


if __name__ == "__main__":
    unittest.main()

