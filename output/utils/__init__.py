# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Utilities package for the Hanoi project.

This package contains utility functions for string manipulation and table formatting.
"""

from .string_utils import juxtapose_multiline_strings
from .table_formatting import calculate_column_widths, print_table, format_time_range

__all__ = [
    # String utilities
    'juxtapose_multiline_strings',
    
    # Table formatting utilities
    'calculate_column_widths',
    'print_table',
    'format_time_range',
] 