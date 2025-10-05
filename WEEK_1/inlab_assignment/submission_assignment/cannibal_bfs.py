import collections

# --- Constants ---
MC_GOAL_STATE = (0, 0, 0)
BOAT_MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)] # (M, C) to move

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

def is_safe(m, c):
    """Checks if a bank state is safe (M not outnumbered by C)."""
    return (m == 0) or (m >= c)

def get_successors(state):
    M1, C1, B = state
    M2, C2 = 3 - M1, 3 - C1
    next_states = []
    
    for dm, dc in BOAT_MOVES:
        if B == 1:  # Left -> Right
            nM1, nC1, nB = M1 - dm, C1 - dc, 0
            nM2, nC2 = M2 + dm, C2 + dc
            if M1 >= dm and C1 >= dc and is_safe(nM1, nC1) and is_safe(nM2, nC2):
                next_states.append((nM1, nC1, nB))
        else:  # Right -> Left
            nM1, nC1, nB = M1 + dm, C1 + dc, 1
            nM2, nC2 = M2 - dm, C2 - dc
            if M2 >= dm and C2 >= dc and is_safe(nM1, nC1) and is_safe(nM2, nC2):
                next_states.append((nM1, nC1, nB))
    return next_states

def solve_bfs(start, goal):
    """BFS finds the optimal (shortest) path and returns the path and nodes explored."""
    queue = collections.deque([start])
    parents = {start: None}
    nodes_explored = 0
    
    while queue:
        current = queue.popleft()
        nodes_explored += 1 # Increment count as we explore (dequeue) the node
        
        if current == goal:
            return reconstruct_path(parents, start, goal), nodes_explored
        
        for next_s in get_successors(current):
            if next_s not in parents:
                parents[next_s] = current
                queue.append(next_s)
    return None, nodes_explored

# --- Execution ---
def run_bfs_mc():
    print(" Missionaries and Cannibals BFS Solver")
    print(f"Goal State: {MC_GOAL_STATE} (0 M, 0 C, Boat Right)")
    
    user_input = input("Enter starting state (M1, C1, B, e.g., 3,3,1): ").strip()
    
    try:
        M1, C1, B = map(int, user_input.split(','))
        initial_s = (M1, C1, B)
        
        if not (0 <= M1 <= 3 and 0 <= C1 <= 3 and B in [0, 1]): raise ValueError
        if not is_safe(M1, C1) or not is_safe(3 - M1, 3 - C1):
             print("Error: The initial state is unsafe or invalid.")
             return
            
    except (ValueError, IndexError):
        print("Invalid format. Please enter M1,C1,B (e.g., 3,3,1).")
        return
        
    print(f"\nStarting search from: {initial_s}")
    
    path, explored_count = solve_bfs(initial_s, MC_GOAL_STATE)

    if path:
        print(f"\nBFS found the optimal solution in {len(path) - 1} steps:")
        for i, (m1, c1, b) in enumerate(path):
            m2, c2 = 3 - m1, 3 - c1
            print(f"Step {i:02d}: Bank 1 ({m1}M, {c1}C) | Bank 2 ({m2}M, {c2}C) | Boat: {'Left' if b == 1 else 'Right'}")
        print(f"\n Total Nodes Explored: {explored_count} ")
    else:
        print("\nNo solution found from this starting state.")

if __name__ == "__main__":
    run_bfs_mc()
