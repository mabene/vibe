# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements the general-purpose BFS solver for any valid Tower of Hanoi puzzle.
"""
from typing import List, Deque, TYPE_CHECKING, Tuple, Set
from collections import deque
from ..base_solver import BaseSolver

if TYPE_CHECKING:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ..hanoi_state import HanoiState

class GeneralBFSSolver(BaseSolver):
    """
    A solver that uses a Breadth-First Search (BFS) algorithm.

    This solver is guaranteed to find the shortest possible solution for any
    valid, solvable puzzle configuration. It is more general but less
    performant than the recursive solver for classical puzzles.
    """
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Performs breadth-first search to find the shortest solution.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            
        Returns:
            A list of moves representing the shortest solution path.
            
        Raises:
            RuntimeError: If no solution is found (should not happen for valid puzzles).
        """
        # Initialize queue with the initial state
        queue: Deque[Tuple['HanoiState', List[Tuple[int, int, int]]]] = deque([(self.initial_state, [])])
        visited: Set['HanoiState'] = set()
        
        # Track initial state generation
        self._stats_node_generated()
        
        while queue:
            # Track maximum queue size
            self._stats_data_structure_size(len(queue))
            
            current_state, path = queue.popleft()
            
            # Skip if we've already visited this state
            if current_state in visited:
                continue
            
            # Mark as visited and count as explored
            visited.add(current_state)
            self._stats_node_explored()
            
            # Check if we've reached the target
            if current_state == self.target_state:
                return path
            
            # Generate all possible moves from the current state
            possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
            
            for from_peg, to_peg, num_disks in possible_moves:
                try:
                    next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                    
                    # Skip if already visited
                    if next_state not in visited:
                        new_path = path + [(from_peg, to_peg, num_disks)]
                        queue.append((next_state, new_path))
                        self._stats_node_generated()
                        
                except ValueError:
                    # Invalid move, skip
                    continue
        
        # Should never reach here for valid Tower of Hanoi puzzles
        raise RuntimeError("BFS search completed without finding a solution. This indicates a bug.")

 