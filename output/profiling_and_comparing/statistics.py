# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Aggregate statistics display functions.

This module provides functions to display aggregate statistics from multiple
puzzle instances, including variance analysis and performance comparisons.
"""

import math
import statistics
from typing import List, Dict, Any, Optional

from ..solution import display_fastest_solution_details


def display_aggregate_statistics(all_results: List[Dict[str, Any]], mode: str, num_disks: int, 
                                profile_enabled: bool = False, show_moves_condition: bool = False):
    """
    Calculate and display aggregate statistics from multiple puzzle instances.
    
    Args:
        all_results: List of result dictionaries from each instance
        mode: The type of puzzle ('classic' or 'random')
        num_disks: The number of disks in the puzzle
        profile_enabled: Whether profiling is enabled
        show_moves_condition: Whether to show moves for the fastest solution
    """
    num_instances = len(all_results)
    
    # Extract timing and solution length data
    times = [r['elapsed_time'] for r in all_results]
    lengths = [r['solution_length'] for r in all_results]
    
    # Calculate statistics
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    avg_length = sum(lengths) / len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    
    # Display results
    print(f"\n{'='*80}")
    print(f"📊 AGGREGATE STATISTICS ({num_instances} instances)")
    print(f"{'='*80}")
    
    # Timing statistics
    if min_time == max_time:
        print(f"⏱️  Average Time:         {avg_time:.4f}s")
    else:
        print(f"⏱️  Average Time:         {avg_time:.4f}s [{min_time:.4f}s-{max_time:.4f}s]")
    
    # Solution length statistics
    if min_length == max_length:
        print(f"📏 Average Moves:        {avg_length:.1f}")
    else:
        print(f"📏 Average Moves:        {avg_length:.1f} [{min_length}-{max_length}]")
    
    # Show consistency metrics
    time_variance = max_time - min_time if max_time != min_time else 0
    length_variance = max_length - min_length if max_length != min_length else 0
    
    if time_variance > 0:
        time_cv = (time_variance / avg_time) * 100
        print(f"📈 Time Variability:     {time_cv:.1f}% (range: {time_variance:.4f}s)")
    
    if length_variance > 0:
        print(f"📊 Solution Variability: {length_variance} moves difference")
    
    print(f"{'='*80}")
    
    # Show solution for the fastest instance if profiling is enabled
    if profile_enabled:
        fastest_instance = min(all_results, key=lambda x: x['elapsed_time'])
        display_fastest_solution_details(fastest_instance, show_moves_condition)


def calculate_statistics_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics from a list of results.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Dictionary containing summary statistics
    """
    if not results:
        return {}
    
    times = [r['elapsed_time'] for r in results]
    lengths = [r['solution_length'] for r in results]
    
    return {
        'count': len(results),
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'avg_moves': sum(lengths) / len(lengths),
        'min_moves': min(lengths),
        'max_moves': max(lengths),
        'time_variance': max(times) - min(times) if len(times) > 1 else 0,
        'move_variance': max(lengths) - min(lengths) if len(lengths) > 1 else 0
    }


def display_statistics_comparison(stats1: Dict[str, Any], stats2: Dict[str, Any], 
                                 label1: str, label2: str):
    """
    Display a comparison between two sets of statistics.
    
    Args:
        stats1: First set of statistics
        stats2: Second set of statistics
        label1: Label for the first set
        label2: Label for the second set
    """
    print(f"\n📊 COMPARISON: {label1} vs {label2}")
    print("=" * 60)
    
    print(f"{'Metric':<20} {'|':<2} {label1:<15} {'|':<2} {label2:<15}")
    print("-" * 60)
    
    print(f"{'Instances':<20} {'|':<2} {stats1.get('count', 0):<15} {'|':<2} {stats2.get('count', 0):<15}")
    print(f"{'Avg Time (s)':<20} {'|':<2} {stats1.get('avg_time', 0):.4f}{'s':<10} {'|':<2} {stats2.get('avg_time', 0):.4f}{'s':<10}")
    print(f"{'Avg Moves':<20} {'|':<2} {stats1.get('avg_moves', 0):.1f}{'moves':<10} {'|':<2} {stats2.get('avg_moves', 0):.1f}{'moves':<10}")
    
    if stats1.get('time_variance', 0) > 0 or stats2.get('time_variance', 0) > 0:
        print(f"{'Time Range (s)':<20} {'|':<2} {stats1.get('time_variance', 0):.4f}{'s':<10} {'|':<2} {stats2.get('time_variance', 0):.4f}{'s':<10}")
    
    if stats1.get('move_variance', 0) > 0 or stats2.get('move_variance', 0) > 0:
        print(f"{'Move Range':<20} {'|':<2} {stats1.get('move_variance', 0):<15} {'|':<2} {stats2.get('move_variance', 0):<15}")
    
    print("=" * 60) 