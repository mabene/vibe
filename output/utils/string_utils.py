# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

def juxtapose_multiline_strings(*strings: str, padding: int = 1) -> str:
    """
    Juxtaposes multiple multiline strings side by side.
    
    Args:
        *strings: Variable number of multiline strings to juxtapose.
        padding: Number of spaces between strings.
        
    Returns:
        Combined multiline string with proper alignment.
    """
    if not strings:
        return ""
    
    # Split each string into lines
    lines_arrays = [s.split('\n') for s in strings]
    
    # Find the maximum number of lines
    max_lines = max(len(lines) for lines in lines_arrays)
    
    # Calculate width of each string
    widths = [max(len(line) for line in lines) if lines else 0 for lines in lines_arrays]
    
    # Build the result
    result_lines = []
    for i in range(max_lines):
        line_parts = []
        for j, lines in enumerate(lines_arrays):
            if i < len(lines):
                line_parts.append(lines[i].ljust(widths[j]))
            else:
                line_parts.append(' ' * widths[j])
        result_lines.append((' ' * padding).join(line_parts))
    
    return '\n'.join(result_lines)