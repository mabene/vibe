# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
This package contains the various solver strategy implementations.

Solvers are organized by their fundamental algorithmic approach:
- blind_search: Uninformed search algorithms (BFS, DFS, etc.)
- informed_search: Heuristic-guided search algorithms (A*, IDA*)  
- closed_form: Closed form solution algorithms (ClosedFormSolver)
"""
from .base_solver import BaseSolver

# Import from organized subdirectories
from .blind_search import (
    GeneralBFSSolver,
    DFSSolver, 
    BidirectionalBFSSolver,
    ParallelBidirectionalBFSSolver,
    IterativeDeepeningSolver
)
from .informed_search import (
    AStarSolver,
    IDAStarSolver,
    GreedyBestFirstSolver
)
from .closed_form import (
    ClosedFormSolver
)

__all__ = [
    'BaseSolver', 
    # Blind search algorithms
    'GeneralBFSSolver', 
    'DFSSolver',
    'BidirectionalBFSSolver', 
    'ParallelBidirectionalBFSSolver', 
    'IterativeDeepeningSolver',
    # Informed search algorithms  
    'AStarSolver', 
    'IDAStarSolver',
    'GreedyBestFirstSolver',
    # No-search algorithms
    'ClosedFormSolver'
] 