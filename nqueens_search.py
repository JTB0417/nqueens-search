"""Solve N-Queens with bitmasks and priority-queue search."""

from __future__ import annotations

import argparse
import heapq
import time
from dataclasses import dataclass


@dataclass(slots=True)
class Node:
    row: int
    columns: int
    descending_diagonals: int
    ascending_diagonals: int
    parent: "Node | None"
    chosen_column: int


def build_column_order(size: int) -> list[int]:
    midpoint = (size - 1) / 2
    return sorted(range(size), key=lambda column: (abs(column - midpoint), column))


def reconstruct_solution(goal: Node) -> list[int]:
    solution: list[int] = []
    current = goal
    while current.parent is not None:
        solution.append(current.chosen_column)
        current = current.parent
    return list(reversed(solution))


def solve_nqueens(size: int, time_limit: float = 1.0) -> tuple[list[int] | None, float, int]:
    if size < 1:
        raise ValueError("Board size must be positive")
    if time_limit <= 0:
        raise ValueError("Time limit must be positive")

    started = time.perf_counter()
    if size in (2, 3):
        return None, time.perf_counter() - started, 0

    all_columns = (1 << size) - 1
    column_order = build_column_order(size)
    root = Node(0, 0, 0, 0, None, -1)
    frontier: list[tuple[int, int, int, Node]] = [(size, 0, 0, root)]
    sequence = 1
    expanded = 0

    while frontier:
        if time.perf_counter() - started > time_limit:
            return None, time.perf_counter() - started, expanded

        _, _, _, node = heapq.heappop(frontier)
        expanded += 1
        if node.row == size:
            return reconstruct_solution(node), time.perf_counter() - started, expanded

        available = all_columns & ~(
            node.columns | node.descending_diagonals | node.ascending_diagonals
        )
        for column in column_order:
            bit = 1 << column
            if not available & bit:
                continue
            child = Node(
                row=node.row + 1,
                columns=node.columns | bit,
                descending_diagonals=(node.descending_diagonals | bit) << 1,
                ascending_diagonals=(node.ascending_diagonals | bit) >> 1,
                parent=node,
                chosen_column=column,
            )
            heapq.heappush(frontier, (size, -child.row, sequence, child))
            sequence += 1

    return None, time.perf_counter() - started, expanded


def is_valid_solution(solution: list[int]) -> bool:
    size = len(solution)
    return (
        len(set(solution)) == size
        and len({row - column for row, column in enumerate(solution)}) == size
        and len({row + column for row, column in enumerate(solution)}) == size
    )


def print_board(solution: list[int], max_rows: int = 60) -> None:
    for column in solution[:max_rows]:
        print("." * column + "Q" + "." * (len(solution) - column - 1))
    if len(solution) > max_rows:
        print("... board truncated ...")


def stress_test(time_limit: float) -> None:
    sizes = [8, 10, 12, 14, 16, 20, 30, 50, 75, 100, 150, 200, 300, 500]
    print(" N     Time(s)     Nodes     Solved")
    print("----------------------------------")
    for size in sizes:
        solution, elapsed, expanded = solve_nqueens(size, time_limit)
        solved = solution is not None and is_valid_solution(solution)
        print(f"{size:>3}   {elapsed:>8.4f}   {expanded:>7}   {solved}")
        if not solved:
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=8, help="board size")
    parser.add_argument("--time-limit", type=float, default=1.0)
    parser.add_argument("--show-board", action="store_true")
    parser.add_argument("--stress-test", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.stress_test:
        stress_test(args.time_limit)
    else:
        solution, elapsed, expanded = solve_nqueens(args.n, args.time_limit)
        print(f"Solved: {solution is not None}")
        print(f"Time: {elapsed:.6f} seconds")
        print(f"Nodes expanded: {expanded}")
        if solution is not None:
            print("Columns:", solution)
            if args.show_board:
                print_board(solution)

