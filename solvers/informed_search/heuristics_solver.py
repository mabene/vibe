# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Abstract base class for heuristic-based Tower of Hanoi solvers.
"""
from abc import ABC
from typing import TYPE_CHECKING
import math
import sys
import os

# Add the parent directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solvers.base_solver import BaseSolver

if TYPE_CHECKING:
    from ..hanoi_state import HanoiState

class HeuristicsSolver(BaseSolver, ABC):
    """
    Abstract base class for heuristic-based Tower of Hanoi solvers.
    
    This class extends BaseSolver with heuristic functions that can be used
    by informed search algorithms like A* and IDA*. It provides admissible
    heuristics that maintain optimality guarantees while guiding the search.
    """
    
    def _blocking_disks_heuristic(self, state: 'HanoiState', max_liftable_disks: int = 1) -> int:
        """
        Admissible heuristic for multi-disk Tower of Hanoi.
        
        Counts disks not in their final position and divides by max_liftable_disks
        to get a lower bound on the number of moves needed. This maintains
        admissibility when multiple disks can be moved at once.
        
        Args:
            state: The current state to evaluate.
            max_liftable_disks: Maximum number of disks that can be lifted at once.
            
        Returns:
            Lower bound estimate of moves needed to reach target.
        """
        # Count total disks not in their final position
        misplaced_disks = 0
        
        for peg_idx in range(len(state.pegs)):
            current_peg = state.pegs[peg_idx]
            target_peg = self.target_state.pegs[peg_idx]
            
            # Find the deepest correctly placed disks
            correct_bottom = 0
            while (correct_bottom < len(current_peg) and 
                   correct_bottom < len(target_peg) and
                   current_peg[correct_bottom] == target_peg[correct_bottom]):
                correct_bottom += 1
            
            # All disks above the correctly placed bottom are misplaced
            misplaced_disks += len(current_peg) - correct_bottom
        
        # With max_liftable_disks per move, we need at least ceil(misplaced / max_liftable) moves
        return math.ceil(misplaced_disks / max_liftable_disks) if misplaced_disks > 0 else 0 