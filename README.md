# N-Queens Heuristic Search

A bitmask-based solver that places queens one row at a time and benchmarks increasingly large boards under a configurable time limit.

## Highlights

- Tracks occupied columns and diagonals with integer bitmasks.
- Reconstructs a solution using parent pointers.
- Orders candidate columns from the center outward.
- Reports execution time and expanded nodes.
- Includes automated checks that verify every returned board.

## Run

```bash
python nqueens_search.py --n 8 --show-board
python nqueens_search.py --stress-test
```

## Test

```bash
python -m unittest discover -s tests
```

## Search behavior

The original exercise framed the solution as A*. Because `g` is the placed-row count and `h` is the remaining-row count, `f = g + h` is constant. The priority queue therefore relies on its depth tie-breaker and behaves like a depth-first heuristic search. This repository states that limitation explicitly while retaining the priority-queue formulation for comparison and experimentation.

