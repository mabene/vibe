# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Algorithm comparator for the Hanoi project.

This module provides functionality to compare different algorithms across single
or multiple instances, displaying results in formatted tables.
"""

import threading
import time
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .profiler import PerformanceProfiler
from solvers.hanoi_state import HanoiState
from output.profiling_and_comparing import (
    display_single_instance_comparison,
    display_multi_instance_comparison,
)

if TYPE_CHECKING:
    from driver import HanoiDriver


class AlgorithmComparator:
    """Handles running multiple algorithms and comparing their performance."""
    
    def __init__(self, driver: 'HanoiDriver'):
        """
        Initialize the algorithm comparator.
        
        Args:
            driver: The HanoiDriver instance to use for algorithm execution
        """
        self.driver = driver
        
    def compare_algorithms(self, max_lift: int, timeout: int = 30) -> List[Tuple[int, int, int]]:
        """
        Compare all applicable algorithms on a single instance.
        
        Args:
            max_lift: Maximum number of disks that can be lifted at once
            timeout: Timeout in seconds for individual algorithms
            
        Returns:
            The optimal solution from the best performing algorithm
        """
        print("\n--- ALGORITHM COMPARISON MODE ---")
        print("Running all applicable algorithms...\n")
        
        # Get applicable algorithms
        algorithms_to_test = self._get_applicable_algorithms(max_lift)
        
        # Run each algorithm
        results = []
        for short_name, solver_class, full_name in algorithms_to_test:
            print(f"Running {full_name}...")
            
            # Execute algorithm with timeout
            result = self.driver.execute_with_timeout(
                short_name, solver_class, full_name, max_lift, timeout, quiet=True
            )
            
            # Add algorithm info
            result['algorithm'] = short_name
            
            if result.get('success', False):
                # Validate solution
                if not self.driver.validate_solution(result['solution'], self.driver.initial_state, self.driver.target_state):
                    result['success'] = False
                    result['error'] = 'Invalid solution returned'
                    
                print(f"  ✓ Completed in {result['solve_time']:.4f}s")
            else:
                if result.get('timeout', False):
                    print(f"  ⏰ Timed out after {timeout}s")
                else:
                    print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
                    
            results.append(result)
        
        # Display results
        display_single_instance_comparison(results)
        
        # Return best solution
        successful_results = [r for r in results if r.get('success', False)]
        if successful_results:
            best_result = min(successful_results, key=lambda x: x['solve_time'])
            return best_result['solution']
        else:
            raise RuntimeError("No algorithms completed successfully")
    
    def compare_multiple_instances(self, num_instances: int, max_lift: int, timeout: int = 30) -> List[Tuple[int, int, int]]:
        """
        Compare algorithms across multiple puzzle instances.
        
        Args:
            num_instances: Number of instances to run
            max_lift: Maximum number of disks that can be lifted at once
            timeout: Timeout in seconds for individual algorithms
            
        Returns:
            The optimal solution from the best performing algorithm
        """
        print(f"\n--- ALGORITHM COMPARISON MODE ({num_instances} instances) ---")
        print("Running all applicable algorithms across multiple instances...\n")
        
        # Get applicable algorithms
        algorithms_to_test = self._get_applicable_algorithms(max_lift)
        
        # Store results for each algorithm across all instances
        algorithm_results = {}
        
        # Generate puzzle instances
        puzzle_instances = self._generate_puzzle_instances(num_instances)
        
        # Run each algorithm on all instances
        for short_name, solver_class, full_name in algorithms_to_test:
            print(f"Running {full_name} across {num_instances} instances...")
            
            algorithm_results[short_name] = {
                'full_name': full_name,
                'times': [],
                'timeout_times': [],
                'solution_lengths': [],
                'nodes_explored': [],
                'nodes_generated': [],
                'max_data_structures': [],
                'iterations': [],
                'solutions': [],
                'success': True,
                'failed_instances': 0,
                'timeout_instances': 0,
                'timeout_duration': timeout,
                'has_upper_bound': False
            }
            
            for instance_idx, (initial_state, target_state) in enumerate(puzzle_instances):
                try:
                    # Create temporary driver for this instance
                    temp_driver = self.driver.__class__(initial_state, target_state)
                    
                    # Execute algorithm
                    result = temp_driver.execute_with_timeout(
                        short_name, solver_class, full_name, max_lift, timeout, quiet=True
                    )
                    
                    if result.get('success', False):
                        # Validate solution
                        if self.driver.validate_solution(result['solution'], initial_state, target_state):
                            # Store results
                            algorithm_results[short_name]['times'].append(result['solve_time'])
                            algorithm_results[short_name]['solution_lengths'].append(len(result['solution']))
                            algorithm_results[short_name]['nodes_explored'].append(result.get('nodes_explored', 0))
                            algorithm_results[short_name]['nodes_generated'].append(result.get('nodes_generated', 0))
                            # Handle both regular max_data_structure_size and upper bounds
                            if 'max_data_structure_size_upper_bound' in result:
                                algorithm_results[short_name]['max_data_structures'].append(result['max_data_structure_size_upper_bound'])
                                algorithm_results[short_name]['has_upper_bound'] = True
                            else:
                                algorithm_results[short_name]['max_data_structures'].append(result.get('max_data_structure_size', 0))
                            algorithm_results[short_name]['iterations'].append(result.get('iterations', 0))
                            algorithm_results[short_name]['solutions'].append(result['solution'])
                        else:
                            algorithm_results[short_name]['failed_instances'] += 1
                    elif result.get('timeout', False):
                        # Handle timeout - include timeout duration in timing
                        algorithm_results[short_name]['timeout_instances'] += 1
                        algorithm_results[short_name]['timeout_times'].append(timeout)
                        # Don't add solution data for timeouts, but keep tracking
                    else:
                        # Other failures (errors, etc.)
                        algorithm_results[short_name]['failed_instances'] += 1
                        
                except Exception as e:
                    algorithm_results[short_name]['failed_instances'] += 1
            
            # Check if algorithm completely failed
            total_failures = algorithm_results[short_name]['failed_instances'] + algorithm_results[short_name]['timeout_instances']
            if total_failures >= num_instances:
                algorithm_results[short_name]['success'] = False
                print(f"  ❌ Failed on all instances")
            else:
                success_rate = (num_instances - total_failures) / num_instances
                # Calculate average time including timeouts
                all_times = algorithm_results[short_name]['times'] + algorithm_results[short_name]['timeout_times']
                avg_time = sum(all_times) / len(all_times) if all_times else 0
                print(f"  ✓ Completed {success_rate:.1%} instances, avg time: {avg_time:.4f}s")
        
        # Display results
        display_multi_instance_comparison(algorithm_results, num_instances)
        
        # Return best solution
        successful_algorithms = {name: results for name, results in algorithm_results.items() 
                               if results['success'] and results['solutions']}
        
        if successful_algorithms:
            # Find fastest algorithm on average (considering only successful instances)
            fastest_algorithm = min(successful_algorithms.items(), 
                                  key=lambda x: sum(x[1]['times']) / len(x[1]['times']) if x[1]['times'] else float('inf'))
            return fastest_algorithm[1]['solutions'][0]  # Return first solution from best algorithm
        else:
            raise RuntimeError("No algorithms completed successfully")
    
    def _get_applicable_algorithms(self, max_lift: int) -> List[Tuple[str, Any, str]]:
        """
        Get list of applicable algorithms based on puzzle characteristics.
        
        Args:
            max_lift: Maximum number of disks that can be lifted at once
            
        Returns:
            List of tuples (short_name, solver_class, full_name)
        """
        # Use the canonical algorithm registry from HanoiDriver
        algorithms_to_test = []
        
        for short_name, algorithm_info in self.driver.ALGORITHMS.items():
            # Skip CFORM unless it's applicable
            if short_name == 'CFORM':
                if self.driver._is_classical_puzzle() and max_lift == 1:
                    algorithms_to_test.append((short_name, algorithm_info['class'], algorithm_info['name']))
            else:
                algorithms_to_test.append((short_name, algorithm_info['class'], algorithm_info['name']))
        
        return algorithms_to_test
    
    def _generate_puzzle_instances(self, num_instances: int) -> List[Tuple[HanoiState, HanoiState]]:
        """
        Generate puzzle instances for multi-instance comparison.
        
        Args:
            num_instances: Number of instances to generate
            
        Returns:
            List of (initial_state, target_state) tuples
        """
        puzzle_instances = []
        num_disks = self.driver.initial_state.number_of_disks
        
        for i in range(num_instances):
            if self.driver._is_classical_puzzle():
                # For classical puzzles, all instances are the same
                puzzle_instances.append((self.driver.initial_state, self.driver.target_state))
            else:
                # For random puzzles, generate new instances using driver's method
                initial, target = self.driver.generate_puzzle_states(num_disks, 'random')
                puzzle_instances.append((initial, target))
        
        return puzzle_instances