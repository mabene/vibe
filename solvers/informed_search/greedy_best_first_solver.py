# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements a Greedy Best-First Search solver for the Tower of Hanoi problem.
"""
from typing import List, Tuple, Set, TYPE_CHECKING
import heapq
from .heuristics_solver import HeuristicsSolver

if TYPE_CHECKING:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ..hanoi_state import HanoiState

class GreedyBestFirstSolver(HeuristicsSolver):
    """
    A solver that uses Greedy Best-First Search algorithm with the blocking disks heuristic.
    
    This solver prioritizes nodes based solely on their heuristic value (estimated distance
    to the goal), without considering the actual path cost. This makes it faster than A*
    but sacrifices optimality guarantees - it may find a solution quickly but not necessarily
    the shortest one.
    
    The algorithm uses a priority queue where nodes with lower heuristic values (closer to
    the goal) are explored first.
    """
    
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Performs Greedy Best-First Search to find a solution.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            
        Returns:
            A list of moves representing a solution path (not necessarily shortest).
            
        Raises:
            RuntimeError: If no solution is found (should not happen for valid puzzles).
        """
        # Priority queue: (heuristic_score, counter, state, path)
        # heuristic_score = estimated cost to goal
        # counter = unique tie-breaker to avoid comparing HanoiState objects
        counter = 0
        open_set = [(self._blocking_disks_heuristic(self.initial_state, max_liftable_disks), counter, self.initial_state, [])]
        
        # Keep track of visited states to avoid cycles
        visited: Set['HanoiState'] = set()
        
        # Track initial state generation
        self._stats_node_generated()
        
        while open_set:
            # Track maximum queue size
            self._stats_data_structure_size(len(open_set))
            
            h_score, _, current_state, path = heapq.heappop(open_set)
            
            # Check if we've reached the target
            if current_state == self.target_state:
                return path
            
            # Skip if we've already processed this state
            if current_state in visited:
                continue
                
            # Mark as visited and count as explored
            visited.add(current_state)
            self._stats_node_explored()
            
            # Explore all possible moves from current state
            possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
            
            for from_peg, to_peg, num_disks in possible_moves:
                try:
                    next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                    
                    # Skip if already visited
                    if next_state in visited:
                        continue
                    
                    # Calculate heuristic score for the next state
                    h_score = self._blocking_disks_heuristic(next_state, max_liftable_disks)
                    
                    # Add to priority queue (greedy: only use heuristic, ignore path cost)
                    new_path = path + [(from_peg, to_peg, num_disks)]
                    counter += 1
                    heapq.heappush(open_set, (h_score, counter, next_state, new_path))
                    self._stats_node_generated()
                    
                except ValueError:
                    # Invalid move, skip
                    continue
        
        # Should never reach here for valid Tower of Hanoi puzzles
        raise RuntimeError("Greedy Best-First Search completed without finding a solution. This indicates a bug.") 