# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements an A* solver for the Tower of Hanoi problem using the blocking disks heuristic.
"""
from typing import List, Tuple, Dict, Set, Optional, TYPE_CHECKING
import heapq
from .heuristics_solver import HeuristicsSolver

if TYPE_CHECKING:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ..hanoi_state import HanoiState

class AStarSolver(HeuristicsSolver):
    """
    A solver that uses A* search algorithm with an admissible heuristic.
    
    This solver combines the optimality guarantees of BFS with the efficiency
    of heuristic-guided search. It uses the "blocking disks" heuristic which
    counts disks that must be moved to unblock correctly placed disks.
    
    A* guarantees finding the shortest solution while often exploring fewer
    states than pure BFS by using the heuristic to guide the search.
    """
    
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Performs A* search to find the optimal solution.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            
        Returns:
            A list of moves representing the shortest solution path.
            
        Raises:
            RuntimeError: If no solution is found (should not happen for valid puzzles).
        """
        # Priority queue: (f_score, g_score, counter, state, path)
        # f_score = g_score + heuristic (estimated total cost)
        # g_score = actual cost from start (number of moves)
        # counter = unique tie-breaker to avoid comparing HanoiState objects
        counter = 0
        open_set = [(self._blocking_disks_heuristic(self.initial_state, max_liftable_disks), 0, counter, self.initial_state, [])]
        
        # Keep track of visited states and their best g_scores
        visited: Set['HanoiState'] = set()
        g_scores: Dict['HanoiState', int] = {self.initial_state: 0}
        
        # Track initial state generation
        self._stats_node_generated()
        
        while open_set:
            # Track maximum queue size
            self._stats_data_structure_size(len(open_set))
            
            f_score, g_score, _, current_state, path = heapq.heappop(open_set)
            
            # Check if we've reached the target
            if current_state == self.target_state:
                return path
            
            # Skip if we've already processed this state with a better path
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
                    
                    # Calculate new g_score (cost from start)
                    tentative_g_score = g_score + 1
                    
                    # Skip if we've seen this state with a better or equal g_score
                    if (next_state in g_scores and 
                        g_scores[next_state] <= tentative_g_score):
                        continue
                    
                    # Skip if already visited (and thus processed optimally)
                    if next_state in visited:
                        continue
                    
                    # This is the best path to next_state so far
                    g_scores[next_state] = tentative_g_score
                    
                    # Calculate f_score = g_score + heuristic
                    h_score = self._blocking_disks_heuristic(next_state, max_liftable_disks)
                    f_score = tentative_g_score + h_score
                    
                    # Add to priority queue
                    new_path = path + [(from_peg, to_peg, num_disks)]
                    counter += 1
                    heapq.heappush(open_set, (f_score, tentative_g_score, counter, next_state, new_path))
                    self._stats_node_generated()
                    
                except ValueError:
                    # Invalid move, skip
                    continue
        
        # Should never reach here for valid Tower of Hanoi puzzles
        raise RuntimeError("A* search completed without finding a solution. This indicates a bug.") 