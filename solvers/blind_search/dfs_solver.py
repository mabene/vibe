# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements a depth-first search solver for the Tower of Hanoi problem.
"""
from typing import List, Tuple, Set, Optional, TYPE_CHECKING
from collections import deque
from ..base_solver import BaseSolver

if TYPE_CHECKING:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ..hanoi_state import HanoiState

class DFSSolver(BaseSolver):
    """
    A solver that uses depth-first search to find solutions.
    
    This solver explores paths deeply before backtracking, making it very
    memory efficient and fast at finding *any* solution (not necessarily
    the shortest). It uses cycle detection to avoid infinite loops and
    an iterative stack-based approach to avoid Python's recursion limits.
    """
    
    def _solve_internal(self, max_liftable_disks: int = 1, max_depth: Optional[int] = None) -> List[Tuple[int, int, int]]:
        """
        Performs depth-first search to find a solution.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            max_depth: Maximum depth to search (None = no limit).
            
        Returns:
            A list of moves representing a solution path (not necessarily shortest).
            
        Raises:
            RuntimeError: If no solution is found within the maximum depth.
        """
        # Use iterative DFS with explicit stack
        # Stack contains: (current_state, path_so_far, depth)
        stack = deque([(self.initial_state, [], 0)])
        visited = set()
        
        # Track initial state generation
        self._stats_node_generated()
        
        while stack:
            # Track maximum stack size
            self._stats_data_structure_size(len(stack))
            
            current_state, path, depth = stack.pop()
            
            # Check if we've reached the target
            if current_state == self.target_state:
                return path
            
            # Check depth limit
            if max_depth is not None and depth >= max_depth:
                continue
                
            # Skip if we've already visited this state
            if current_state in visited:
                continue
                
            # Mark as visited and count as explored
            visited.add(current_state)
            self._stats_node_explored()
            
            # Get all possible moves from current state
            possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
            
            # Add all valid next states to stack (in reverse order for consistent DFS behavior)
            for from_peg, to_peg, num_disks in reversed(possible_moves):
                try:
                    next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                    
                    # Only add if not already visited
                    if next_state not in visited:
                        new_path = path + [(from_peg, to_peg, num_disks)]
                        stack.append((next_state, new_path, depth + 1))
                        self._stats_node_generated()
                        
                except ValueError:
                    # Invalid move, skip
                    continue
        
        # No solution found
        if max_depth is not None:
            raise RuntimeError(f"No solution found within maximum depth of {max_depth}")
        else:
            raise RuntimeError("DFS search completed without finding a solution. This indicates a bug.") 