# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements the no-search solver for classical Tower of Hanoi puzzles.

This solver performs no search whatsoever - it directly computes the 
mathematically optimal solution using the well-known classical algorithm.
"""
from typing import List, Tuple
from ..base_solver import BaseSolver

class ClosedFormSolver(BaseSolver):
    """
    A solver that directly computes the optimal solution without any search.

    This solver exploits the mathematical structure of classical Tower of Hanoi
    puzzles where the branching factor is effectively 1 - at each step, there is
    exactly one optimal next move. Instead of searching through possible paths,
    it directly computes the sequence using the classical recursive formula.
    
    Characteristics:
    - No search through state space
    - No exploration of alternative paths  
    - Direct mathematical computation
    - Optimal for classical puzzles only
    - Branching factor = 1 (no decision points)
    """
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Generates the optimal solution for a classical Tower of Hanoi puzzle.
        
        This method exploits the mathematical structure of the classical puzzle
        to directly compute the optimal solution without any search.
        
        Args:
            max_liftable_disks: Ignored for classical puzzles (always 1).
            
        Returns:
            A list of moves representing the optimal solution.
        """
        # For classical puzzles, we can directly compute the solution
        # The optimal solution follows a recursive pattern
        
        # Find which peg has all the disks initially
        from_peg = None
        num_disks = 0
        
        for peg_idx, peg in enumerate(self.initial_state.pegs):
            if peg:
                from_peg = peg_idx + 1  # Convert to 1-indexed
                num_disks = len(peg)
                break
        
        if from_peg is None:
            return []  # No disks to move
        
        # Find the target peg
        to_peg = None
        for peg_idx, peg in enumerate(self.target_state.pegs):
            if peg:
                to_peg = peg_idx + 1  # Convert to 1-indexed
                break
        
        if to_peg is None:
            return []  # No target specified
        
        # Find the auxiliary peg (the one that's neither source nor target)
        all_pegs = {1, 2, 3}
        aux_peg = list(all_pegs - {from_peg, to_peg})[0]
        
        # Generate the optimal solution recursively
        return self._hanoi_recursive(num_disks, from_peg, to_peg, aux_peg)
    
    def _hanoi_recursive(self, n: int, from_peg: int, to_peg: int, aux_peg: int) -> List[Tuple[int, int, int]]:
        """
        Recursively generates the optimal solution for moving n disks.
        
        Args:
            n: Number of disks to move.
            from_peg: Source peg (1-indexed).
            to_peg: Destination peg (1-indexed).
            aux_peg: Auxiliary peg (1-indexed).
            
        Returns:
            List of moves to transfer n disks from from_peg to to_peg.
        """
        # Track that we're generating nodes (even though no search is involved)
        self._stats_node_generated()
        
        if n == 1:
            return [(from_peg, to_peg, 1)]
        
        moves = []
        
        # Move n-1 disks from source to auxiliary peg
        moves.extend(self._hanoi_recursive(n - 1, from_peg, aux_peg, to_peg))
        
        # Move the largest disk from source to destination
        moves.append((from_peg, to_peg, 1))
        
        # Move n-1 disks from auxiliary to destination peg
        moves.extend(self._hanoi_recursive(n - 1, aux_peg, to_peg, from_peg))
        
        return moves 