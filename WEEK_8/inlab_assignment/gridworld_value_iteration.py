import numpy as np

# Grid definition (3 rows x 4 columns)
# Coordinates: (row, col) starting from top-left (0,0)
# Terminal states:
#  (0,3) = +1
#  (1,3) = -1
# Wall at (1,1)

ROWS = 3
COLS = 4

terminal_states = {(0, 3): 1.0, (1, 3): -1.0}
wall = (1, 1)

ACTIONS = ["U", "D", "L", "R"]
action_vectors = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

# Perpendicular directions for stochasticity (0.1, 0.1)
perp = {
    "U": ["L", "R"],
    "D": ["L", "R"],
    "L": ["U", "D"],
    "R": ["U", "D"],
}

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS and (r, c) != wall

def next_state(r, c, action):
    dr, dc = action_vectors[action]
    nr, nc = r + dr, c + dc
    if in_bounds(nr, nc):
        return (nr, nc)
    return (r, c)

def compute_value_iteration(reward=-0.04, gamma=0.99, theta=1e-4):
    V = np.zeros((ROWS, COLS))

    # Keep terminal states fixed
    for (r, c), val in terminal_states.items():
        V[r, c] = val

    while True:
        delta = 0
        newV = V.copy()

        for r in range(ROWS):
            for c in range(COLS):

                if (r, c) in terminal_states or (r, c) == wall:
                    continue

                values = []

                # Try every action
                for a in ACTIONS:
                    val = 0

                    # 0.8 intended direction
                    nr, nc = next_state(r, c, a)
                    val += 0.8 * (reward + gamma * V[nr, nc])

                    # 0.1 sideways moves
                    for p in perp[a]:
                        nr, nc = next_state(r, c, p)
                        val += 0.1 * (reward + gamma * V[nr, nc])

                    values.append(val)

                newV[r, c] = max(values)
                delta = max(delta, abs(V[r, c] - newV[r, c]))

        V = newV

        if delta < theta:
            break

    return V

def print_grid(V):
    for r in range(ROWS):
        row = ""
        for c in range(COLS):
            if (r, c) == wall:
                row += "  WALL     "
            else:
                row += f"{V[r,c]:8.3f} "
        print(row)
    print()

if __name__ == "__main__":
    rewards = [-2, 0.1, 0.02, 1]

    for r in rewards:
        print(f"\n=========== Reward = {r} ===========")
        V = compute_value_iteration(reward=r)
        print_grid(V)
