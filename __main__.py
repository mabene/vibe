# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Makes the Hanoi package executable using `python -m Hanoi`.

This file allows the user to run the solver directly using the `-m` flag
with the package name, providing a cleaner invocation syntax. For example:

`python -m Hanoi --classic 4`
"""
import runpy

if __name__ == "__main__":
    # This correctly sets up the package context and runs hanoi.py as the main script.
    runpy.run_module("Hanoi.hanoi", run_name="__main__") 