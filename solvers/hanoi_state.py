# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

import random
from typing import Union, List, Tuple

class HanoiState:
    """
    Represents a single, immutable state of a Tower of Hanoi puzzle.

    This class encapsulates the configuration of disks on three pegs. The state
    is represented by a tuple of tuples, where each inner tuple contains the
    disks on a peg, ordered from largest at the bottom to smallest at the top.
    
    The class is designed to be immutable. Methods that change the state, such as
    `apply_move`, return a new `HanoiState` instance rather than modifying the
    current one. This makes it suitable for use in search algorithms that require
    tracking visited states, as instances can be safely added to sets and used
    as dictionary keys.

    Attributes:
        pegs (tuple[tuple[int, ...], ...]): The core data structure representing
            the three pegs and the disks on them.
        number_of_disks (int): The total number of disks in this puzzle state.
    """
    def __init__(self, pegs: tuple[tuple[int, ...], ...]):
        """
        Initializes a new state for the Tower of Hanoi puzzle.

        Args:
            pegs: A tuple of three tuples, where each inner tuple represents a
                  peg. Disks are represented by integers, with larger numbers
                  for larger disks.

        Raises:
            ValueError: If the number of pegs is not exactly 3.
        """
        if len(pegs) != 3:
            raise ValueError("There must be exactly 3 pegs.")
        
        self.pegs = pegs
        self._hash = None
        self.number_of_disks = sum(len(p) for p in pegs)

    @classmethod
    def classic_init(cls, num_disks: int, on_peg: int = 1):
        """
        Creates a `HanoiState` for a classical puzzle setup.

        Args:
            num_disks: The total number of disks for the puzzle.
            on_peg: The 1-indexed peg on which to stack the disks.

        Returns:
            A `HanoiState` instance representing the specified classical setup.
        
        Raises:
            ValueError: If `num_disks` is not a positive integer or `on_peg`
                        is not a valid peg number (1, 2, or 3).
        """
        if not isinstance(num_disks, int) or num_disks < 1:
            raise ValueError("Number of disks must be a positive integer")
        if not (1 <= on_peg <= 3):
            raise ValueError("Peg number must be between 1 and 3.")
        
        pegs: List[Tuple[int, ...]] = [(), (), ()]
        pegs[on_peg - 1] = tuple(range(num_disks, 0, -1))
        
        return cls(tuple(pegs))

    @classmethod
    def random_init(cls, num_disks: int):
        """
        Creates a valid, randomized `HanoiState`.

        This method distributes the specified number of disks randomly across
        the three pegs while adhering to the fundamental rule that no larger
        disk may be placed on a smaller one.

        Args:
            num_disks: The total number of disks to distribute.

        Returns:
            A `HanoiState` instance with a valid, random configuration.
            
        Raises:
            ValueError: If `num_disks` is not a positive integer.
        """
        if not isinstance(num_disks, int) or num_disks < 1:
            raise ValueError("Number of disks must be a positive integer")
        
        disks = list(range(num_disks, 0, -1))
        pegs: List[List[int]] = [list() for _ in range(3)]
        
        for disk in disks:
            valid_peg_indices = [i for i, p in enumerate(pegs) if not p or disk < p[-1]]
            chosen_peg_idx = random.choice(valid_peg_indices)
            pegs[chosen_peg_idx].append(disk)
            
        return cls(tuple(tuple(p) for p in pegs))

    def render(self) -> str:
        """
        Generates an ASCII art representation of the current state.

        Returns:
            A string containing the rendered view of the pegs and disks.
        """
        from output.rendering_towers.render_hanoi_towers import render_hanoi_towers
        return render_hanoi_towers(self.pegs)

    def apply_move(self, from_peg: int, to_peg: int, how_many_disks: int = 1) -> 'HanoiState':
        """
        Applies a move and returns a new, resulting HanoiState object.

        This method simulates moving one or more disks from a source peg to a
        target peg. It performs validation to ensure the move is legal according
        to the rules of the generalized Tower of Hanoi puzzle.

        Args:
            from_peg: The 1-indexed source peg number.
            to_peg: The 1-indexed target peg number.
            how_many_disks: The number of disks to move from top of the source peg.

        Returns:
            A new `HanoiState` instance representing the board after the move.

        Raises:
            ValueError: If peg numbers are invalid, source and target are the
                        same, not enough disks are on the source peg, or the move
                        is illegal (placing a larger disk on a smaller one).
        """
        if not (1 <= from_peg <= 3 and 1 <= to_peg <= 3):
            raise ValueError("Peg numbers must be between 1 and 3.")
        if from_peg == to_peg:
            raise ValueError("Source and target pegs cannot be the same.")

        from_peg_idx = from_peg - 1
        to_peg_idx = to_peg - 1

        original_pegs = self.pegs
        
        if len(original_pegs[from_peg_idx]) < how_many_disks:
             raise ValueError(f"Not enough disks on peg {from_peg} to move.")
        
        disks_to_move = original_pegs[from_peg_idx][-how_many_disks:]

        if original_pegs[to_peg_idx] and disks_to_move[0] > original_pegs[to_peg_idx][-1]:
             raise ValueError("Cannot place a larger disk on a smaller one.")

        new_pegs_list = [list(p) for p in original_pegs]
        new_pegs_list[from_peg_idx] = new_pegs_list[from_peg_idx][:-how_many_disks]
        new_pegs_list[to_peg_idx].extend(disks_to_move)

        return HanoiState(tuple(tuple(p) for p in new_pegs_list))

    def __hash__(self):
        """
        Computes the hash of the state, caching the result for efficiency.
        """
        if self._hash is None:
            self._hash = hash(self.pegs)
        return self._hash

    def __eq__(self, other):
        """
        Checks for equality between two HanoiState instances.
        """
        return isinstance(other, HanoiState) and self.pegs == other.pegs

    def get_classical_peg_if_any(self) -> Union[int, None]:
        """
        Checks if the state is a "classical" configuration.

        A classical configuration is one where all disks of the puzzle are
        stacked in correct decreasing order on a single peg.

        Returns:
            The 1-indexed number of the peg holding all the disks if it's a
            classical configuration, otherwise None.
        """
        pegs_with_disks_indices = [i for i, peg in enumerate(self.pegs) if peg]
        if len(pegs_with_disks_indices) != 1:
            return None

        peg_idx_0_based = pegs_with_disks_indices[0]
        peg = self.pegs[peg_idx_0_based]

        if len(peg) != self.number_of_disks:
            return None

        expected_disks = tuple(range(self.number_of_disks, 0, -1))
        if peg == expected_disks:
            return peg_idx_0_based + 1
        
        return None
