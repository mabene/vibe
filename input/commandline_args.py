# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Configures the command-line argument parser for the Hanoi solver application.

This module encapsulates all the details of the command-line interface,
keeping the main application script (`hanoi.py`) clean and focused on its
core logic. It uses Python's `argparse` library to define the expected
arguments, their types, and their help messages.
"""
import argparse
from .instance_parser import validate_instance_format

def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser for the command-line interface.

    This function defines the entire CLI structure, including the mutually
    exclusive modes for puzzle generation (`--classic` vs. `--random` vs. `--instance`) and
    the options for controlling output verbosity (`--show`).
    
    Returns:
        An `argparse.ArgumentParser` object fully configured and ready to parse
        the command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A flexible solver for the Tower of Hanoi puzzle, developed through human-AI collaboration.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-c', '--classic', type=int, metavar='N', help="Solve a classical puzzle with N disks.")
    mode_group.add_argument('-r', '--random', type=int, metavar='N', help="Find the path between two random N-disk states.")
    mode_group.add_argument(
        '-i', '--instance', 
        type=validate_instance_format,
        metavar='SPEC',
        help="""Solve a custom instance specified as "INITIAL>FINAL" where:
  INITIAL and FINAL are in the form PEG1:PEG2:PEG3, where
  each PEG1/2/3 contains comma-separated disk sizes, top to bottom;
  empty pegs are represented by the empty string.
Examples:
  -i "1,2,3:: > ::1,2,3"                (classical 3-disk problem)
  -i "1,2:3,4:5,6 > 5,6:3,4:1,2"        (simple 6-disk swap)
  -i "1,2,3::4,5,6 > 1,3,4::2,4,6"      (custom rearrangement)"""
    )

    parser.add_argument(
        '-s', '--search',
        choices=['BFS', 'DFS', 'IDE', 'ASTAR', 'IDASTAR', 'GBFS', 'BIBFS', 'PBIBFS', 'CFORM', 'COMPARE'],
        default=None,
        metavar='ALGORITHM',
        help="""Choose the search algorithm to use:
  BFS:      Breadth-First Search (optimal, moderate memory)
  DFS:      Depth-First Search (fast, low memory, non-optimal)
  IDE:      Iterative Deepening (optimal, low memory)
  ASTAR:    A* with heuristic (optimal, efficient search)
  IDASTAR:  Iterative Deepening A* (optimal, very low memory)
  GBFS:     Greedy Best-First Search (fast, low memory, non-optimal)
  BIBFS:    Bidirectional BFS (optimal, faster than BFS)
  PBIBFS:   Parallel Bidirectional BFS (optimal, multi-core)
  CFORM:    Closed Form (optimal, for classical puzzles only)
  COMPARE:  Run all applicable algorithms and compare results
If not specified, the solver will auto-select an appropriate algorithm."""
    )

    parser.add_argument(
        '-l', '--max_lift',
        type=int,
        default=1,
        metavar='N',
        help="""The maximum number of disks that can be lifted in a single move.
Defaults to 1. Using a value > 1 is incompatible with the CFORM solver."""
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        metavar='N',
        help="""Set random seed for reproducible puzzle generation.
If specified, all random puzzle generation will be deterministic.
Using the same seed with the same parameters guarantees identical puzzles and outputs."""
    )
    
    parser.add_argument(
        '--show',
        choices=['summary', 'moves', 'states'],
        default=None,
        help="""Control the output verbosity:
  summary: Show only the final summary.
  moves:   Show the summary and the list of moves (default for <=100 moves).
  states:  Show the summary, moves, and a full visualization of each intermediate state."""
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        metavar='S',
        help="""Set timeout in seconds for algorithm execution.
If any algorithm takes longer than S seconds, it will be terminated with an error.
Defaults to 30 seconds. Applies to all modes including single algorithm execution."""
    )
    
    parser.add_argument(
        '-p', '--profile',
        type=int,
        nargs='?',
        const=1,
        default=None,
        metavar='X',
        help="""Enable detailed profiling and statistics collection.
If not specified, only minimal output is shown and no statistics are collected
to avoid overhead. If specified, full statistics are collected and displayed.
Optional integer argument X defaults to 1. If X > 1, runs X instances of the
puzzle and provides aggregate statistics across all runs."""
    )

    return parser 