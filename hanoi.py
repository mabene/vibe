# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Tower of Hanoi solver with multiple algorithms and comprehensive analysis.

This module provides a comprehensive command-line interface for solving Tower of Hanoi
puzzles using various algorithms, with detailed performance analysis and visualization.
"""

import argparse
import math
import random
import sys
import time
from typing import List, Tuple, Any, Dict

from input.commandline_args import create_parser
from driver.driver import HanoiDriver
from solvers.hanoi_state import HanoiState
from output.profiling_and_comparing import (
    display_puzzle_header,
    display_puzzle_states,
    display_solution_summary,
    display_solution_moves,
    display_solution_states,
    display_multi_instance_header,
    display_instance_progress,
    display_instance_result,
    display_aggregate_statistics,
    determine_verbosity_level
)
from input.instance_parser import parse_instance

def main():
    """
    Main entry point for the command-line interface.

    Parses arguments and calls the appropriate functions to solve the puzzle.
    Includes a shortcut for the common case of solving a classical puzzle,
    e.g., `python3 hanoi.py 5`.
    """
    # Handle the simple shortcut case: `python3 hanoi.py 5`
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        num_disks = int(sys.argv[1])
        # Manually create args namespace with correct defaults for the shortcut.
        args = argparse.Namespace(show=None, max_lift=1, search=None, profile=None, timeout=30, seed=None, instance=None)
        # No seed initialization for shortcut case (will use random puzzles if applicable)
        if num_disks > 0:
            solve_puzzle(num_disks, 'classic', args)
        else:
            print("Error: Number of disks must be a positive integer.", file=sys.stderr)
        return

    parser = create_parser()
    args = parser.parse_args()

    # Initialize random seed for reproducibility if specified
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Random seed set to {args.seed} for reproducible puzzle generation.")

    if args.classic:
        if args.classic > 0:
            solve_puzzle(args.classic, 'classic', args)
        else:
            print("Error: Number of disks for --classic must be a positive integer.", file=sys.stderr)
    
    elif args.random:
        if args.random > 0:
            solve_puzzle(args.random, 'random', args)
        else:
            print("Error: Number of disks for --random must be a positive integer.", file=sys.stderr)
    
    elif args.instance:
        solve_custom_instance(args)

def solve_puzzle(num_disks: int, mode: str, args: argparse.Namespace):
    """
    Coordinates the process of solving a single puzzle instance.

    This function handles the entire lifecycle of a puzzle run:
    1.  Creates the initial and target `HanoiState` objects based on the mode.
    2.  Instantiates the `HanoiSolver`.
    3.  Times the solving process.
    4.  Prints the results according to the determined verbosity level.

    Args:
        num_disks: The number of disks to use for the puzzle.
        mode: The type of puzzle to create ('classic' or 'random').
        args: The parsed command-line arguments, used for verbosity control.
    """
    # Determine number of instances to run
    num_instances = args.profile if args.profile is not None and args.profile > 1 else 1
    
    if num_instances > 1:
        solve_multiple_instances(num_disks, mode, args, num_instances)
    else:
        solve_single_instance(num_disks, mode, args)

def solve_single_instance(num_disks: int, mode: str, args: argparse.Namespace):
    """
    Solves a single puzzle instance with the specified algorithm.
    
    Args:
        num_disks: The number of disks to use for the puzzle.
        mode: The type of puzzle to create ('classic' or 'random').
        args: The parsed command-line arguments.
    """
    # Display puzzle header
    display_puzzle_header(num_disks, mode)
    
    # Generate puzzle states
    if mode == 'classic' and num_disks >= 10 and args.show == 'states':
        print(f"Warning: Showing states for a classical puzzle with {num_disks} disks will be very verbose.")
    
    initial_state, target_state = HanoiDriver.generate_puzzle_states(num_disks, mode)
    
    # Display puzzle states
    display_puzzle_states(initial_state, target_state)
    
    # Solve the puzzle
    driver = HanoiDriver(initial_state, target_state)
    start_time = time.time()
    solution_path = driver.solve_with_algorithm(max_lift=args.max_lift, algorithm=args.search, profile=args.profile, timeout=args.timeout)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Skip final summary for COMPARE mode - the comparison table is the final result
    if args.search == 'COMPARE':
        return
    
    # Display solution summary
    display_solution_summary(len(solution_path), elapsed_time, mode)
    
    # Display solution based on verbosity level
    verbosity = determine_verbosity_level(solution_path, args.show)
    
    if verbosity == 'moves':
        display_solution_moves(solution_path)
    elif verbosity == 'states':
        display_solution_states(solution_path, initial_state)

def solve_multiple_instances(num_disks: int, mode: str, args: argparse.Namespace, num_instances: int):
    """
    Solves multiple puzzle instances and reports averaged statistics.
    
    Args:
        num_disks: The number of disks to use for the puzzle.
        mode: The type of puzzle to create ('classic' or 'random').
        args: The parsed command-line arguments, used for verbosity control.
        num_instances: The number of instances to run.
    """
    display_multi_instance_header(num_instances, mode, num_disks)
    
    # Handle COMPARE mode specially - let HanoiDriver manage multiple instances
    if args.search == 'COMPARE':
        # Generate first instance for the initial solver
        if mode == 'classic':
            initial_state = HanoiState.classic_init(num_disks, on_peg=1)
            target_state = HanoiState.classic_init(num_disks, on_peg=3)
        else: # mode == 'random'
            initial_state = HanoiState.random_init(num_disks)
            target_state = HanoiState.random_init(num_disks)
            while initial_state == target_state:
                target_state = HanoiState.random_init(num_disks)
        
        # Only show states if explicitly requested with --show states
        if args.show == 'states':
            print("\nFirst instance states:")
            display_puzzle_states(initial_state, target_state)
        
        # Let HanoiDriver handle the multi-instance comparison
        driver = HanoiDriver(initial_state, target_state)
        start_time = time.time()
        solution_path = driver.solve_with_algorithm(max_lift=args.max_lift, algorithm=args.search, profile=num_instances, timeout=args.timeout)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Don't print misleading summary for COMPARE mode - the comparison table is the final result
        return
    
    # Handle single algorithm across multiple instances
    all_results = []
    
    for instance in range(num_instances):
        if num_instances > 1:
            display_instance_progress(instance + 1, num_instances)
        
        # Generate puzzle states
        initial_state, target_state = HanoiDriver.generate_puzzle_states(num_disks, mode)
        
        # Only show states for first instance if explicitly requested with --show states
        if instance == 0 and args.show == 'states':
            display_puzzle_states(initial_state, target_state)
        
        # Solve the puzzle
        driver = HanoiDriver(initial_state, target_state)
        start_time = time.time()
        solution_path = driver.solve_with_algorithm(max_lift=args.max_lift, algorithm=args.search, profile=1, timeout=args.timeout)  # Always profile for multi-instance
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Collect results
        result = {
            'instance': instance + 1,
            'elapsed_time': elapsed_time,
            'solution_length': len(solution_path),
            'solution_path': solution_path
        }
        all_results.append(result)
        
        display_instance_result(elapsed_time, len(solution_path))
    
    # Calculate and display aggregate statistics
    profile_enabled = args.profile is not None
    show_moves_condition = args.show == 'moves' or (args.show is None and 
                                                    min(all_results, key=lambda x: x['elapsed_time'])['solution_length'] <= 100)
    display_aggregate_statistics(all_results, mode, num_disks, profile_enabled, show_moves_condition)

def solve_custom_instance(args: argparse.Namespace):
    """
    Solve a custom instance specified by the user.
    
    Args:
        args: The parsed command-line arguments containing the instance specification.
    """
    try:
        # Parse the instance string to get initial and target states
        initial_state, target_state = parse_instance(args.instance)
        
        # For custom instances, multiple runs don't make sense since the instance is fixed
        if args.profile is not None and args.profile > 1:
            print(f"Note: Multiple instances (-p {args.profile}) not applicable for custom instances.")
            print("Custom instances specify a fixed puzzle configuration, so multiple runs would be identical.")
            print("Solving the custom instance once...\n")
        
        num_disks = initial_state.number_of_disks
        
        # Display puzzle header
        print(f"--- Solving a custom Hanoi puzzle with {num_disks} disks ---\n")
        
        # Display puzzle states
        display_puzzle_states(initial_state, target_state)
        
        # Solve the puzzle
        driver = HanoiDriver(initial_state, target_state)
        start_time = time.time()
        solution_path = driver.solve_with_algorithm(max_lift=args.max_lift, algorithm=args.search, profile=args.profile, timeout=args.timeout)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Skip final summary for COMPARE mode - the comparison table is the final result
        if args.search == 'COMPARE':
            return
        
        # Display solution summary
        print(f"\nShortest solution found in {elapsed_time:.4f} seconds: {len(solution_path)} moves required.")
        
        # Display solution based on verbosity level
        verbosity = determine_verbosity_level(solution_path, args.show)
        
        if verbosity == 'moves':
            display_solution_moves(solution_path)
        elif verbosity == 'states':
            display_solution_states(solution_path, initial_state)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return

if __name__ == '__main__':
    main()