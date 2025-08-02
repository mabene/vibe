# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Parser for custom Tower of Hanoi instances specified via command line.

This module handles parsing of the --instance argument format:
-i PEG1_INITIAL:PEG2_INITIAL:PEG3_INITIAL>PEG1_FINAL:PEG2_FINAL:PEG3_FINAL

Example: -i "1,2,5 : 3,4 : 6 > 4,5,6 : 1,2,3 : 5"
Note: Disks are listed from top to bottom, so smaller disks should come first.
      Spaces are allowed anywhere for better readability.
"""

from typing import List, Tuple
import sys
import os

# Add the parent directory to the path to import HanoiState
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers.hanoi_state import HanoiState


def parse_instance(instance_string: str) -> Tuple['HanoiState', 'HanoiState']:
    """
    Parse a custom instance string into initial and target HanoiState objects.
    
    Args:
        instance_string: String in format "PEG1:PEG2:PEG3>PEG1:PEG2:PEG3"
                        where each PEG is comma-separated disk sizes (top to bottom)
                        Disks must be in valid Tower of Hanoi order (smaller on top)
                        Spaces are allowed anywhere for better readability
                        
    Returns:
        Tuple of (initial_state, target_state)
        
    Raises:
        ValueError: If the instance string is malformed or invalid
        
    Example:
        >>> initial, target = parse_instance("1, 3 : 2 : > : 1, 2 : 3")
        >>> print(initial.pegs)  # [[3, 1], [2], []]
        >>> print(target.pegs)   # [[], [2, 1], [3]]
    """
    try:
        # Remove all spaces for easier parsing while maintaining flexibility for users
        clean_string = instance_string.replace(' ', '')
        
        # Split into initial and final parts
        if '>' not in clean_string:
            raise ValueError("Instance string must contain '>' to separate initial and final states")
        
        parts = clean_string.split('>')
        if len(parts) != 2:
            raise ValueError("Instance string must contain exactly one '>' separator")
        
        initial_str, final_str = parts
        
        # Parse initial and final states
        initial_pegs = _parse_state_string(initial_str, "initial")
        final_pegs = _parse_state_string(final_str, "final")
        
        # Validate consistency between initial and final states
        _validate_states_consistency(initial_pegs, final_pegs)
        
        # Create HanoiState objects (convert lists to tuples as required by HanoiState)
        # Reverse each peg's disk order to match HanoiState expectation (largest at bottom)
        initial_pegs_reversed = [list(reversed(peg)) for peg in initial_pegs]
        final_pegs_reversed = [list(reversed(peg)) for peg in final_pegs]
        
        initial_state = HanoiState(tuple(tuple(peg) for peg in initial_pegs_reversed))
        final_state = HanoiState(tuple(tuple(peg) for peg in final_pegs_reversed))
        
        return initial_state, final_state
        
    except Exception as e:
        raise ValueError(f"Failed to parse instance string '{instance_string}': {str(e)}")


def _parse_state_string(state_string: str, state_name: str) -> List[List[int]]:
    """
    Parse a state string into a list of pegs.
    
    Args:
        state_string: String like "1,3:2:5,6" representing pegs
        state_name: Name of the state (for error messages)
        
    Returns:
        List of lists, where each inner list represents disks on a peg (top to bottom)
        
    Raises:
        ValueError: If the state string is malformed
    """
    # Split into pegs
    peg_strings = state_string.split(':')
    if len(peg_strings) != 3:
        raise ValueError(f"{state_name} state must have exactly 3 pegs separated by ':'")
    
    pegs = []
    for peg_idx, peg_str in enumerate(peg_strings):
        peg_str = peg_str.strip()
        
        if not peg_str:  # Empty peg
            pegs.append([])
            continue
            
        # Parse disk sizes
        try:
            disk_strs = peg_str.split(',')
            disks = [int(disk_str.strip()) for disk_str in disk_strs]
        except ValueError:
            raise ValueError(f"{state_name} state peg {peg_idx + 1} contains non-integer disk sizes")
        
        # Validate disk sizes are positive
        for disk in disks:
            if disk <= 0:
                raise ValueError(f"{state_name} state peg {peg_idx + 1} contains non-positive disk size: {disk}")
        
        # Validate disks are in valid Tower of Hanoi order (smaller on top of larger)
        # This means the list should be in increasing order (top to bottom)
        if disks != sorted(disks):
            raise ValueError(f"{state_name} state peg {peg_idx + 1} has disks not in valid Tower of Hanoi order (smaller disks must be on top): {disks}")
        
        pegs.append(disks)
    
    return pegs


def _validate_states_consistency(initial_pegs: List[List[int]], final_pegs: List[List[int]]) -> None:
    """
    Validate that initial and final states contain the same set of disks.
    
    Args:
        initial_pegs: List of pegs for initial state
        final_pegs: List of pegs for final state
        
    Raises:
        ValueError: If states are inconsistent
    """
    # Collect all disks from initial state
    initial_disks = set()
    for peg in initial_pegs:
        for disk in peg:
            if disk in initial_disks:
                raise ValueError(f"Disk {disk} appears multiple times in initial state")
            initial_disks.add(disk)
    
    # Collect all disks from final state
    final_disks = set()
    for peg in final_pegs:
        for disk in peg:
            if disk in final_disks:
                raise ValueError(f"Disk {disk} appears multiple times in final state")
            final_disks.add(disk)
    
    # Check that both states have the same disks
    if initial_disks != final_disks:
        missing_in_final = initial_disks - final_disks
        extra_in_final = final_disks - initial_disks
        
        error_msg = "Initial and final states must contain the same set of disks"
        if missing_in_final:
            error_msg += f". Missing in final: {sorted(missing_in_final)}"
        if extra_in_final:
            error_msg += f". Extra in final: {sorted(extra_in_final)}"
        
        raise ValueError(error_msg)
    
    # Check that we have at least one disk
    if not initial_disks:
        raise ValueError("Instance must contain at least one disk")


def validate_instance_format(instance_string: str) -> str:
    """
    Validate an instance string format without creating HanoiState objects.
    
    This is a lightweight validation function that can be used by argparse
    to check the format before the main parsing logic runs.
    
    Args:
        instance_string: The instance string to validate
        
    Returns:
        The validated instance string (unchanged if valid)
        
    Raises:
        ValueError: If the format is invalid
    """
    if not instance_string.strip():
        raise ValueError("Instance string cannot be empty")
    
    # Remove all spaces for consistent validation with the main parser
    clean_string = instance_string.replace(' ', '')
    
    if '>' not in clean_string:
        raise ValueError("Instance string must contain '>' to separate initial and final states")
    
    parts = clean_string.split('>')
    if len(parts) != 2:
        raise ValueError("Instance string must contain exactly one '>' separator")
    
    initial_str, final_str = parts
    
    # Basic format validation
    for state_name, state_str in [("initial", initial_str), ("final", final_str)]:
        if ':' not in state_str:
            raise ValueError(f"{state_name} state must contain ':' separators for pegs")
        
        peg_count = len(state_str.split(':'))
        if peg_count != 3:
            raise ValueError(f"{state_name} state must have exactly 3 pegs separated by ':'")
    
    return instance_string


if __name__ == "__main__":
    # Test the parser with some examples
    test_cases = [
        "1,3,7,8,10:2,4,9:5,6,11>10::1,2,3,4,5,6,7,8,9,10,11",
        "1:2:3>3:2:1",
        "1,2,3::>::1,2,3",
        "::1,2,3>1,2,3::",
    ]
    
    for test in test_cases:
        try:
            initial, final = parse_instance(test)
            print(f"✓ '{test}' -> Initial: {initial.pegs}, Final: {final.pegs}")
        except ValueError as e:
            print(f"✗ '{test}' -> Error: {e}") 