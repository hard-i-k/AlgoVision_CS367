import numpy as np

class TSPHopfield:
    def __init__(self, n, dist, lam=420):
        # number of cities and distance matrix
        self.n = n
        self.D = dist
        self.lam = lam

        # total neurons = n × n (city × tour position)
        self.total = n * n

        # weight matrix + thresholds
        self.W = np.zeros((self.total, self.total))
        self.bias = np.zeros(self.total)

        # random initial pattern
        self.state = np.random.randint(0, 2, self.total)

        # build Hopfield weights
        self.build_W()

    def pos(self, city, slot):
        # convert city,position -> neuron index
        return city * self.n + slot

    def build_W(self):
        n = self.n
        L = self.lam

        # penalty constraints for valid tour
        for i in range(n):
            for k in range(n):
                a = self.pos(i, k)

                # rule: each position must have exactly one city
                for j in range(n):
                    if j != i:
                        b = self.pos(j, k)
                        self.W[a, b] -= L

                # rule: each city appears exactly once in tour
                for k2 in range(n):
                    if k2 != k:
                        b = self.pos(i, k2)
                        self.W[a, b] -= L

        # add distance cost between successive positions
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                for k in range(n):
                    a = self.pos(i, k)
                    b = self.pos(j, (k + 1) % n)
                    self.W[a, b] -= self.D[i, j]

        # no self-connections
        np.fill_diagonal(self.W, 0)

        # uniform bias
        self.bias[:] = -L / 2

    def update(self):
        # synchronous update of neurons
        for i in range(self.total):
            h = np.dot(self.W[i], self.state) - self.bias[i]
            self.state[i] = 1 if h > 0 else 0

    def extract_path(self):
        # read final tour (city at each tour position)
        route = []
        for k in range(self.n):
            found = -1
            for i in range(self.n):
                if self.state[self.pos(i, k)] == 1:
                    found = i
                    break
            route.append(found)
        return route

    def solve(self, steps=900):
        # iterate until convergence
        for _ in range(steps):
            prev = self.state.copy()
            self.update()
            if np.array_equal(prev, self.state):
                break
        return self.extract_path()


if __name__ == "__main__":
    n = 10
    np.random.seed(14)

    # symmetric distance matrix
    D = np.random.randint(1, 120, (n, n))
    np.fill_diagonal(D, 0)
    D = (D + D.T) // 2

    net = TSPHopfield(n, D)
    result = net.solve()

    print("TSP Route:", result)
