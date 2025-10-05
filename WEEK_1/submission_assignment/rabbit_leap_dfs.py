# --- Constants ---
E_RABBIT, W_RABBIT, SPACE = 'E', 'W', '_'
GOAL_STATE = ('W', 'W', 'W', SPACE, 'E', 'E', 'E')

# --- Core Functions ---
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

def solve_dfs(current, goal, visited, path, explored_count):
    """DFS finds a path (not guaranteed optimal) using recursion."""
    
    # The 'visited' set is tracking explored nodes.
    # The initial state is explored when the function is first called.
    explored_count[0] += 1
    
    if current == goal:
        return path + [current], explored_count[0]
    
    visited.add(current)
    
    # Sort successors for a consistent path
    for next_s in sorted(get_possible_moves(current)):
        if next_s not in visited:
            # Recursive call
            result, count = solve_dfs(next_s, goal, visited, path + [current], explored_count)
            if result:
                return result, count
    return None, explored_count[0]

# --- Execution ---
def run_dfs_rabbit():
   
    print(f"Goal State: {''.join(GOAL_STATE)}")
    
    user_input = input("Enter starting state (e.g., EEE_WWW): ").strip().upper()
    
    # Input validation
    if len(user_input) != 7 or user_input.count(SPACE) != 1 or user_input.count(E_RABBIT) != 3 or user_input.count(W_RABBIT) != 3:
        print("Invalid state. Needs 3 E's, 3 W's, and 1 '_'.")
        return
    
    initial_s = tuple(user_input)
    print(f"\nStarting search from: {''.join(initial_s)}")
    
    # explored_count is passed as a mutable list [0] to track the count across recursive calls
    path, explored_count = solve_dfs(initial_s, GOAL_STATE, set(), [], [0])

    if path:
        print(f"\nDFS found a solution in {len(path) - 1} steps:")
        for i, state in enumerate(path):
            print(f"Step {i:02d}: {''.join(state)}")
        print(f"\n Total Nodes Explored: {explored_count}")
    else:
        print("\nNo solution found from this starting state.")

if __name__ == "__main__":
    run_dfs_rabbit()
