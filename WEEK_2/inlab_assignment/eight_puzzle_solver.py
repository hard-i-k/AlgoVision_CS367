

import numpy as np
import time
import heapq
from collections import deque
import matplotlib.pyplot as plt


class PuzzleState:
    """
    Represents a state in the 8-puzzle game
    Contains the board configuration and metadata for search
    """
    def __init__(self, board_config, parent_state=None, move_cost=0, estimated_cost=0, action_taken=None):
        self.board_config = np.array(board_config)
        self.parent_state = parent_state
        self.move_cost = move_cost  # g(n) - cost from start
        self.estimated_cost = estimated_cost  # h(n) - heuristic estimate
        self.total_cost = move_cost + estimated_cost  # f(n) = g(n) + h(n)
        self.action_taken = action_taken
        self.state_id = self._generate_state_hash()

    def _generate_state_hash(self):
        """Generate unique hash for the state"""
        return hash(tuple(self.board_config.flatten()))

    def __eq__(self, other_state):
        """Check if two states are equal"""
        return np.array_equal(self.board_config, other_state.board_config)

    def __lt__(self, other_state):
        """Comparison for priority queue ordering"""
        return self.total_cost < other_state.total_cost

    def __hash__(self):
        """Hash function for storing in sets/dictionaries"""
        return self.state_id

    def __str__(self):
        """String representation of the state"""
        return str(self.board_config)

    def find_blank_position(self):
        """Find the position of the blank tile (represented as 0)"""
        blank_pos = np.where(self.board_config == 0)
        return (blank_pos[0][0], blank_pos[1][0])


class SearchQueue:
    """
    Custom priority queue implementation for search algorithms
    Supports both FIFO (BFS) and priority-based (A*) operations
    """
    def __init__(self, queue_type="priority"):
        self.queue_type = queue_type
        if queue_type == "priority":
            self.container = []
        elif queue_type == "fifo":
            self.container = deque()
        else:
            self.container = []  # Default to list for LIFO

    def add_state(self, puzzle_state):
        """Add a state to the queue"""
        if self.queue_type == "priority":
            heapq.heappush(self.container, puzzle_state)
        elif self.queue_type == "fifo":
            self.container.append(puzzle_state)
        else:  # LIFO for DFS
            self.container.append(puzzle_state)

    def remove_state(self):
        """Remove and return the next state"""
        if self.queue_type == "priority":
            return heapq.heappop(self.container)
        elif self.queue_type == "fifo":
            return self.container.popleft()
        else:  # LIFO for DFS
            return self.container.pop()

    def is_empty(self):
        """Check if queue is empty"""
        return len(self.container) == 0

    def size(self):
        """Get current queue size"""
        return len(self.container)


class PuzzleEnvironment:
    """
    Environment class that handles the 8-puzzle game mechanics
    Generates states, validates moves, and checks goal conditions
    """
    def __init__(self, target_depth=None, target_state=None):
        self.possible_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.target_state = target_state if target_state is not None else self._get_default_goal()
        self.target_depth = target_depth
        self.initial_state = self._create_initial_state()

    def _get_default_goal(self):
        """Default goal state for 8-puzzle"""
        return np.array([[1, 2, 3],
                        [4, 5, 6], 
                        [7, 8, 0]])

    def _create_initial_state(self):
        """Generate initial state by scrambling from goal state"""
        if self.target_depth is None:
            return self._get_random_solvable_state()
        
        current_state = np.copy(self.target_state)
        depth_count = 0
        
        while depth_count < self.target_depth:
            possible_states = self.generate_successor_states(current_state)
            # Randomly select next state but avoid returning to previous state
            selected_state = np.random.choice(len(possible_states))
            
            if not np.array_equal(possible_states[selected_state], current_state):
                current_state = possible_states[selected_state]
                depth_count += 1
        
        return current_state

    def _get_random_solvable_state(self):
        """Generate a random solvable 8-puzzle state"""
        # Simple implementation: scramble goal state with random moves
        state = np.copy(self.target_state)
        for _ in range(100):  # 100 random moves
            successors = self.generate_successor_states(state)
            if successors:
                state = successors[np.random.randint(len(successors))]
        return state

    def get_initial_state(self):
        """Return the initial puzzle state"""
        return self.initial_state

    def get_target_state(self):
        """Return the target/goal puzzle state"""
        return self.target_state

    def generate_successor_states(self, current_state):
        """
        Generate all possible successor states from current state
        Returns list of valid board configurations
        """
        successors = []
        blank_row, blank_col = self._find_blank_tile(current_state)

        # Define possible moves: [row_delta, col_delta]
        move_directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        for action, (row_delta, col_delta) in move_directions.items():
            new_row = blank_row + row_delta
            new_col = blank_col + col_delta

            # Check if move is within bounds
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Create new state by swapping blank with adjacent tile
                new_state = np.copy(current_state)
                new_state[blank_row, blank_col] = new_state[new_row, new_col]
                new_state[new_row, new_col] = 0  # 0 represents blank
                
                successors.append(new_state)

        return successors

    def _find_blank_tile(self, state):
        """Find position of blank tile (0) in the puzzle"""
        blank_position = np.where(state == 0)
        return blank_position[0][0], blank_position[1][0]

    def is_goal_reached(self, current_state):
        """Check if current state matches the target state"""
        return np.array_equal(current_state, self.target_state)


class GraphSearchAgent:
    """
    Graph search agent implementing various search algorithms
    Includes A*, BFS, DFS, and Iterative Deepening Search
    """
    def __init__(self, environment, heuristic_function, search_algorithm="astar"):
        self.frontier_queue = SearchQueue("priority" if search_algorithm == "astar" else "fifo")
        self.explored_states = {}  # Hash table for visited states
        self.initial_state = environment.get_initial_state()
        self.target_state = environment.get_target_state()
        self.environment = environment
        self.solution_node = None
        self.heuristic_function = heuristic_function
        self.search_algorithm = search_algorithm
        self.nodes_expanded = 0
        self.max_frontier_size = 0

    def execute_search(self):
        """
        Main search execution method
        Returns: (nodes_expanded, solution_depth, time_taken, memory_used)
        """
        start_time = time.time()
        
        if self.search_algorithm == "iterative_deepening":
            return self._iterative_deepening_search()
        else:
            return self._graph_search()

    def _graph_search(self):
        """Standard graph search implementation"""
        # Initialize with starting state
        initial_node = PuzzleState(
            board_config=self.initial_state,
            parent_state=None,
            move_cost=0,
            estimated_cost=self.heuristic_function(self.initial_state, self.target_state)
        )
        
        self.frontier_queue.add_state(initial_node)
        self.nodes_expanded = 0

        while not self.frontier_queue.is_empty():
            # Track memory usage
            current_frontier_size = self.frontier_queue.size()
            if current_frontier_size > self.max_frontier_size:
                self.max_frontier_size = current_frontier_size

            # Get next state to explore
            current_node = self.frontier_queue.remove_state()

            # Skip if already explored
            if current_node.state_id in self.explored_states:
                continue

            # Mark as explored
            self.explored_states[current_node.state_id] = current_node
            self.nodes_expanded += 1

            # Check if goal reached
            if self.environment.is_goal_reached(current_node.board_config):
                self.solution_node = current_node
                break

            # Generate and add successor states
            successor_states = self.environment.generate_successor_states(current_node.board_config)
            
            for successor_config in successor_states:
                successor_node = PuzzleState(
                    board_config=successor_config,
                    parent_state=current_node,
                    move_cost=current_node.move_cost + 1,
                    estimated_cost=self.heuristic_function(successor_config, self.target_state)
                )
                
                # Add to frontier if not already explored
                if successor_node.state_id not in self.explored_states:
                    self.frontier_queue.add_state(successor_node)

        solution_depth = self._calculate_solution_depth()
        memory_usage = self._calculate_memory_usage()
        
        return self.nodes_expanded, solution_depth, memory_usage

    def _iterative_deepening_search(self):
        """
        Iterative Deepening Search Implementation
        
        IDS combines the space-efficiency of DFS with the optimality of BFS.
        It performs a series of depth-limited searches with increasing depth limits.
        """
        print("Executing Iterative Deepening Search...")
        
        max_depth = 50  # Maximum depth to search
        total_nodes_expanded = 0
        
        for depth_limit in range(max_depth):
            print(f"Searching at depth limit: {depth_limit}")
            
            # Reset for each depth-limited search
            self.explored_states = {}
            self.frontier_queue = SearchQueue("fifo")  # Use FIFO for BFS-like behavior
            self.nodes_expanded = 0
            
            # Perform depth-limited search
            result = self._depth_limited_search(depth_limit)
            total_nodes_expanded += self.nodes_expanded
            
            if result is not None:  # Solution found
                print(f"Solution found at depth: {depth_limit}")
                return total_nodes_expanded, depth_limit + 1, self._calculate_memory_usage()
        
        print("No solution found within maximum depth")
        return total_nodes_expanded, -1, self._calculate_memory_usage()

    def _depth_limited_search(self, depth_limit):
        """Perform depth-limited search up to specified depth"""
        initial_node = PuzzleState(
            board_config=self.initial_state,
            move_cost=0,
            estimated_cost=0
        )
        
        return self._recursive_dls(initial_node, depth_limit)

    def _recursive_dls(self, current_node, depth_limit):
        """Recursive depth-limited search helper"""
        self.nodes_expanded += 1
        
        # Check if goal reached
        if self.environment.is_goal_reached(current_node.board_config):
            self.solution_node = current_node
            return current_node
        
        # Check depth limit
        if current_node.move_cost >= depth_limit:
            return None
        
        # Explore successors
        successor_states = self.environment.generate_successor_states(current_node.board_config)
        
        for successor_config in successor_states:
            successor_node = PuzzleState(
                board_config=successor_config,
                parent_state=current_node,
                move_cost=current_node.move_cost + 1,
                estimated_cost=0
            )
            
            # Avoid cycles by checking if state was visited in current path
            if not self._is_in_path(successor_node, current_node):
                result = self._recursive_dls(successor_node, depth_limit)
                if result is not None:
                    return result
        
        return None

    def _is_in_path(self, state, current_node):
        """Check if state exists in current search path (cycle detection)"""
        node = current_node
        while node is not None:
            if np.array_equal(state.board_config, node.board_config):
                return True
            node = node.parent_state
        return False

    def _calculate_solution_depth(self):
        """Calculate depth of solution path"""
        if self.solution_node is None:
            return -1
        
        depth = 0
        current_node = self.solution_node
        while current_node.parent_state is not None:
            depth += 1
            current_node = current_node.parent_state
        
        return depth

    def _calculate_memory_usage(self):
        """Estimate memory usage in bytes"""
        # Rough estimation: each state uses about 100 bytes
        frontier_memory = self.frontier_queue.size() * 100
        explored_memory = len(self.explored_states) * 100
        return frontier_memory + explored_memory

    def reconstruct_solution_path(self):
        """
        Backtrack from goal to initial state to construct solution path
        Returns list of states representing the solution
        """
        if self.solution_node is None:
            return []
        
        solution_path = []
        current_node = self.solution_node
        
        while current_node is not None:
            solution_path.append(current_node)
            current_node = current_node.parent_state
        
        return solution_path[::-1]  # Reverse to get path from start to goal

    def print_solution_path(self):
        """Print the complete solution path"""
        path = self.reconstruct_solution_path()
        
        if not path:
            print("No solution found!")
            return
        
        print(f"Solution found in {len(path) - 1} steps:")
        
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print(state.board_config)
            print("-" * 20)

    def get_performance_metrics(self):
        """Return performance metrics for analysis"""
        return {
            'nodes_expanded': self.nodes_expanded,
            'solution_depth': self._calculate_solution_depth(),
            'memory_usage': self._calculate_memory_usage(),
            'max_frontier_size': self.max_frontier_size
        }


# Heuristic Functions
def null_heuristic(current_state, goal_state):
    """
    Null heuristic (always returns 0)
    Used for uniform cost search / Dijkstra's algorithm
    """
    return 0


def misplaced_tiles_heuristic(current_state, goal_state):
    """
    Counts number of misplaced tiles (excluding blank)
    Admissible heuristic for A* search
    """
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if current_state[i, j] != 0 and current_state[i, j] != goal_state[i, j]:
                misplaced += 1
    return misplaced


def manhattan_distance_heuristic(current_state, goal_state):
    """
    Manhattan distance heuristic
    Sum of distances each tile is from its goal position
    Admissible and more informed than misplaced tiles
    """
    total_distance = 0
    
    for i in range(3):
        for j in range(3):
            if current_state[i, j] != 0:  # Skip blank tile
                tile_value = current_state[i, j]
                # Find goal position of this tile
                goal_pos = np.where(goal_state == tile_value)
                goal_i, goal_j = goal_pos[0][0], goal_pos[1][0]
                
                # Calculate Manhattan distance
                distance = abs(i - goal_i) + abs(j - goal_j)
                total_distance += distance
    
    return total_distance


def run_performance_analysis():
    """
    Comprehensive performance analysis of the 8-puzzle solver
    Tests various depths and generates performance tables
    """
   
    print("8-PUZZLE SOLVER PERFORMANCE ANALYSIS")
    
    # Test parameters
    test_depths = [0,20,40,60,80,100,120,140,160,180,200]
    goal_configuration = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    num_trials = 10  # Number of trials per depth for averaging
    
    # Results storage
    performance_results = {
        'depth': [],
        'avg_nodes_expanded': [],
        'avg_time': [],
        'avg_memory': [],
        'success_rate': []
    }
    
    print(f"Testing depths: {test_depths}")
    print(f"Trials per depth: {num_trials}")
    print(f"Heuristic: Manhattan Distance")
    print("Testing depths...")
    
    for depth in test_depths:
        print(f"Testing depth {depth}...")
        
        total_nodes = 0
        total_time = 0
        total_memory = 0
        successful_solves = 0
        
        for trial in range(num_trials):
            try:
                # Create environment with specific depth
                environment = PuzzleEnvironment(target_depth=depth, target_state=goal_configuration)
                
                # Create agent with Manhattan distance heuristic
                agent = GraphSearchAgent(
                    environment=environment,
                    heuristic_function=manhattan_distance_heuristic,
                    search_algorithm="astar"
                )
                
                # Run search and measure performance
                start_time = time.time()
                nodes_expanded, solution_depth, memory_used = agent.execute_search()
                end_time = time.time()
                
                if agent.solution_node is not None:
                    successful_solves += 1
                    total_nodes += nodes_expanded
                    total_time += (end_time - start_time)
                    total_memory += memory_used
                
            except Exception as e:
                print(f"Error in trial {trial} for depth {depth}: {e}")
        
        # Calculate averages
        if successful_solves > 0:
            avg_nodes = total_nodes / successful_solves
            avg_time = total_time / successful_solves
            avg_memory = total_memory / successful_solves
            success_rate = (successful_solves / num_trials) * 100
        else:
            avg_nodes = avg_time = avg_memory = 0
            success_rate = 0
        
        # Store results
        performance_results['depth'].append(depth)
        performance_results['avg_nodes_expanded'].append(avg_nodes)
        performance_results['avg_time'].append(avg_time)
        performance_results['avg_memory'].append(avg_memory)
        performance_results['success_rate'].append(success_rate)
        
        print(f"Depth {depth}: {avg_nodes:.1f} nodes, {avg_time:.4f}s, {avg_memory:.1f} bytes, {success_rate:.1f}% success")
    
    # Display results table
    print("\nPERFORMANCE ANALYSIS RESULTS")
    
    print(f"{'Depth':<8} {'Nodes':<12} {'Time (s)':<12} {'Memory (B)':<15} {'Success %':<10}")
    
    for i in range(len(performance_results['depth'])):
        depth = performance_results['depth'][i]
        nodes = performance_results['avg_nodes_expanded'][i]
        time_val = performance_results['avg_time'][i]
        memory = performance_results['avg_memory'][i]
        success = performance_results['success_rate'][i]
        
        print(f"{depth:<8} {nodes:<12.1f} {time_val:<12.4f} {memory:<15.1f} {success:<10.1f}")
    
    return performance_results


def demonstrate_iterative_deepening():
    """
    Demonstrate Iterative Deepening Search
    
    Iterative Deepening Search (IDS) is a search strategy that combines
    the space-efficiency of depth-first search with the optimality of
    breadth-first search. It works by performing a series of depth-limited
    searches with increasing depth limits until a solution is found.
    
    Advantages:
    - Space complexity: O(bd) where b is branching factor, d is depth
    - Time complexity: O(b^d) - same as BFS
    - Optimal for uniform step costs
    - Memory efficient compared to BFS
    
    Disadvantages:
    - Redundant work (revisits states at smaller depths)
    - Slower than A* with good heuristic
    """
    print("ITERATIVE DEEPENING SEARCH DEMONSTRATION")
    
    print("Iterative Deepening Search (IDS) Explanation:")
    
    
    # Create a simple puzzle instance
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    environment = PuzzleEnvironment(target_depth=10, target_state=goal_state)
    
    print("Initial State:")
    print(environment.get_initial_state())
    print("\nGoal State:")
    print(goal_state)
    print()
    
    # Run Iterative Deepening Search
    agent = GraphSearchAgent(
        environment=environment,
        heuristic_function=null_heuristic,  # IDS doesn't need heuristic
        search_algorithm="iterative_deepening"
    )
    
    start_time = time.time()
    nodes_expanded, solution_depth, memory_used = agent.execute_search()
    end_time = time.time()
    
    print(f"\nIDS Results:")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Solution depth: {solution_depth}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Memory used: {memory_used} bytes")
    
    if agent.solution_node:
        print("\nSolution path:")
        agent.print_solution_path()


def main():
    print("8-PUZZLE SOLVER WITH GRAPH SEARCH ALGORITHMS")
    print("CS367 - Artificial Intelligence Lab Assignment 2")
    
    # Example 1: Solve a specific puzzle instance
    print("\n1. SOLVING SAMPLE 8-PUZZLE INSTANCE")
    
    
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    environment = PuzzleEnvironment(target_depth=15, target_state=goal_state)
    
    print("Initial State:")
    print(environment.get_initial_state())
    print("\nGoal State:")
    print(goal_state)
    
    # Solve with A* using Manhattan distance heuristic
    agent = GraphSearchAgent(
        environment=environment,
        heuristic_function=manhattan_distance_heuristic,
        search_algorithm="astar"
    )
    
    start_time = time.time()
    nodes_expanded, solution_depth, memory_used = agent.execute_search()
    end_time = time.time()
    
    print(f"\nA* Search Results:")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Solution depth: {solution_depth}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Memory used: {memory_used} bytes")
    
    if agent.solution_node:
        print("\nSolution found! Displaying path...")
        agent.print_solution_path()
    
    # Example 2: Demonstrate Iterative Deepening
    print("\n2. ITERATIVE DEEPENING SEARCH DEMONSTRATION")
    
    demonstrate_iterative_deepening()
    
    # Example 3: Performance analysis
    print("\n3. COMPREHENSIVE PERFORMANCE ANALYSIS")

    performance_data = run_performance_analysis()
    
    print("\nPerformance analysis completed!")
    print("Check the results table above for detailed metrics.")


if __name__ == "__main__":
    main()