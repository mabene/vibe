# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

from typing import List, Tuple, Any, Optional


def display_solution_moves(solution_path: List[Tuple[int, int, int]]):
    """
    Display the solution as a list of moves.
    
    Args:
        solution_path: List of tuples representing moves (from_peg, to_peg, num_disks)
    """
    print("\nSolution:")
    for i, move in enumerate(solution_path):
        from_p, to_p, num_d = move
        disk_str = "disk" if num_d == 1 else "disks"
        print(f"  Move {i+1}: {num_d} {disk_str} from peg {from_p} to peg {to_p}")


def display_solution_states(solution_path: List[Tuple[int, int, int]], initial_state: Any):
    """
    Display the solution with intermediate states.
    
    Args:
        solution_path: List of tuples representing moves (from_peg, to_peg, num_disks)
        initial_state: The initial HanoiState to start from
    """
    print("\nSolution (with intermediate states):")
    current_state = initial_state
    for i, move in enumerate(solution_path):
        from_p, to_p, num_d = move
        disk_str = "disk" if num_d == 1 else "disks"
        print(f"\nMove {i+1}: {num_d} {disk_str} from peg {from_p} to peg {to_p}")
        current_state = current_state.apply_move(from_p, to_p, num_d)
        print(current_state.render())


def display_puzzle_header(num_disks: int, mode: str):
    """
    Display the puzzle header with initial setup information.
    
    Args:
        num_disks: Number of disks in the puzzle
        mode: Type of puzzle ('classic' or 'random')
    """
    if mode == 'classic':
        print(f"--- Solving a classical Hanoi puzzle with {num_disks} disks ---")
    else:
        print(f"--- Searching for a solution between two random {num_disks}-disk states ---")


def display_puzzle_states(initial_state: Any, target_state: Any):
    """
    Display the initial and target states of the puzzle.
    
    Args:
        initial_state: The starting HanoiState
        target_state: The target HanoiState
    """
    print("\nInitial State:")
    print(initial_state.render())
    print("\nTarget State:")
    print(target_state.render())


def display_solution_summary(solution_length: int, elapsed_time: float, mode: str):
    """
    Display a summary of the solution found.
    
    Args:
        solution_length: Number of moves in the solution found
        elapsed_time: Time taken to find the solution
        mode: Type of puzzle ('classic' or 'random')
    """
    summary_verb = "produced" if mode == 'classic' else "found"
    print(f"\nShortest solution {summary_verb} in {elapsed_time:.4f} seconds: {solution_length} moves required.")


def display_verbosity_warning():
    """Display a warning about output being suppressed due to length."""
    print("(Output suppressed as it exceeds 100 moves. Use --show [moves|states] to see it.)")


def display_instance_progress(instance: int, total_instances: int):
    """
    Display progress information for multi-instance runs.
    
    Args:
        instance: Current instance number (1-indexed)
        total_instances: Total number of instances
    """
    print(f"\n🔄 Instance {instance}/{total_instances}:")


def display_instance_result(elapsed_time: float, solution_length: int):
    """
    Display the result of a single instance.
    
    Args:
        elapsed_time: Time taken to solve this instance
        solution_length: Number of moves in the solution found
    """
    print(f"  ✓ Solved in {elapsed_time:.4f}s with {solution_length} moves")


def display_multi_instance_header(num_instances: int, mode: str, num_disks: int):
    """
    Display header for multi-instance runs.
    
    Args:
        num_instances: Number of instances being run
        mode: Type of puzzle ('classic' or 'random')
        num_disks: Number of disks in the puzzle
    """
    print(f"--- Running {num_instances} instances of {mode} {num_disks}-disk puzzles ---")


def display_fastest_solution_details(fastest_instance: dict, show_moves: bool = False):
    """
    Display details of the fastest solution found.
    
    Args:
        fastest_instance: Dictionary containing the fastest instance data
        show_moves: Whether to show the actual moves
    """
    print(f"\n💨 Fastest solution (Instance {fastest_instance['instance']}):")
    print(f"   Time: {fastest_instance['elapsed_time']:.4f}s, Moves: {fastest_instance['solution_length']}")
    
    if show_moves:
        print("\n   Solution:")
        for i, move in enumerate(fastest_instance['solution_path']):
            from_p, to_p, num_d = move
            disk_str = "disk" if num_d == 1 else "disks"
            print(f"     Move {i+1}: {num_d} {disk_str} from peg {from_p} to peg {to_p}")


def determine_verbosity_level(solution_path: List[Tuple[int, int, int]], show_arg: Optional[str] = None) -> str:
    """
    Determine the level of detail to show based on user args or smart defaults.
    
    Args:
        solution_path: The list of moves in the solution
        show_arg: The user's --show argument value
        
    Returns:
        The verbosity level ('summary', 'moves', or 'states')
    """
    if show_arg:
        return show_arg
    
    if len(solution_path) <= 100:
        return 'moves'
    else:
        display_verbosity_warning()
        return 'summary' 