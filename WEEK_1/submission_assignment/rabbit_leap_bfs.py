import collections

# --- Constants ---
E_RABBIT, W_RABBIT, SPACE = 'E', 'W', '_'
GOAL_STATE = ('W', 'W', 'W', SPACE, 'E', 'E', 'E')

# --- Core Functions ---
def reconstruct_path(parents, start, goal):
    """Rebuilds the solution path from the goal back to the start state."""
    path = []
    current = goal
    if current not in parents: return None
        
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    return path

def get_possible_moves(state):
    """Calculates all legal moves (slide or jump) from the current state."""
    s_list = list(state)
    empty_idx = s_list.index(SPACE)
    next_states = []
    
    for i in range(len(s_list)):
        rabbit = s_list[i]
        
        # E moves right: Slide (1) or Leap (2)
        if rabbit == E_RABBIT and i < empty_idx and (i == empty_idx - 1 or i == empty_idx - 2):
            new_s = s_list[:]
            new_s[empty_idx], new_s[i] = new_s[i], new_s[empty_idx]
            next_states.append(tuple(new_s))
        
        # W moves left: Slide (1) or Leap (2)
        elif rabbit == W_RABBIT and i > empty_idx and (i == empty_idx + 1 or i == empty_idx + 2):
            new_s = s_list[:]
            new_s[empty_idx], new_s[i] = new_s[i], new_s[empty_idx]
            next_states.append(tuple(new_s))
                
    return next_states

def solve_bfs(start, goal):
    """BFS finds the optimal (shortest) path and returns the path and nodes explored."""
    queue = collections.deque([start])
    parents = {start: None}
    nodes_explored = 0
    
    while queue:
        current = queue.popleft()
        nodes_explored += 1  # Increment count as we explore (dequeue) the node
        
        if current == goal:
            return reconstruct_path(parents, start, goal), nodes_explored
        
        for next_s in get_possible_moves(current):
            if next_s not in parents:
                parents[next_s] = current
                queue.append(next_s)
    return None, nodes_explored

# --- Execution ---
def run_bfs_rabbit():
    print("--- Rabbit Leap BFS Solver (Optimal) ---")
    print(f"Goal State: {''.join(GOAL_STATE)}")
    
    user_input = input("Enter starting state (e.g., EEE_WWW): ").strip().upper()
    
    # Input validation
    if len(user_input) != 7 or user_input.count(SPACE) != 1 or user_input.count(E_RABBIT) != 3 or user_input.count(W_RABBIT) != 3:
        print("Invalid state. Needs 3 E's, 3 W's, and 1 '_'.")
        return
    
    initial_s = tuple(user_input)
    print(f"\nStarting search from: {''.join(initial_s)}")
    
    path, explored_count = solve_bfs(initial_s, GOAL_STATE)

    if path:
        print(f"\nBFS found the optimal solution in {len(path) - 1} steps:")
        for i, state in enumerate(path):
            print(f"Step {i:02d}: {''.join(state)}")
        print(f"\n Total Nodes Explored: {explored_count}")
    else:
        print("\nNo solution found from this starting state.")

if __name__ == "__main__":
    run_bfs_rabbit()
