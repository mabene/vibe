# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Performance display and analysis for Hanoi solver results.

This module provides functions for displaying performance metrics,
search statistics, and comparative analysis of different solving algorithms.
"""

from typing import List, Optional, Any, Dict
from output.utils.table_formatting import print_table

def display_search_statistics(
    solve_time: float,
    solution_length: int,
    nodes_explored: int,
    nodes_generated: int,
    max_data_structure_size: int,
    iterations: int,
    cutoff_bounds: Optional[List[Any]] = None
) -> None:
    """
    Display comprehensive search statistics for a single algorithm run.
    
    Args:
        solve_time: Time taken to solve the puzzle (in seconds).
        solution_length: Number of moves in the solution found.
        nodes_explored: Total number of nodes explored during search.
        nodes_generated: Total number of nodes generated during search.
        max_data_structure_size: Maximum size of the main data structure.
        iterations: Number of iterations (relevant for iterative algorithms).
        cutoff_bounds: List of cutoff bounds used (for iterative deepening algorithms).
    """
    print(f"\n--- Search Statistics ---")
    print(f"Solution found in {solve_time:.4f} seconds")
    print(f"Solution length: {solution_length} moves")
    print(f"Nodes explored: {nodes_explored:,}")
    print(f"Nodes generated: {nodes_generated:,}")
    print(f"Max data structure size: {max_data_structure_size:,}")
    
    if iterations > 0:
        print(f"Iterations: {iterations}")
    
    if cutoff_bounds:
        print(f"Cutoff bounds: {cutoff_bounds}")
    
    # Calculate efficiency metrics
    if nodes_explored > 0:
        efficiency = (solution_length / nodes_explored) * 100
        print(f"Search efficiency: {efficiency:.4f}% (moves/nodes explored)")
    
    if nodes_generated > 0:
        branching_factor = nodes_generated / max(nodes_explored, 1)
        print(f"Effective branching factor: {branching_factor:.2f}")

def display_performance_comparison(results: List[Dict[str, Any]]) -> None:
    """
    Display a comparison table of multiple algorithm results.
    
    Args:
        results: List of result dictionaries, each containing algorithm performance data.
    """
    if not results:
        print("No results to display.")
        return
    
    print(f"\n--- Performance Comparison ---")
    
    # Prepare table data
    headers = [
        "Algorithm",
        "Time (s)",
        "Moves",
        "Nodes Explored",
        "Nodes Generated",
        "Max Data Size",
        "Iterations"
    ]
    
    rows = []
    for result in results:
        # Handle potential missing keys with defaults
        row = [
            result.get('algorithm', 'Unknown'),
            f"{result.get('solve_time', 0):.4f}",
            str(result.get('solution_length', 0)),
            f"{result.get('nodes_explored', 0):,}",
            f"{result.get('nodes_generated', 0):,}",
            f"{result.get('max_data_structure_size', 0):,}",
            str(result.get('iterations', 0))
        ]
        rows.append(row)
    
    # Create and display table
    print_table(headers, rows)
    
    # Add analysis
    _display_performance_analysis(results)

def _display_performance_analysis(results: List[Dict[str, Any]]) -> None:
    """
    Display analysis of performance comparison results.
    
    Args:
        results: List of result dictionaries containing performance data.
    """
    if len(results) < 2:
        return
    
    print(f"\n--- Performance Analysis ---")
    
    # Find fastest algorithm
    fastest = min(results, key=lambda r: r.get('solve_time', float('inf')))
    print(f"Fastest algorithm: {fastest.get('algorithm', 'Unknown')} "
          f"({fastest.get('solve_time', 0):.4f}s)")
    
    # Find most efficient (fewest nodes explored)
    most_efficient = min(results, key=lambda r: r.get('nodes_explored', float('inf')))
    print(f"Most efficient: {most_efficient.get('algorithm', 'Unknown')} "
          f"({most_efficient.get('nodes_explored', 0):,} nodes explored)")
    
    # Find shortest solution
    shortest = min(results, key=lambda r: r.get('solution_length', float('inf')))
    print(f"Shortest solution: {shortest.get('algorithm', 'Unknown')} "
          f"({shortest.get('solution_length', 0)} moves)")
    
    # Calculate speedup ratios
    if len(results) > 1:
        slowest = max(results, key=lambda r: r.get('solve_time', 0))
        speedup = slowest.get('solve_time', 0) / fastest.get('solve_time', 1)
        print(f"Speed improvement: {speedup:.2f}x faster than slowest")

def display_algorithm_details(algorithm_name: str, result: Dict[str, Any]) -> None:
    """
    Display detailed information about a specific algorithm's performance.
    
    Args:
        algorithm_name: Name of the algorithm.
        result: Dictionary containing the algorithm's performance data.
    """
    print(f"\n--- {algorithm_name} Details ---")
    
    # Basic metrics
    print(f"Execution time: {result.get('solve_time', 0):.4f} seconds")
    print(f"Solution length: {result.get('solution_length', 0)} moves")
    print(f"Nodes explored: {result.get('nodes_explored', 0):,}")
    print(f"Nodes generated: {result.get('nodes_generated', 0):,}")
    print(f"Maximum data structure size: {result.get('max_data_structure_size', 0):,}")
    
    # Algorithm-specific metrics
    if result.get('iterations', 0) > 0:
        print(f"Iterations performed: {result.get('iterations', 0)}")
    
    if result.get('cutoff_bounds'):
        print(f"Cutoff bounds used: {result.get('cutoff_bounds')}")
    
    # Efficiency calculations
    nodes_explored = result.get('nodes_explored', 0)
    if nodes_explored > 0:
        efficiency = (result.get('solution_length', 0) / nodes_explored) * 100
        print(f"Search efficiency: {efficiency:.4f}% (solution moves / nodes explored)")
    
    nodes_generated = result.get('nodes_generated', 0)
    if nodes_generated > 0:
        branching_factor = nodes_generated / max(nodes_explored, 1)
        print(f"Effective branching factor: {branching_factor:.2f}")
 