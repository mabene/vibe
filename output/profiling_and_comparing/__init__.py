# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Profiling and Comparing package for the Hanoi project.

This package provides centralized functions for displaying all types of 
algorithm results, comparisons, and statistics in formatted tables.
"""

# Import all display functions from submodules
from .comparison import (
    display_single_instance_comparison,
    display_multi_instance_comparison,
)

from ..solution import (
    display_solution_moves,
    display_solution_states,
    display_puzzle_header,
    display_puzzle_states,
    display_solution_summary,
    display_verbosity_warning,
    display_instance_progress,
    display_instance_result,
    display_multi_instance_header,
    display_fastest_solution_details,
    determine_verbosity_level,
)

from .statistics import (
    display_aggregate_statistics,
    calculate_statistics_summary,
    display_statistics_comparison,
)

from .performance import (
    display_search_statistics,
    display_performance_comparison,
    display_algorithm_details,
)

__all__ = [
    # Algorithm comparison
    'display_single_instance_comparison',
    'display_multi_instance_comparison',
    
    # Solution display
    'display_solution_moves',
    'display_solution_states',
    'display_puzzle_header',
    'display_puzzle_states',
    'display_solution_summary',
    'display_verbosity_warning',
    'display_instance_progress',
    'display_instance_result',
    'display_multi_instance_header',
    'display_fastest_solution_details',
    'determine_verbosity_level',
    
    # Aggregate statistics
    'display_aggregate_statistics',
    'calculate_statistics_summary',
    'display_statistics_comparison',
    
    # Performance profiling
    'display_search_statistics',
    'display_performance_comparison',
    'display_algorithm_details',
] 