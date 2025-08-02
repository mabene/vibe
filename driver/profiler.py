# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Performance profiling utilities for the Hanoi solver.

This module provides tools for measuring and analyzing the performance of
different solving algorithms, including execution time, memory usage, and
search space exploration statistics.
"""

from typing import Dict, Any, Optional, List

import time
import gc
from solvers.base_solver import BaseSolver

class PerformanceMetrics:
    """Container for performance metrics collected during solving."""
    
    def __init__(self, solve_time: float, solution_length: int, nodes_explored: int, 
                 nodes_generated: int, max_data_structure_size: int, iterations: int,
                 cutoff_bounds: Optional[List[Any]] = None, memory_usage: Optional[float] = None):
        """Initialize performance metrics with validation."""
        self.solve_time = solve_time
        self.solution_length = solution_length
        self.nodes_explored = nodes_explored
        self.nodes_generated = nodes_generated
        self.max_data_structure_size = max_data_structure_size
        self.iterations = iterations
        self.cutoff_bounds = cutoff_bounds
        self.memory_usage = memory_usage
        
        # Validate metrics after initialization
        if self.solve_time < 0:
            raise ValueError("Solve time cannot be negative")
        if self.solution_length < 0:
            raise ValueError("Solution length cannot be negative")
        if self.nodes_explored < 0:
            raise ValueError("Nodes explored cannot be negative")
        if self.nodes_generated < 0:
            raise ValueError("Nodes generated cannot be negative")

class PerformanceProfiler:
    """
    Profiler for collecting and analyzing solver performance metrics.
    
    This class provides utilities for measuring various aspects of solver
    performance, including execution time, memory usage, and search statistics.
    """
    
    @staticmethod
    def collect_solver_statistics(solver: BaseSolver) -> Dict[str, Any]:
        """
        Collect comprehensive statistics from a solver instance.
        
        Args:
            solver: The solver instance to collect statistics from.
            
        Returns:
            Dictionary containing all available statistics.
        """
        if hasattr(solver, 'get_stats'):
            solver_stats = solver.get_stats()
        else:
            solver_stats = {}
        
        # Add basic statistics that all solvers should have
        basic_stats = {
            'nodes_explored': getattr(solver, '_stats_nodes_explored', 0),
            'nodes_generated': getattr(solver, '_stats_nodes_generated', 0),
            'iterations': getattr(solver, '_stats_iterations', 0),
            'cutoff_bounds': getattr(solver, '_stats_cutoff_bounds', None)
        }
        
        # Handle max_data_structure_size - prefer upper bound if available
        if 'max_data_structure_size_upper_bound' in solver_stats:
            basic_stats['max_data_structure_size_upper_bound'] = solver_stats['max_data_structure_size_upper_bound']
        else:
            basic_stats['max_data_structure_size'] = getattr(solver, '_stats_max_data_structure_size', 0)
        
        # Merge solver-specific stats with basic stats
        solver_stats.update(basic_stats)
        
        return solver_stats
    
    @staticmethod
    def create_performance_metrics(
        solve_time: float,
        solution_length: int,
        solver: BaseSolver
    ) -> PerformanceMetrics:
        """
        Create a PerformanceMetrics object from solver data.
        
        Args:
            solve_time: Time taken to solve the puzzle.
            solution_length: Length of the solution found.
            solver: The solver instance to extract statistics from.
            
        Returns:
            PerformanceMetrics object with all collected data.
        """
        stats = PerformanceProfiler.collect_solver_statistics(solver)
        
        return PerformanceMetrics(
            solve_time=solve_time,
            solution_length=solution_length,
            nodes_explored=stats.get('nodes_explored', 0),
            nodes_generated=stats.get('nodes_generated', 0),
            max_data_structure_size=stats.get('max_data_structure_size', 0),
            iterations=stats.get('iterations', 0),
            cutoff_bounds=stats.get('cutoff_bounds'),
            memory_usage=None  # Could be implemented later
        )
    
    @staticmethod
    def format_performance_summary(metrics: PerformanceMetrics) -> str:
        """
        Format performance metrics into a readable summary.
        
        Args:
            metrics: The performance metrics to format.
            
        Returns:
            Formatted string containing the performance summary.
        """
        lines = [
            f"Performance Summary:",
            f"  Solve Time: {metrics.solve_time:.4f} seconds",
            f"  Solution Length: {metrics.solution_length} moves",
            f"  Nodes Explored: {metrics.nodes_explored:,}",
            f"  Nodes Generated: {metrics.nodes_generated:,}",
            f"  Max Data Structure Size: {metrics.max_data_structure_size:,}",
            f"  Iterations: {metrics.iterations:,}"
        ]
        
        if metrics.cutoff_bounds:
            lines.append(f"  Cutoff Bounds: {metrics.cutoff_bounds}")
        
        if metrics.memory_usage:
            lines.append(f"  Memory Usage: {metrics.memory_usage:.2f} MB")
        
        return "\n".join(lines)
    
    @staticmethod
    def compare_metrics(metrics_list: List[PerformanceMetrics], 
                       algorithm_names: List[str]) -> str:
        """
        Compare multiple performance metrics and generate a comparison report.
        
        Args:
            metrics_list: List of performance metrics to compare.
            algorithm_names: List of algorithm names corresponding to metrics.
            
        Returns:
            Formatted comparison report.
        """
        if len(metrics_list) != len(algorithm_names):
            raise ValueError("Number of metrics must match number of algorithm names")
        
        lines = ["Performance Comparison:"]
        lines.append("-" * 60)
        
        # Header
        lines.append(f"{'Algorithm':<20} {'Time (s)':<12} {'Moves':<8} {'Nodes Exp':<12} {'Nodes Gen':<12}")
        lines.append("-" * 60)
        
        # Data rows
        for i, (metrics, name) in enumerate(zip(metrics_list, algorithm_names)):
            lines.append(
                f"{name:<20} {metrics.solve_time:<12.4f} {metrics.solution_length:<8} "
                f"{metrics.nodes_explored:<12,} {metrics.nodes_generated:<12,}"
            )
        
        return "\n".join(lines) 