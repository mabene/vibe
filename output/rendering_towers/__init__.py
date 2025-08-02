# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Rendering towers package for the Hanoi project.

This package provides functions to render Tower of Hanoi states as ASCII art,
including side-by-side rendering, move visualization, and custom styles.
"""

# Import all functions from the render_hanoi_towers module
from .render_hanoi_towers import (
    render_hanoi_towers,
    rendered_tower,
    padded_rendered_tower,
    juxtapose_multiline_strings,
)

__all__ = ['render_hanoi_towers', 'rendered_tower', 'padded_rendered_tower', 'juxtapose_multiline_strings'] 