# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Base solver class for Tower of Hanoi solvers.

This module provides the base class that all specific solver implementations inherit from,
defining the common interface and shared functionality for solving Tower of Hanoi puzzles.
"""

import abc
import os
import time
from typing import List, Tuple, Set, Optional, Any

from .hanoi_state import HanoiState
from output.profiling_and_comparing import display_search_statistics

class BaseSolver(abc.ABC):
    """
    Abstract base class for a Tower of Hanoi solver.

    This class defines the common interface for all solver strategies. Concrete
    solver classes must inherit from this class and implement the `solve` method.
    """
    def __init__(self, initial_state: 'HanoiState', target_state: 'HanoiState'):
        """
        Initializes the base solver.

        Args:
            initial_state: The starting configuration of the puzzle.
            target_state: The desired final configuration of the puzzle.
        """
        self.initial_state = initial_state
        self.target_state = target_state
        
        # Initialize statistics tracking
        self._stats_start_time: Optional[float] = None
        self._stats_end_time: Optional[float] = None
        self._stats_nodes_explored: int = 0
        self._stats_nodes_generated: int = 0
        self._stats_max_data_structure_size: int = 0
        self._stats_iterations: int = 0
        self._stats_cutoff_bounds: List[Any] = []
        self._stats_solution_length: int = 0

    @abc.abstractmethod
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[tuple[int, int, int]]:
        """
        When implemented in a subclass, this method contains the specific
        algorithm to find a solution path from the initial to the target state.

        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.

        Returns:
            A list of moves representing the solution path.
        
        Raises:
            NotImplementedError: If a subclass does not implement this method.
        """
        raise NotImplementedError
    
    def solve(self, max_liftable_disks: int = 1) -> List[tuple[int, int, int]]:
        """
        Solves the Tower of Hanoi puzzle with statistics tracking.
        
        This method wraps the internal solver with comprehensive performance
        monitoring and displays detailed statistics upon completion.

        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.

        Returns:
            A list of moves representing the solution path.
        """
        # Reset statistics
        self._stats_reset()
        
        # Start timing and memory tracking
        self._stats_start_timing()
        
        try:
            # Call the actual solver implementation
            solution = self._solve_internal(max_liftable_disks)
            
            # Record solution length
            self._stats_solution_length = len(solution)
            
            # End timing
            self._stats_end_timing()
            
            # Display statistics
            self._display_search_statistics()
            
            return solution
            
        except Exception as e:
            # End timing even if solver failed
            self._stats_end_timing()
            raise e
    
    # Statistics tracking helper methods
    def _stats_reset(self) -> None:
        """Reset all statistics counters."""
        self._stats_start_time = None
        self._stats_end_time = None
        self._stats_nodes_explored = 0
        self._stats_nodes_generated = 0
        self._stats_max_data_structure_size = 0
        self._stats_iterations = 0
        self._stats_cutoff_bounds = []
        self._stats_solution_length = 0
    
    def _stats_start_timing(self) -> None:
        """Start timing the solve process."""
        self._stats_start_time = time.perf_counter()
    
    def _stats_end_timing(self) -> None:
        """End timing the solve process."""
        self._stats_end_time = time.perf_counter()
    
    def _stats_node_explored(self) -> None:
        """Increment the nodes explored counter."""
        self._stats_nodes_explored += 1
    
    def _stats_node_generated(self) -> None:
        """Increment the nodes generated counter."""
        self._stats_nodes_generated += 1
    
    def _stats_data_structure_size(self, size: int) -> None:
        """Update the maximum data structure size."""
        self._stats_max_data_structure_size = max(self._stats_max_data_structure_size, size)
    
    def _stats_add_iteration(self, bound: Optional[Any] = None) -> None:
        """Add an iteration, optionally with a cutoff bound."""
        self._stats_iterations += 1
        if bound is not None:
            self._stats_cutoff_bounds.append(bound)
    
    def _display_search_statistics(self) -> None:
        """Display comprehensive search statistics."""
        if self._stats_start_time is None or self._stats_end_time is None:
            return
        
        solve_time = self._stats_end_time - self._stats_start_time
        
        display_search_statistics(
            solve_time=solve_time,
            solution_length=self._stats_solution_length,
            nodes_explored=self._stats_nodes_explored,
            nodes_generated=self._stats_nodes_generated,
            max_data_structure_size=self._stats_max_data_structure_size,
            iterations=self._stats_iterations,
            cutoff_bounds=self._stats_cutoff_bounds if self._stats_cutoff_bounds else None
        )
    
    def _get_possible_moves(self, current_state, max_liftable_disks: int = 1) -> List[tuple[int, int, int]]:
        """
        Calculates all legal moves from a given state.
        
        This method is used by all search-based solvers (BFS, bidirectional BFS, etc.)
        to enumerate possible moves from the current state. The recursive solver
        doesn't use this as it constructs moves directly.
        
        Args:
            current_state: The current Hanoi state to generate moves from.
            max_liftable_disks: The maximum number of disks that can be lifted at once.
            
        Returns:
            A list of tuples (from_peg, to_peg, num_disks) representing all legal moves.
        """
        moves = []
        num_pegs = len(current_state.pegs)
        
        for i in range(num_pegs):
            source_peg_idx = i
            source_tower = current_state.pegs[source_peg_idx]

            if not source_tower:
                continue
            
            for j in range(num_pegs):
                if i == j:
                    continue
                
                target_peg_idx = j
                target_tower = current_state.pegs[target_peg_idx]

                for k in range(1, 1 + min(max_liftable_disks, len(source_tower))):
                    disks_to_lift = source_tower[-k:]
                    
                    if not target_tower or disks_to_lift[0] < target_tower[-1]:
                        moves.append((source_peg_idx + 1, target_peg_idx + 1, k))
                        
        return moves
    
    def get_stats(self) -> dict:
        """
        Get statistics about the last solve operation.
        
        Returns:
            Dictionary containing performance statistics
        """
        if self._stats_start_time is None or self._stats_end_time is None:
            return {}
        
        return {
            'solve_time': self._stats_end_time - self._stats_start_time,
            'solution_length': self._stats_solution_length,
            'nodes_explored': self._stats_nodes_explored,
            'nodes_generated': self._stats_nodes_generated,
            'max_data_structure_size': self._stats_max_data_structure_size,
            'iterations': self._stats_iterations,
            'cutoff_bounds': self._stats_cutoff_bounds.copy() if self._stats_cutoff_bounds else []
        }
    
 