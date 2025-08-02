# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

from typing import List, Optional


def calculate_column_widths(headers: List[str], data_rows: List[List[str]]) -> List[int]:
    """
    Calculate column widths needed for table formatting.
    
    Args:
        headers: List of column headers
        data_rows: List of data rows, where each row is a list of string values
        
    Returns:
        List of column widths
    """
    col_widths = [max(len(h), 10) for h in headers]
    
    for row in data_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
            
    return col_widths


def print_table(headers: List[str], data_rows: List[List[str]], title: Optional[str] = None):
    """
    Print a formatted ASCII table.
    
    Args:
        headers: List of column headers
        data_rows: List of data rows, where each row is a list of string values
        title: Optional table title
    """
    col_widths = calculate_column_widths(headers, data_rows)
    
    # Print title if provided
    if title:
        table_width = sum(col_widths) + len(headers) * 3 - 1
        print("\n" + "=" * table_width)
        print(title)
        print("=" * table_width)
    
    # Print header
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    
    # Print data rows
    for row in data_rows:
        formatted_row = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(formatted_row)
    
    # Print footer
    if title:
        print("=" * table_width)


def format_time_range(times: List[float]) -> str:
    """
    Format time statistics with optional range.
    
    Args:
        times: List of time values
        
    Returns:
        Formatted time string with range only if values differ
    """
    if not times:
        return "-"
    
    avg_time = sum(times) / len(times)
    if len(times) > 1 and min(times) != max(times):
        return f"{avg_time:.4f} [{min(times):.4f}-{max(times):.4f}]"
    return f"{avg_time:.4f}" 