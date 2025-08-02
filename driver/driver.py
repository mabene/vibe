# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

import threading
import time
from typing import List, Optional, Dict, Any, Tuple
from solvers.hanoi_state import HanoiState
from .profiler import PerformanceProfiler
from solvers import (
    ClosedFormSolver, 
    GeneralBFSSolver, 
    DFSSolver, 
    IterativeDeepeningSolver,
    AStarSolver,
    IDAStarSolver,
    GreedyBestFirstSolver,
    BidirectionalBFSSolver,
    ParallelBidirectionalBFSSolver
)


class HanoiDriver:
    """Main driver that orchestrates solving Tower of Hanoi puzzles."""
    
    # Algorithm registry
    ALGORITHMS = {
        'BFS': {'class': GeneralBFSSolver, 'name': 'Breadth-First Search'},
        'DFS': {'class': DFSSolver, 'name': 'Depth-First Search'},
        'IDE': {'class': IterativeDeepeningSolver, 'name': 'Iterative Deepening'},
        'ASTAR': {'class': AStarSolver, 'name': 'A* with heuristic'},
        'IDASTAR': {'class': IDAStarSolver, 'name': 'Iterative Deepening A*'},
        'GBFS': {'class': GreedyBestFirstSolver, 'name': 'Greedy Best-First Search'},
        'BIBFS': {'class': BidirectionalBFSSolver, 'name': 'Bidirectional BFS'},
        'PBIBFS': {'class': ParallelBidirectionalBFSSolver, 'name': 'Parallel Bidirectional BFS'},
        'CFORM': {'class': ClosedFormSolver, 'name': 'Closed Form'}
    }
    
    def __init__(self, initial_state: HanoiState, target_state: HanoiState):
        """
        Initialize the driver with start and end states.
        
        Args:
            initial_state: The HanoiState from which to start the search
            target_state: The HanoiState to reach
        """
        self.initial_state = initial_state
        self.target_state = target_state
        
    def solve_with_algorithm(self, max_lift: int = 1, algorithm: Optional[str] = None, 
              profile: Optional[int] = None, timeout: int = 30) -> List[Tuple[int, int, int]]:
        """
        Solve the Tower of Hanoi puzzle using the specified algorithm or auto-select.
        
        Args:
            max_lift: The maximum number of disks that can be lifted at once (default 1)
            algorithm: The algorithm to use. If None, auto-selects based on puzzle type.
                      Special value 'COMPARE' runs all applicable algorithms.
            profile: Enable detailed profiling and statistics collection.
                    If > 1, runs multiple instances for comparison.
            timeout: Timeout in seconds for individual algorithm execution (default 30)
            
        Returns:
            A list of tuples representing the solution moves.
            
        Raises:
            ValueError: If an invalid algorithm is specified
            RuntimeError: If the algorithm fails or times out
        """
        # Handle comparison mode
        if algorithm == 'COMPARE':
            from .comparator import AlgorithmComparator
            comparator = AlgorithmComparator(self)
            
            if profile is not None and profile > 1:
                return comparator.compare_multiple_instances(profile, max_lift, timeout)
            else:
                return comparator.compare_algorithms(max_lift, timeout)
        
        # Handle specific algorithm
        if algorithm is not None:
            return self._solve_with_algorithm(algorithm, max_lift, profile, timeout)
        
        # Auto-select algorithm
        selected_algorithm = self._auto_select_algorithm(max_lift)
        return self._solve_with_algorithm(selected_algorithm, max_lift, profile, timeout)
    
    def _solve_with_algorithm(self, algorithm: str, max_lift: int, 
                             profile: Optional[int], timeout: int) -> List[Tuple[int, int, int]]:
        """
        Solve the puzzle using the specified algorithm.
        
        Args:
            algorithm: The algorithm to use
            max_lift: The maximum number of disks that can be lifted at once
            profile: Enable detailed profiling and statistics collection
            timeout: Timeout in seconds for algorithm execution
            
        Returns:
            A list of tuples representing the solution moves
        """
        if not self._validate_algorithm(algorithm):
            raise ValueError(f"Unknown algorithm: {algorithm}")
            
        solver_class = self.ALGORITHMS[algorithm]['class']
        algorithm_name = self.ALGORITHMS[algorithm]['name']
        
        if profile is not None:
            print(f"\n--- Using {algorithm_name} solver. ---")
        
        # Execute with timeout
        result = self.execute_with_timeout(algorithm, solver_class, algorithm_name, max_lift, timeout)
        
        if result.get('timeout', False):
            raise RuntimeError(f"{algorithm_name} timed out after {timeout} seconds")
        elif not result.get('success', False):
            raise RuntimeError(f"{algorithm_name} failed: {result.get('error', 'Unknown error')}")
        
        return result['solution']
    
    def execute_with_timeout(self, algorithm: str, solver_class, algorithm_name: str, 
                           max_lift: int, timeout: int, quiet: bool = False) -> Dict[str, Any]:
        """
        Execute an algorithm with timeout support.
        
        Args:
            algorithm: Short algorithm name
            solver_class: The solver class to instantiate
            algorithm_name: Full algorithm name for display
            max_lift: Maximum number of disks that can be lifted at once
            timeout: Timeout in seconds
            quiet: If True, suppress progress output during algorithm execution
            
        Returns:
            Dictionary with algorithm results or timeout/error status
        """
        result: Dict[str, Any] = {'algorithm': algorithm, 'full_name': algorithm_name}
        solver_instance = None  # Keep reference to solver for timeout case
        
        def run_algorithm():
            nonlocal solver_instance
            try:
                # Create solver
                solver_instance = solver_class(self.initial_state, self.target_state)
                
                start_time = time.perf_counter()
                
                # Execute algorithm
                if algorithm == 'CFORM':
                    solution = solver_instance._solve_internal()
                elif algorithm in ['IDE', 'IDASTAR']:
                    # Only pass quiet parameter to iterative algorithms that support it
                    solution = solver_instance._solve_internal(max_liftable_disks=max_lift, quiet=quiet)
                else:
                    solution = solver_instance._solve_internal(max_liftable_disks=max_lift)
                
                end_time = time.perf_counter()
                solve_time = end_time - start_time
                
                # Basic results
                result['success'] = True
                result['solution'] = solution
                result['solve_time'] = solve_time
                result['solution_length'] = len(solution)
                
                # Collect solver statistics using centralized method
                solver_stats = PerformanceProfiler.collect_solver_statistics(solver_instance)
                result.update(solver_stats)
                
                # Calculate efficiency (ratio of explored to generated nodes)
                nodes_explored = result.get('nodes_explored', 0)
                nodes_generated = result.get('nodes_generated', 0)
                result['efficiency'] = self.calculate_efficiency(nodes_explored, nodes_generated)
                
            except Exception as e:
                result['success'] = False
                result['error'] = str(e)
        
        # Run algorithm in a separate thread with timeout
        thread = threading.Thread(target=run_algorithm)
        thread.daemon = True  # Dies when main thread dies
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Algorithm timed out - collect partial statistics from solver if available
            result['success'] = False
            result['timeout'] = True
            result['error'] = f'Timed out after {timeout} seconds'
            
            # Try to collect partial statistics from the solver instance
            if solver_instance is not None:
                try:
                    solver_stats = PerformanceProfiler.collect_solver_statistics(solver_instance)
                    result.update(solver_stats)
                except Exception:
                    # If we can't collect stats, just continue with timeout result
                    pass
        
        return result
    
    @staticmethod
    def generate_puzzle_states(num_disks: int, mode: str) -> Tuple[HanoiState, HanoiState]:
        """
        Generate initial and target states for a puzzle.
        
        Args:
            num_disks: Number of disks in the puzzle
            mode: 'classic' or 'random'
            
        Returns:
            Tuple of (initial_state, target_state)
        """
        if mode == 'classic':
            initial_state = HanoiState.classic_init(num_disks, on_peg=1)
            target_state = HanoiState.classic_init(num_disks, on_peg=3)
        else:  # mode == 'random'
            initial_state = HanoiState.random_init(num_disks)
            target_state = HanoiState.random_init(num_disks)
            while initial_state == target_state:
                target_state = HanoiState.random_init(num_disks)
        
        return initial_state, target_state
    
    @staticmethod
    def calculate_efficiency(nodes_explored: int, nodes_generated: int) -> float:
        """
        Calculate search efficiency as the ratio of explored to generated nodes.
        
        Args:
            nodes_explored: Number of nodes explored during search
            nodes_generated: Number of nodes generated during search
            
        Returns:
            Efficiency percentage (0-100)
        """
        return (nodes_explored / nodes_generated) * 100 if nodes_generated > 0 else 0
    
    @staticmethod
    def validate_solution(solution: List[Tuple[int, int, int]], 
                         initial_state: HanoiState, target_state: HanoiState) -> bool:
        """
        Validate that a solution is correct for given states.
        
        Args:
            solution: List of moves to validate
            initial_state: Starting state
            target_state: Target state
            
        Returns:
            True if solution is valid, False otherwise
        """
        try:
            test_state = initial_state
            for from_peg, to_peg, num_disks in solution:
                test_state = test_state.apply_move(from_peg, to_peg, num_disks)
            return test_state == target_state
        except Exception:
            return False
    
    def _auto_select_algorithm(self, max_lift: int) -> str:
        """
        Auto-select the most appropriate algorithm based on puzzle characteristics.
        
        Args:
            max_lift: Maximum number of disks that can be lifted at once
            
        Returns:
            Algorithm name to use
        """
        if self._is_classical_puzzle() and max_lift == 1:
            return 'CFORM'
        else:
            return 'BFS'
    
    def _is_classical_puzzle(self) -> bool:
        """
        Check if the puzzle is a classical Tower of Hanoi puzzle.
        
        Returns:
            True if it's a classical puzzle, False otherwise
        """
        initial_peg = self.initial_state.get_classical_peg_if_any()
        target_peg = self.target_state.get_classical_peg_if_any()
        
        return (
            initial_peg is not None and
            target_peg is not None and
            initial_peg != target_peg and
            self.initial_state.number_of_disks == self.target_state.number_of_disks
        )
    
    def _validate_algorithm(self, algorithm: str) -> bool:
        """
        Validate that an algorithm is supported.
        
        Args:
            algorithm: Algorithm name to validate
            
        Returns:
            True if algorithm is supported, False otherwise
        """
        return algorithm in self.ALGORITHMS 