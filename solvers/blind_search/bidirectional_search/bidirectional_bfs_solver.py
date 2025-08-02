# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Bidirectional BFS solver for Tower of Hanoi puzzles.

This module implements bidirectional breadth-first search, which simultaneously
searches from both the initial state forward and the target state backward
until the two search frontiers meet.
"""

from collections import deque
from typing import List, Tuple, Dict, Any, Optional

from ...base_solver import BaseSolver
from ...hanoi_state import HanoiState

class BidirectionalBFSSolver(BaseSolver):
    """
    Bidirectional BFS solver for Tower of Hanoi puzzles.
    
    This solver searches simultaneously from both the initial state (forward)
    and the target state (backward) until the two search frontiers meet.
    This can significantly reduce the search space compared to unidirectional BFS.
    """
    
    def __init__(self, initial_state: HanoiState, target_state: HanoiState):
        """
        Initialize the bidirectional BFS solver.
        
        Args:
            initial_state: The starting configuration of the puzzle.
            target_state: The desired final configuration of the puzzle.
        """
        super().__init__(initial_state, target_state)
        # Track which direction found the solution
        self._meeting_point = None
        self._forward_path = []
        self._backward_path = []
        
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Solve the puzzle using bidirectional BFS.
        
        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.
            
        Returns:
            A list of moves representing the solution path.
        """
        # Initialize forward and backward search frontiers
        forward_queue = deque([(self.initial_state, [])])
        backward_queue = deque([(self.target_state, [])])
        
        # Track visited states and their paths
        forward_visited = {self.initial_state: []}
        backward_visited = {self.target_state: []}
        
        # Alternate between forward and backward search
        forward_turn = True
        
        while forward_queue or backward_queue:
            # Update statistics
            self._stats_data_structure_size(len(forward_queue) + len(backward_queue))
            
            if forward_turn and forward_queue:
                # Forward search step
                current_state, path = forward_queue.popleft()
                self._stats_node_explored()
                
                # Check if we've met the backward search
                if current_state in backward_visited:
                    # Found intersection!
                    backward_path = backward_visited[current_state]
                    return self._construct_solution_path(path, backward_path)
                
                # Generate moves from current state
                moves = self._get_possible_moves(current_state, max_liftable_disks)
                
                for move in moves:
                    from_peg, to_peg, num_disks = move
                    
                    try:
                        new_state = current_state.apply_move(from_peg, to_peg, num_disks)
                        
                        if new_state not in forward_visited:
                            forward_visited[new_state] = path + [move]
                            forward_queue.append((new_state, path + [move]))
                            self._stats_node_generated()
                            
                    except ValueError:
                        # Invalid move, skip
                        continue
                        
            else:
                # Backward search step
                if backward_queue:
                    current_state, path = backward_queue.popleft()
                    self._stats_node_explored()
                    
                    # Check if we've met the forward search
                    if current_state in forward_visited:
                        # Found intersection!
                        forward_path = forward_visited[current_state]
                        return self._construct_solution_path(forward_path, path)
                    
                    # Generate moves from current state (backward)
                    moves = self._get_possible_moves(current_state, max_liftable_disks)
                    
                    for move in moves:
                        from_peg, to_peg, num_disks = move
                        
                        try:
                            new_state = current_state.apply_move(from_peg, to_peg, num_disks)
                            
                            if new_state not in backward_visited:
                                backward_visited[new_state] = path + [move]
                                backward_queue.append((new_state, path + [move]))
                                self._stats_node_generated()
                                
                        except ValueError:
                            # Invalid move, skip
                            continue
            
            # Alternate between forward and backward search
            forward_turn = not forward_turn
        
        # No solution found
        raise RuntimeError("No solution found")
    
    def _construct_solution_path(self, forward_path: List[Tuple[int, int, int]], 
                               backward_path: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Construct the complete solution path from forward and backward paths.
        
        Args:
            forward_path: Path from initial state to meeting point.
            backward_path: Path from target state to meeting point.
            
        Returns:
            Complete solution path from initial to target state.
        """
        # The backward path needs to be reversed and inverted
        reversed_backward_path = []
        
        # Reverse the backward path and invert each move
        for move in reversed(backward_path):
            from_peg, to_peg, num_disks = move
            # Invert the move (swap from and to pegs)
            inverted_move = (to_peg, from_peg, num_disks)
            reversed_backward_path.append(inverted_move)
        
        # Combine forward path with reversed backward path
        complete_path = forward_path + reversed_backward_path
        
        return complete_path
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get detailed statistics about the search process.
        
        Returns:
            A dictionary containing statistics about the search.
        """
        base_stats = super().get_stats()
        base_stats.update({
            'algorithm_name': 'Bidirectional BFS',
            'meeting_point': self._meeting_point,
            'forward_path_length': len(self._forward_path),
            'backward_path_length': len(self._backward_path)
        })
        return base_stats
    
    def _expand_forward(self, queue: deque, visited: Dict, max_liftable_disks: int) -> None:
        """Expands one level of the forward search."""
        if not queue:
            return
            
        current_state, path = queue.popleft()
        possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
        
        for from_peg, to_peg, num_disks in possible_moves:
            try:
                next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                if next_state not in visited:
                    new_path = path + [(from_peg, to_peg, num_disks)]
                    visited[next_state] = new_path
                    queue.append((next_state, new_path))
            except ValueError:
                continue
    
    def _expand_backward(self, queue: deque, visited: Dict, max_liftable_disks: int) -> None:
        """Expands one level of the backward search."""
        if not queue:
            return
            
        current_state, path = queue.popleft()
        possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
        
        for from_peg, to_peg, num_disks in possible_moves:
            try:
                next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                if next_state not in visited:
                    # For backward search, we store the reverse move
                    new_path = [(to_peg, from_peg, num_disks)] + path
                    visited[next_state] = new_path
                    queue.append((next_state, new_path))
            except ValueError:
                continue
    
    def _find_intersection(self, forward_visited: Dict, backward_visited: Dict) -> Optional['HanoiState']:
        """Finds if forward and backward searches have met at a common state."""
        common_states = set(forward_visited.keys()) & set(backward_visited.keys())
        if common_states:
            return next(iter(common_states))  # Return any common state
        return None
    
    def _reconstruct_path(self, intersection: 'HanoiState', forward_visited: Dict, backward_visited: Dict) -> List[tuple[int, int, int]]:
        """Reconstructs the complete path from initial to target via the intersection."""
        forward_path = forward_visited[intersection]
        backward_path = backward_visited[intersection]
        
        # The backward path is already reversed, so we can concatenate directly
        return forward_path + backward_path
    
    def _reverse_path(self, path: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Reverses a path by swapping source and destination pegs and reversing order.
        
        Args:
            path: List of moves to reverse
            
        Returns:
            Reversed path
        """
        return [(to_peg, from_peg, num_disks) for from_peg, to_peg, num_disks in reversed(path)]
 