"""
IDA* (Iterative Deepening A*) Solver for Tower of Hanoi

This solver combines the memory efficiency of Iterative Deepening with the 
heuristic guidance of A*. It performs depth-first search with iteratively 
increasing f-cost bounds.

Copyright (c) 2025 - A collaborative work by Claude Sonnet 4 and Gemini 2.5 Pro
Licensed under the Unlicense - see LICENSE file for details
Multi-AI development project - Repository: [URL to be added when public]
"""

from typing import List, Optional, Tuple
from .heuristics_solver import HeuristicsSolver
from ..hanoi_state import HanoiState


class IDAStarSolver(HeuristicsSolver):
    """
    IDA* (Iterative Deepening A*) solver.
    
    Combines iterative deepening with A* heuristic guidance:
    - Memory efficient like DFS (O(depth) space)
    - Optimal like A* (with admissible heuristic)
    - Iteratively increases f-cost bound until solution found
    """
    
    def _solve_internal(self, max_liftable_disks: int = 1, quiet: bool = False) -> List[Tuple[int, int, int]]:
        """
        Solve using IDA* algorithm.
        
        Iteratively increases the f-cost bound until a solution is found.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            quiet: If True, suppress progress output during search.
            
        Returns:
            A list of moves representing the shortest solution path.
        """
        # Track initial state generation
        self._stats_node_generated()
        
        # Initial bound is the heuristic value of start state
        bound = self._blocking_disks_heuristic(self.initial_state, max_liftable_disks)
        
        while True:
            if not quiet:
                print(f"IDA* searching with f-cost bound: {bound}")
            self._stats_add_iteration(bound)
            
            # Search with current bound
            moves, next_bound = self._ida_star_search(
                [self.initial_state], [], 0, bound, max_liftable_disks
            )
            
            # If solution found, return the moves
            if moves is not None:
                return moves
                
            # If no improvement possible, no solution exists
            if next_bound >= 999999:
                raise RuntimeError("IDA* search completed without finding a solution. "
                                 "This indicates a bug.")
                
            # Update bound for next iteration
            bound = next_bound
            
    def _ida_star_search(self, state_path: List['HanoiState'], move_path: List[Tuple[int, int, int]], 
                        g_cost: int, bound: int, max_liftable_disks: int) -> Tuple[Optional[List[Tuple[int, int, int]]], int]:
        """
        Recursive IDA* search with f-cost bound.
        
        Args:
            state_path: Current path of states
            move_path: Current path of moves
            g_cost: Current g-cost (moves from start)
            bound: Current f-cost bound
            max_liftable_disks: Maximum disks that can be lifted
            
        Returns:
            (solution_moves, next_bound) where:
            - solution_moves is the move sequence if found, None otherwise
            - next_bound is the minimum f-cost that exceeded the bound
        """
        current_state = state_path[-1]
        f_cost = g_cost + self._blocking_disks_heuristic(current_state, max_liftable_disks)
        
        # Track data structure size (state path for cycle detection)
        self._stats_data_structure_size(len(state_path))
        
        # If f-cost exceeds bound, return the exceeded value
        if f_cost > bound:
            return None, int(f_cost)
            
        # Check if we reached the target
        if current_state == self.target_state:
            return move_path, f_cost
            
        # Track node exploration
        self._stats_node_explored()
        min_exceeded = float('inf')
        
        # Try all possible moves
        for from_peg, to_peg, num_disks in self._get_possible_moves(current_state, max_liftable_disks):
            try:
                new_state = current_state.apply_move(from_peg, to_peg, num_disks)
                self._stats_node_generated()
                
                # Avoid cycles (check if state already in path)
                if new_state in state_path:
                    continue
                    
                # Recursive search with increased g-cost
                new_state_path = state_path + [new_state]
                new_move_path = move_path + [(from_peg, to_peg, num_disks)]
                
                result, exceeded = self._ida_star_search(
                    new_state_path, new_move_path, g_cost + 1, bound, max_liftable_disks
                )
                
                # If solution found, return it
                if result is not None:
                    return result, exceeded
                    
                # Track minimum exceeded f-cost for next iteration
                if exceeded < min_exceeded:
                    min_exceeded = exceeded
                    
            except ValueError:
                # Invalid move, skip
                continue
                
        return None, int(min_exceeded) if min_exceeded != float('inf') else 999999 