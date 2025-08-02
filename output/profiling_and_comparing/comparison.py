# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Displays algorithm comparison results in formatted tables.

This module provides functions to format and display the results of running
multiple algorithms on Tower of Hanoi puzzles, showing performance metrics
like timing, solution quality, and search efficiency.
"""

from typing import Dict, List, Any, Tuple
from output.utils import calculate_column_widths, format_time_range


def display_single_instance_comparison(results: List[Dict[str, Any]]):
    """
    Display a formatted ASCII comparison table of algorithm results from a single instance.
    
    Args:
        results: List of algorithm result dictionaries
    """
    # Prepare table data - include both successful and timed-out results
    successful_results = [r for r in results if r.get('success', False)]
    displayable_results = [r for r in results if r.get('success', False) or r.get('timeout', False)]
    
    if not displayable_results:
        print("❌ No algorithms completed or timed out!")
        return
    
    # Sort results: successful algorithms by time (ascending), then timed-out algorithms
    def sort_key(result):
        if result.get('timeout', False):
            # Timed-out algorithms go last
            return (1, result.get('solve_time', float('inf')))
        else:
            # Successful algorithms sorted by time
            return (0, result.get('solve_time', 0))
    
    displayable_results.sort(key=sort_key)
    
    # Table headers
    headers = ["Algorithm", "Time (s)", "Moves", "Explored", "Generated", "Frontier", "Efficiency", "Iterations"]
    
    # Calculate column widths
    col_widths = [max(len(h), 10) for h in headers]
    
    # Helper function to format row data
    def format_row_data(result):
        if result.get('timeout', False):
            # Extract timeout duration from error message
            timeout_duration = "30"  # default
            if 'error' in result:
                import re
                match = re.search(r'(\d+)', result['error'])
                if match:
                    timeout_duration = match.group(1)
            
            return [
                result['algorithm'][:11],
                f"timeout ({timeout_duration}s)",
                result.get('solution_length', 0) and str(result['solution_length']) or "-",
                result.get('nodes_explored', 0) and str(result['nodes_explored']) or "-",
                result.get('nodes_generated', 0) and str(result['nodes_generated']) or "-",
                result.get('max_data_structure', 0) and str(result['max_data_structure']) or "-",
                result.get('efficiency', 0) and f"{result['efficiency']:.1f}%" or "-",
                result.get('iterations', 0) and str(result['iterations']) or "-"
            ]
        else:
            return [
                result['algorithm'][:11],
                f"{result['solve_time']:.4f}",
                str(result['solution_length']),
                str(result['nodes_explored']) if result['nodes_explored'] > 0 else "-",
                str(result['nodes_generated']) if result['nodes_generated'] > 0 else "-", 
                (f"<={result['max_data_structure_size_upper_bound']}" if 'max_data_structure_size_upper_bound' in result 
                 else str(result['max_data_structure_size']) if result.get('max_data_structure_size', 0) > 0 else "-"),
                f"{result['efficiency']:.1f}%" if result['efficiency'] > 0 else "-",
                str(result['iterations']) if result['iterations'] > 0 else "-"
            ]
    
    # Calculate column widths based on all displayable results
    for result in displayable_results:
        row_data = format_row_data(result)
        for i, data in enumerate(row_data):
            col_widths[i] = max(col_widths[i], len(str(data)))
    
    # Build header row and calculate actual table width
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    table_width = len(header_row)
    
    # Print table with proper borders
    print("\n" + "="*table_width)
    print("🏆 ALGORITHM COMPARISON RESULTS")
    print("="*table_width)
    
    # Print header
    print(header_row)
    print("-" * table_width)
    
    # Print data rows (maintain original algorithm execution order)
    for result in displayable_results:
        row_data = format_row_data(result)
        row = " | ".join(str(data).ljust(col_widths[i]) for i, data in enumerate(row_data))
        print(row)
    
    print("="*table_width)
    
    # Display summary statistics
    _display_comparison_summary(successful_results, results, table_width)


def display_multi_instance_comparison(algorithm_results: Dict[str, Dict[str, Any]], num_instances: int):
    """
    Display a formatted ASCII comparison table with averaged statistics from multiple instances.
    
    Args:
        algorithm_results: Dictionary mapping algorithm names to their results across instances
        num_instances: Number of instances that were run
    """
    # Filter algorithms that ran at least some instances (not completely failed)
    displayable_algorithms = {name: results for name, results in algorithm_results.items() 
                             if results['success'] or results.get('timeout_instances', 0) > 0 or len(results['times']) > 0}
    
    if not displayable_algorithms:
        print("❌ No algorithms completed successfully!")
        return
    
    # Check if any algorithm had timeouts
    has_timeouts = any(results.get('timeout_instances', 0) > 0 for results in displayable_algorithms.values())
    
    # Table headers - add Timeouts column first if any algorithm had timeouts
    headers = ["Algorithm", "Time (s)", "Moves", "Generated", "Explored", "Ratio", "Frontier", "Iterations"]
    if has_timeouts:
        headers.insert(1, "Timeouts")  # Insert right after "Algorithm"
    
    # Calculate column widths
    col_widths = [max(len(h), 10) for h in headers]
    
    # Calculate statistics for each algorithm
    processed_results = []
    for name, results in displayable_algorithms.items():
        # Get successful and timeout times separately
        successful_times = results['times']
        timeout_times = results.get('timeout_times', [])
        timeout_count = results.get('timeout_instances', 0)
        
        # All times combined for overall timing statistics
        all_times = successful_times + timeout_times
        
        # Solution-dependent statistics (successful runs only)
        successful_lengths = results['solution_lengths']
        explored = [x for x in results['nodes_explored'] if x > 0]
        generated = [x for x in results['nodes_generated'] if x > 0]
        iterations = [x for x in results['iterations'] if x > 0]
        max_ds = [x for x in results['max_data_structures'] if x > 0]
        
        # Format time with range (including timeouts)
        if successful_times:
            # Has some successful runs - show time range including any timeouts
            time_str = format_time_range(all_times)
        else:
            # No successful runs (all timeouts/failures) - show dash
            time_str = "-"
        
        # Format moves with range (successful runs only)
        if successful_lengths:
            avg_moves = sum(successful_lengths) / len(successful_lengths)
            if len(successful_lengths) > 1 and min(successful_lengths) != max(successful_lengths):
                moves_str = f"{avg_moves:.1f} [{min(successful_lengths)}-{max(successful_lengths)}]"
            else:
                moves_str = f"{avg_moves:.1f}"
        else:
            moves_str = "-"
        
        # Format other statistics
        explored_str = f"{sum(explored) / len(explored):.0f}" if explored else "-"
        generated_str = f"{sum(generated) / len(generated):.0f}" if generated else "-"
        # Handle upper bounds vs regular max DS size
        if results.get('has_upper_bound', False) and max_ds:
            max_ds_str = f"<={sum(max_ds) / len(max_ds):.0f}"
        else:
            max_ds_str = f"{sum(max_ds) / len(max_ds):.0f}" if max_ds else "-"
        iterations_str = f"{sum(iterations) / len(iterations):.0f}" if iterations else "-"
        
        # Calculate efficiency
        if generated:
            avg_explored = sum(explored) / len(explored) if explored else 0
            avg_generated = sum(generated) / len(generated)
            efficiency = (avg_explored / avg_generated) * 100 if avg_generated > 0 else 0
            efficiency_str = f"{efficiency:.1f}%"
        else:
            efficiency_str = "-"
        
        # Prepare row data
        row_data = [
            name[:11],
            time_str,
            moves_str,
            generated_str,
            explored_str,
            efficiency_str,
            max_ds_str,
            iterations_str
        ]
        
        # Add timeout count if needed
        if has_timeouts:
            if timeout_count > 0:
                timeout_duration = results.get('timeout_duration', 30)
                timeout_str = f"{timeout_count} ({timeout_duration}s)"
            else:
                timeout_str = "-"
            row_data.insert(1, timeout_str)  # Insert right after algorithm name
        
        processed_results.append({
            'name': name,
            'full_name': results['full_name'],
            'row_data': row_data,
            'avg_time': sum(all_times) / len(all_times) if all_times else float('inf'),
            'avg_successful_time': sum(successful_times) / len(successful_times) if successful_times else float('inf'),
            'avg_moves': avg_moves if successful_lengths else float('inf'),
            'efficiency': efficiency if 'efficiency' in locals() else 0,
            'successful_runs': len(successful_times),
            'timeout_count': timeout_count
        })
        
        # Update column widths
        for i, data in enumerate(row_data):
            col_widths[i] = max(col_widths[i], len(str(data)))
    
    # Build header row and calculate actual table width
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    table_width = len(header_row)
    
    # Sort results with sophisticated timeout handling:
    # 1. No timeouts (sorted by avg successful time)
    # 2. Some timeouts (sorted by timeout count, then avg successful time)
    # 3. All timeouts (placed last)
    def sort_key(x):
        has_timeouts = x['timeout_count'] > 0
        has_successful_runs = x['successful_runs'] > 0
        
        if not has_successful_runs:
            # All timeouts - place at the end (order doesn't matter among these)
            return (2, 0, 0)
        elif not has_timeouts:
            # No timeouts - sort by avg successful time
            return (0, x['avg_successful_time'], 0)
        else:
            # Some timeouts - sort by timeout count, then avg successful time
            return (1, x['timeout_count'], x['avg_successful_time'])
    
    processed_results.sort(key=sort_key)
    
    # Print table with proper borders
    print("\n" + "="*table_width)
    print(f"🏆 MULTI-INSTANCE ALGORITHM COMPARISON RESULTS ({num_instances} instances)")
    print("="*table_width)
    
    # Print header
    print(header_row)
    print("-" * table_width)
    
    # Print data rows
    for result in processed_results:
        row_data = result['row_data']
        row = " | ".join(str(data).ljust(col_widths[i]) for i, data in enumerate(row_data))
        print(row)
    
    print("="*table_width)
    
    # Add comprehensive legend for clarity
    print("\nLegend:")
    if has_timeouts:
        print("- Timeouts: number of instances that timed out, if any")
    print("- Time: average execution time across all instances, in seconds")
    print("- Moves: average number of moves in the solution found (successful instances only)")
    print("- Generated: average number of nodes/states generated during search")
    print("- Explored: average number of nodes/states explored during search")
    print("- Ratio: search efficiency as (Explored/Generated)*100%")
    print("- Frontier: maximum number of entries in the search queue/stack")
    print("- Iterations: maximum search depth (iterative deepening variants only)")
    print("- [min-max]: range of values across instances where applicable")
    print("="*table_width)


def _display_comparison_summary(successful_results: List[Dict[str, Any]], all_results: List[Dict[str, Any]], table_width: int):
    """
    Display summary statistics for single instance comparison.
    
    Args:
        successful_results: List of successful algorithm results
        all_results: List of all algorithm results (including failed ones)
        table_width: Width of the table for consistent borders
    """
    print("\n📊 SUMMARY:")
    
    # Find best performers
    fastest = min(successful_results, key=lambda x: x['solve_time'])
    optimal_results = [r for r in successful_results if r['solution_length'] == min(r['solution_length'] for r in successful_results)]
    most_efficient = max((r for r in successful_results if r['efficiency'] > 0), 
                       key=lambda x: x['efficiency'], default=None)
    least_memory = min((r for r in successful_results if r['nodes_generated'] > 0), 
                      key=lambda x: x['nodes_generated'], default=None)
    
    print(f"⚡ Fastest:          {fastest['algorithm']} ({fastest['solve_time']:.4f}s)")
    print(f"🎯 Optimal:          {', '.join(r['algorithm'] for r in optimal_results)} ({optimal_results[0]['solution_length']} moves)")
    
    if most_efficient:
        print(f"🏅 Most Efficient:   {most_efficient['algorithm']} ({most_efficient['efficiency']:.1f}% efficiency)")
    
    if least_memory:
        print(f"💾 Least Memory:     {least_memory['algorithm']} ({least_memory['nodes_generated']} nodes generated)")
    
    # Show only failed algorithms (timed-out are now in main table)
    failed_results = [r for r in all_results if not r.get('success', False) and not r.get('timeout', False)]
    
    if failed_results:
        print(f"\n❌ Failed: {', '.join(r['algorithm'] for r in failed_results)}")
    
    print("\nLegend:")
    print("- Time: execution time for this instance, in seconds")
    print("- Moves: number of moves in the solution found")
    print("- Explored: number of nodes/states explored during search")
    print("- Generated: number of nodes/states generated during search")
    print("- Frontier: maximum number of entries in the search queue/stack")
    print("- Efficiency: search efficiency as (Explored/Generated)*100%")
    print("- Iterations: maximum search depth (iterative deepening variants only)")
    print("="*table_width) 