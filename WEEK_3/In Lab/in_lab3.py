import heapq

class BoardNode:
    """Represents a single node in the search tree."""
    def __init__(self, board, parent=None, cost=0, heuristic=0):
        self.board = board
        self.parent = parent
        self.g = cost             # actual path cost
        self.h = heuristic        # estimated cost to goal
        self.f = self.g + self.h  # total cost (A* priority)

    def __lt__(self, other):
        return self.f < other.f


def valid_moves(board):
    """Finds all possible legal moves for the current board configuration."""
    all_moves = []
    steps = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # move 2 steps
    jumps = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # jump over one

    for r in range(7):
        for c in range(7):
            if board[r][c] != 'O': 
                continue
            for (dr, dc), (jr, jc) in zip(steps, jumps):
                new_r, new_c = r + dr, c + dc
                mid_r, mid_c = r + jr, c + jc
                if not (0 <= new_r < 7 and 0 <= new_c < 7):
                    continue
                if board[mid_r][mid_c] == 'O' and board[new_r][new_c] == '0':
                    all_moves.append((r, c, new_r, new_c))
    return all_moves


def make_move(board, move):
    """Applies a given move and returns the new board state."""
    new_board = [row[:] for row in board]
    sr, sc, er, ec = move
    jr, jc = (sr + er) // 2, (sc + ec) // 2

    new_board[sr][sc] = '0'
    new_board[jr][jc] = '0'
    new_board[er][ec] = 'O'
    return new_board


def one_marble_left(board):
    """Checks if the goal state (only one marble remaining) is reached."""
    return sum(row.count('O') for row in board) == 1


def marble_count_heuristic(board):
    """Heuristic 1: number of marbles remaining."""
    return sum(row.count('O') for row in board)


def distance_to_center_heuristic(board):
    """Heuristic 2: sum of Manhattan distances of all marbles from the center."""
    cx, cy = 3, 3
    total = 0
    for r in range(7):
        for c in range(7):
            if board[r][c] == 'O':
                total += abs(r - cx) + abs(c - cy)
    return total


def greedy_best_first(board, heuristic_fn):
    """Implements Greedy Best-First Search."""
    start_h = heuristic_fn(board)
    start = BoardNode(board, heuristic=start_h)
    frontier = [(start.h, start)]
    explored = set()
    max_frontier = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        state_tuple = tuple(map(tuple, current.board))
        if state_tuple in explored:
            continue
        explored.add(state_tuple)

        if len(frontier) > max_frontier:
            max_frontier = len(frontier)

        if one_marble_left(current.board):
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            print("\n--- Greedy Best-First Search ---")
            print("Visited nodes:", len(explored))
            print("Max queue size:", max_frontier)
            print("Path length:", len(path))
            return path[::-1]

        for mv in valid_moves(current.board):
            child_board = make_move(current.board, mv)
            h_val = heuristic_fn(child_board)
            child = BoardNode(child_board, current, heuristic=h_val)
            heapq.heappush(frontier, (child.h, child))
    return None


def a_star_solver(board, heuristic_fn):
    """Implements the A* search algorithm."""
    start_h = heuristic_fn(board)
    start = BoardNode(board, cost=0, heuristic=start_h)
    frontier = [(start.f, start)]
    explored = set()
    max_frontier = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        state_tuple = tuple(map(tuple, current.board))
        if state_tuple in explored:
            continue
        explored.add(state_tuple)

        if len(frontier) > max_frontier:
            max_frontier = len(frontier)

        if one_marble_left(current.board):
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            print("\n--- A* Search ---")
            print("Visited nodes:", len(explored))
            print("Max queue size:", max_frontier)
            print("Path length:", len(path))
            return path[::-1]

        for mv in valid_moves(current.board):
            new_board = make_move(current.board, mv)
            g_val = current.g + 1
            h_val = heuristic_fn(new_board)
            child = BoardNode(new_board, current, g_val, h_val)
            heapq.heappush(frontier, (child.f, child))
    return None


# ---- Initial Configuration ----
initial_board = [
    ['-', '-', 'O', 'O', 'O', '-', '-'],
    ['-', '-', 'O', 'O', 'O', '-', '-'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', '0', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['-', '-', 'O', 'O', 'O', '-', '-'],
    ['-', '-', 'O', 'O', 'O', '-', '-']
]

print("Initial possible moves:")
for mv in valid_moves(initial_board):
    print(f"{mv[0], mv[1]} → {mv[2], mv[3]}")

# Run both algorithms
greedy_best_first(initial_board, distance_to_center_heuristic)
a_star_solver(initial_board, distance_to_center_heuristic)
