# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Driver package for the Hanoi project.

This package contains the main driver classes for orchestrating puzzle solving,
algorithm comparison, and performance profiling. The driver coordinates between
solvers, manages execution, and provides interfaces for different solving modes.

Classes:
    HanoiDriver: Main orchestrator for solving Tower of Hanoi puzzles
    AlgorithmComparator: Handles comparison of different algorithms
    PerformanceProfiler: Collects and analyzes performance metrics

Functions:
    generate_puzzle_states: Generate puzzle states for testing
    validate_solution: Validate solution correctness
"""

# Backwards compatibility and main API
from .driver import HanoiDriver
from .comparator import AlgorithmComparator
from .profiler import PerformanceProfiler

__all__ = [
    'HanoiDriver',
    'AlgorithmComparator', 
    'PerformanceProfiler'
] 