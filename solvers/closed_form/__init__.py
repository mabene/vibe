"""
No-search algorithms for Tower of Hanoi.

This solver performs no search through the state space. Instead, it directly
computes the optimal solution by exploiting the mathematical structure of
classical Tower of Hanoi puzzles where the branching factor is effectively 1.
"""

from .closed_form_solver import ClosedFormSolver

__all__ = [
    'ClosedFormSolver'
] 