# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

"""
Implements a parallel bidirectional BFS solver using multi-threading.
"""
from typing import List, Dict, Optional, TYPE_CHECKING, Tuple, Any
from collections import deque
import threading
import time
import sys
import os

# Add the parent directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from solvers.base_solver import BaseSolver

if TYPE_CHECKING:
    from ...hanoi_state import HanoiState

class ParallelBidirectionalBFSSolver(BaseSolver):
    """
    A solver that uses parallel bidirectional BFS with multi-threading.
    
    This solver runs forward and backward searches in separate threads to
    exploit multi-core hardware while avoiding the overhead of inter-process
    communication. It uses thread-safe data structures for coordination.
    """
    
    def __init__(self, initial_state: 'HanoiState', target_state: 'HanoiState'):
        super().__init__(initial_state, target_state)
        
        # Thread-safe shared data structures
        self._forward_visited = {}  # Dict[HanoiState, List[move]]
        self._backward_visited = {}  # Dict[HanoiState, List[move]]
        self._forward_lock = threading.Lock()
        self._backward_lock = threading.Lock()
        
        # Solution sharing
        self._solution = None
        self._solution_lock = threading.Lock()
        
        # Thread coordination
        self._solution_found = threading.Event()
        self._threads_finished = threading.Event()
        
        # Statistics from both threads
        self._forward_stats = {'generated': 0, 'explored': 0, 'max_queue_size': 0}
        self._backward_stats = {'generated': 0, 'explored': 0, 'max_queue_size': 0}
        self._stats_lock = threading.Lock()
    
    def _solve_internal(self, max_liftable_disks: int = 1) -> List[Tuple[int, int, int]]:
        """
        Performs parallel bidirectional BFS to find the optimal solution.
        
        Args:
            max_liftable_disks: The max number of disks that can be lifted at once.
            
        Returns:
            A list of moves representing the shortest solution path.
        """
        # Reset state for this solve
        self._forward_visited.clear()
        self._backward_visited.clear()
        self._solution = None
        self._solution_found.clear()
        self._threads_finished.clear()
        self._forward_stats = {'generated': 0, 'explored': 0, 'max_queue_size': 0}
        self._backward_stats = {'generated': 0, 'explored': 0, 'max_queue_size': 0}
        
        # Initialize visited dictionaries with start states
        self._forward_visited[self.initial_state] = []
        self._backward_visited[self.target_state] = []
        
        # Track initial state generation
        self._stats_node_generated()  # Initial state
        self._stats_node_generated()  # Target state
        
        # Create and start threads
        forward_thread = threading.Thread(
            target=self._search_forward,
            args=(max_liftable_disks,),
            name="ForwardSearch"
        )
        
        backward_thread = threading.Thread(
            target=self._search_backward,
            args=(max_liftable_disks,),
            name="BackwardSearch"
        )
        
        forward_thread.start()
        backward_thread.start()
        
        # Adaptive intersection checking with exponentially increasing intervals
        timeout = 60.0  # 60 second timeout
        check_interval = 1e-6  # Start at 1 microsecond
        interval_multiplier = 1.2  # Increase by 20% each time
        max_interval = 1.0  # Cap at 1 second
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check if both threads are still alive
            if not forward_thread.is_alive() and not backward_thread.is_alive():
                break
                
            # Check for intersections
            if self._check_for_intersections():
                # Found intersections, signal threads to stop
                self._solution_found.set()
                break
                
            # Sleep for current interval
            time.sleep(check_interval)
            
            # Increase interval for next check (adaptive timing)
            check_interval = min(check_interval * interval_multiplier, max_interval)
        
        # Signal threads to stop if they haven't already
        self._solution_found.set()
        
        # Wait for threads to finish
        forward_thread.join(timeout=5.0)
        backward_thread.join(timeout=5.0)
        
        # Find optimal solution among all intersections
        optimal_solution = self._find_optimal_solution()
        
        # Collect final statistics
        with self._stats_lock:
            for _ in range(self._forward_stats['generated']):
                self._stats_node_generated()
            for _ in range(self._forward_stats['explored']):
                self._stats_node_explored()
            for _ in range(self._backward_stats['generated']):
                self._stats_node_generated()
            for _ in range(self._backward_stats['explored']):
                self._stats_node_explored()
        
        # Return solution or raise error
        if optimal_solution is not None:
            return optimal_solution
        else:
            raise RuntimeError("Parallel bidirectional BFS timed out without finding a solution.")
    
    def _check_for_intersections(self) -> bool:
        """
        Check if there are any intersections between forward and backward searches.
        
        Returns:
            True if intersections are found, False otherwise.
        """
        try:
            # Quick check without full intersection computation
            with self._forward_lock:
                forward_states = set(self._forward_visited.keys())
            with self._backward_lock:
                backward_states = set(self._backward_visited.keys())
            
            return bool(forward_states & backward_states)
        except:
            return False
    
    def _find_optimal_solution(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find the optimal solution among all intersection states.
        
        Returns:
            The optimal solution path, or None if no intersections found.
        """
        try:
            # Get snapshots of both visited dictionaries
            with self._forward_lock:
                forward_visited = dict(self._forward_visited)
            with self._backward_lock:
                backward_visited = dict(self._backward_visited)
            
            # Find all intersection states
            forward_states = set(forward_visited.keys())
            backward_states = set(backward_visited.keys())
            intersection_states = forward_states & backward_states
            
            if not intersection_states:
                return None
            
            # Find the intersection state that gives the shortest total path
            best_total_length = float('inf')
            best_solution = None
            
            for state in intersection_states:
                forward_path = forward_visited[state]
                backward_path = backward_visited[state]
                total_length = len(forward_path) + len(backward_path)
                
                if total_length < best_total_length:
                    best_total_length = total_length
                    # Reverse the backward path moves
                    reversed_backward = [(to_p, from_p, num_d) for from_p, to_p, num_d in reversed(backward_path)]
                    best_solution = forward_path + reversed_backward
            
            return best_solution
            
        except Exception as e:
            return None
    
    def _search_forward(self, max_liftable_disks: int) -> None:
        """
        Forward search thread that explores from initial state toward target.
        
        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.
        """
        try:
            queue = deque([(self.initial_state, [])])
            local_generated = 0
            local_explored = 0
            local_max_queue_size = 1  # Track local maximum queue size
            
            while queue and not self._solution_found.is_set():
                # Update local maximum queue size (no synchronization needed)
                local_max_queue_size = max(local_max_queue_size, len(queue))
                current_state, path = queue.popleft()
                local_explored += 1
                
                # Generate successors
                possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
                for from_peg, to_peg, num_disks in possible_moves:
                    if self._solution_found.is_set():
                        break
                        
                    try:
                        next_state = current_state.apply_move(from_peg, to_peg, num_disks)
                        
                        # Check if we've seen this state in forward search
                        with self._forward_lock:
                            if next_state not in self._forward_visited:
                                new_path = path + [(from_peg, to_peg, num_disks)]
                                self._forward_visited[next_state] = new_path
                                queue.append((next_state, new_path))
                                local_generated += 1
                                
                    except ValueError:
                        continue
            
            # Update statistics
            with self._stats_lock:
                self._forward_stats['generated'] += local_generated
                self._forward_stats['explored'] += local_explored
                self._forward_stats['max_queue_size'] = local_max_queue_size
                
        except Exception as e:
            # Signal other thread to stop
            self._solution_found.set()
    
    def _search_backward(self, max_liftable_disks: int) -> None:
        """
        Backward search thread that explores from target state toward initial.
        
        Args:
            max_liftable_disks: Maximum number of disks that can be lifted at once.
        """
        try:
            queue = deque([(self.target_state, [])])
            local_generated = 0
            local_explored = 0
            local_max_queue_size = 1  # Track local maximum queue size
            
            while queue and not self._solution_found.is_set():
                # Update local maximum queue size (no synchronization needed)
                local_max_queue_size = max(local_max_queue_size, len(queue))
                current_state, path = queue.popleft()
                local_explored += 1
                
                # Generate predecessors (reverse moves)
                possible_moves = self._get_possible_moves(current_state, max_liftable_disks)
                for from_peg, to_peg, num_disks in possible_moves:
                    if self._solution_found.is_set():
                        break
                        
                    try:
                        # For backward search, we apply the reverse move to get predecessors
                        prev_state = current_state.apply_move(to_peg, from_peg, num_disks)
                        
                        # Check if we've seen this state in backward search
                        with self._backward_lock:
                            if prev_state not in self._backward_visited:
                                new_path = [(from_peg, to_peg, num_disks)] + path
                                self._backward_visited[prev_state] = new_path
                                queue.append((prev_state, new_path))
                                local_generated += 1
                                
                    except ValueError:
                        continue
            
            # Update statistics
            with self._stats_lock:
                self._backward_stats['generated'] += local_generated
                self._backward_stats['explored'] += local_explored
                self._backward_stats['max_queue_size'] = local_max_queue_size
                
        except Exception as e:
            # Signal other thread to stop
            self._solution_found.set()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get detailed statistics about the parallel search process.
        
        Returns:
            A dictionary containing statistics about the search.
        """
        base_stats = super().get_stats()
        
        # Calculate upper bound for combined data structure size
        max_combined_size = self._forward_stats['max_queue_size'] + self._backward_stats['max_queue_size']
        
        base_stats.update({
            'algorithm_name': 'Parallel Bidirectional BFS',
            'forward_generated': self._forward_stats['generated'],
            'forward_explored': self._forward_stats['explored'],
            'forward_max_queue_size': self._forward_stats['max_queue_size'],
            'backward_generated': self._backward_stats['generated'],
            'backward_explored': self._backward_stats['explored'], 
            'backward_max_queue_size': self._backward_stats['max_queue_size'],
            'max_data_structure_size_upper_bound': max_combined_size
        })
        return base_stats

 