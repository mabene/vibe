# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Render Hanoi towers to ASCII art.

This module provides functions to render Tower of Hanoi states as ASCII art,
including side-by-side rendering, move visualization, and custom styles.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Add the parent directory to the path to import from solvers
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from solvers.hanoi_state import HanoiState
from ..utils.string_utils import juxtapose_multiline_strings


def render_hanoi_towers(pegs: tuple[tuple[int, ...], ...]) -> str:
    """
    Renders the complete state of the Tower of Hanoi puzzle.
    """
    all_disks = [d for p in pegs for d in p]
    if not all_disks:
        max_disk_val = 5 # Default for empty board
        max_height = 5
    else:
        max_disk_val = max(all_disks)
        max_height = len(all_disks)

    max_width_vis = 2 * max_disk_val + 1
    
    rendered_pegs = [padded_rendered_tower(list(p), max_height, max_width_vis) for p in pegs]
    return juxtapose_multiline_strings(*rendered_pegs, padding=2)

def rendered_tower(disk_widths: list[int]) -> str:
    """
    Renders a tower given a list of disk widths (bottom to top).
    Each disk is rendered as underscores with a pipe at the center, centered to the largest disk.
    Each logical width is mapped to a visual width using: visual_width = 2*logical_width + 1.

    Args:
        disk_widths: List of integers, each the logical width of a disk, from bottom to top.
            Must be monotonically decreasing (no disk on top of a smaller disk).

    Returns:
        A multiline string representation of the tower.
    """
    mapped_widths = [2 * w + 1 for w in disk_widths]

    if not mapped_widths:
        return ""
    if any(mapped_widths[i] <= 0 for i in range(len(mapped_widths))):
        raise ValueError("All disk widths must be positive integers.")
    if any(mapped_widths[i] >= mapped_widths[i-1] for i in range(1, len(mapped_widths))):
        raise ValueError("Disk widths must be monotonically decreasing from bottom to top.")

    max_width = mapped_widths[0]
    lines = []
    for width in reversed(mapped_widths):  # top to bottom
        half_disk = "_" * ((width - 1) // 2)
        disk = f"{half_disk}|{half_disk}"    
        lines.append(disk.center(max_width))
    return "\n".join(lines)

def padded_rendered_tower(disk_widths: list[int], max_height: int, max_width: Optional[int] = None) -> str:
    """
    Returns a string representing a tower of the given disk widths, padded to max_height.
    The way the tower is padded is that the top of the tower is padded with pipes
    that prolong the ones already present, up to a height of max_height 
    (while nothing is padded below the top of the tower).
    Overall, the pipes, visually, form a rod of max_height.
    This is done by inserting the appropriate number of strings plus newlines in front of
    the string returned by render_tower.

    Args:
        disk_widths: List of integers, each the width of a disk, from bottom to top.
        max_height: The maximum height for padding.
        max_width: If provided, each line of the output will be centered to this width.
    
    Returns:
        A string representation of the padded tower.
    """
    height = len(disk_widths)
    if max_height <= 0:
        return ""
    if height > max_height:
        raise ValueError("height cannot be greater than max_height")
    
    result_str = ""
    if not disk_widths:
        result_str = ("|\n" * max_height).rstrip("\n")
    else:
        current_max_width = 2 * disk_widths[0] + 1  # Use the width of the largest disk for centering
        pad_lines = max_height - height
        pad = ("|".center(current_max_width) + "\n") * pad_lines if pad_lines > 0 else ""

        tower = rendered_tower(disk_widths)
        if tower:
            result_str = pad + tower
        else:
            result_str = pad.rstrip("\n")

    if max_width is not None:
        lines = result_str.split('\n')
        centered_lines = [line.center(max_width) for line in lines]
        result_str = "\n".join(centered_lines)
        
    return result_str 