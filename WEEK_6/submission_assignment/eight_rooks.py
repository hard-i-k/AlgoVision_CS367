import numpy as np

class HopfieldRooks:
    def __init__(self, n):
        # board size (n x n) and total units
        self.n = n
        self.units = n * n

        # weight matrix and threshold vector
        self.W = np.zeros((self.units, self.units))
        self.th = np.full(self.units, -0.8)   # slightly changed threshold

        # create weights that encode rook constraints
        self.build_W()

    def build_W(self):
        # negative interaction prevents two rooks in same row/column
        penalty = -1.9   

        for r in range(self.n):
            for c in range(self.n):
                idx = r * self.n + c

                # same row conflict
                for c2 in range(self.n):
                    if c2 != c:
                        j = r * self.n + c2
                        self.W[idx, j] = penalty

                # same column conflict
                for r2 in range(self.n):
                    if r2 != r:
                        j = r2 * self.n + c
                        self.W[idx, j] = penalty

        # no self-connection
        np.fill_diagonal(self.W, 0)

    def update(self, s):
        # synchronous full update of all neurons
        for i in range(self.units):
            h = np.dot(self.W[i], s) - self.th[i]
            s[i] = 1 if h > 0 else 0
        return s

    def solve(self, iters=120):
        # random initial state of 0/1 values
        state = np.random.randint(0, 2, self.units)

        for _ in range(iters):
            old = state.copy()
            state = self.update(state)
            if np.array_equal(old, state):  # network converged
                break

        return state


# run the network
n = 8
net = HopfieldRooks(n)
final_state = net.solve().reshape((n, n))

print("Eight-Rooks Board:")
print(final_state)
