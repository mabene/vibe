# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Iterative deepening solver for Tower of Hanoi puzzles.

This module provides an implementation of the iterative deepening search algorithm
for solving Tower of Hanoi puzzles. This algorithm combines the space efficiency of
depth-first search with the optimality guarantee of breadth-first search.
"""

from collections import deque
from typing import List, Tuple, Optional, Dict, Any

from ..base_solver import BaseSolver
from ..hanoi_state import HanoiState

class IterativeDeepeningSolver(BaseSolver):
    """
    Iterative deepening solver for Tower of Hanoi puzzles.
    
    This solver uses iterative deepening search, which repeatedly performs
    depth-limited search with increasing depth limits until a solution is found.
    This combines the space efficiency of DFS with the optimality guarantee of BFS.
    """
    
    def __init__(self, initial_state: HanoiState, target_state: HanoiState):
        """
        Initialize the iterative deepening solver.
        
        Args:
            initial_state: The starting configuration of the puzzle.
            target_state: The desired final configuration of the puzzle.
        """
        super().__init__(initial_state, target_state)
        # Track the maximum depth reached during the search
        self._max_depth_reached = 0
        
    def _solve_internal(self, max_liftable_disks: int = 1, quiet: bool = False) -> List[Tuple[int, int, int]]:
        """
        Solve the puzzle using iterative deepening search.
        
        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.
            quiet: If True, suppress progress output during search.
            
        Returns:
            A list of moves representing the solution path.
        """
        # Start with depth limit of 0 and increase until solution found
        depth_limit = 0
        
        while True:
            # Display progress if not quiet
            if not quiet:
                print(f"Trying depth limit {depth_limit}...")
            
            # Perform depth-limited search
            result = self._depth_limited_search(depth_limit, max_liftable_disks)
            
            # Record this iteration
            self._stats_add_iteration(depth_limit)
            
            if result is not None:
                return result
            
            # Increase depth limit for next iteration
            depth_limit += 1
            
            # Safety check to prevent infinite loops
            if depth_limit > 1000:  # Arbitrary large limit
                raise RuntimeError("Search depth limit exceeded (1000). Puzzle may be unsolvable.")
    
    def _depth_limited_search(self, depth_limit: int, max_liftable_disks: int) -> Optional[List[Tuple[int, int, int]]]:
        """
        Perform depth-limited search up to the specified depth.
        
        Args:
            depth_limit: Maximum depth to search.
            max_liftable_disks: Maximum number of disks that can be lifted at once.
            
        Returns:
            A list of moves if solution found within depth limit, None otherwise.
        """
        # Use a stack to track path, state, and depth
        stack = [(self.initial_state, [], 0)]  # (state, path, depth)
        visited_at_depth = set()
        
        while stack:
            current_state, path, depth = stack.pop()
            
            # Update statistics
            self._stats_node_explored()
            self._stats_data_structure_size(len(stack))
            self._max_depth_reached = max(self._max_depth_reached, depth)
            
            # Check if we've reached the target
            if current_state == self.target_state:
                return path
            
            # If we've reached the depth limit, don't expand further
            if depth >= depth_limit:
                continue
            
            # Generate all possible moves from current state
            moves = self._get_possible_moves(current_state, max_liftable_disks)
            
            for move in moves:
                from_peg, to_peg, num_disks = move
                
                try:
                    # Apply the move to get new state
                    new_state = current_state.apply_move(from_peg, to_peg, num_disks)
                    
                    # Create state-depth key to avoid revisiting same state at same depth
                    state_depth_key = (new_state, depth + 1)
                    
                    if state_depth_key not in visited_at_depth:
                        visited_at_depth.add(state_depth_key)
                        
                        # Update statistics
                        self._stats_node_generated()
                        
                        # Add to stack for exploration
                        new_path = path + [move]
                        stack.append((new_state, new_path, depth + 1))
                        
                except ValueError:
                    # Move is invalid, skip it
                    continue
        
        # No solution found within depth limit
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get detailed statistics about the search process.
        
        Returns:
            A dictionary containing statistics about the search.
        """
        base_stats = super().get_stats()
        base_stats.update({
            'max_depth_reached': self._max_depth_reached,
            'algorithm_name': 'Iterative Deepening'
        })
        return base_stats 