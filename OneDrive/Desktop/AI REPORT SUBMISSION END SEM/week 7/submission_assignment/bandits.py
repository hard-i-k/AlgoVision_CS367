import numpy as np
import random

# reproducibility not set here; set in runner script if desired

# ---------------- BINARY BANDIT ---------------- #
class BinaryBandit:
    def __init__(self, p):
        assert len(p) == 2
        self.p = p  # success probs [p0, p1]

    def pull(self, action):
        return 1 if random.random() < self.p[action] else 0

def epsilon_greedy_bandit(env, steps=1000, epsilon=0.1):
    Q = [0.0, 0.0]
    N = [0, 0]
    rewards = []

    for t in range(steps):
        if random.random() < epsilon:
            action = random.choice([0, 1])
        else:
            action = int(np.argmax(Q))

        r = env.pull(action)
        N[action] += 1
        Q[action] += (1 / N[action]) * (r - Q[action])
        rewards.append(r)

    return rewards

# ---------------- 10-ARM NON-STATIONARY BANDIT ---------------- #
class NonStationaryBandit:
    def __init__(self, k=10):
        self.k = k
        # start all means equal to zero
        self.means = np.zeros(k)

    def step(self):
        # independent random walks
        self.means += np.random.normal(0, 0.01, self.k)

    def pull(self, action):
        # reward drawn from normal with mean = current bandit mean, sigma=1
        return np.random.normal(self.means[action], 1)

def epsilon_greedy_sample_avg(env, steps=10000, epsilon=0.1):
    Q = np.zeros(env.k)
    N = np.zeros(env.k)
    rewards = []
    optimal = []

    for t in range(steps):
        env.step()
        if random.random() < epsilon:
            action = np.random.randint(0, env.k)
        else:
            action = int(np.argmax(Q))

        r = env.pull(action)
        N[action] += 1
        Q[action] += (1 / N[action]) * (r - Q[action])

        rewards.append(r)
        optimal.append(action == int(np.argmax(env.means)))

    return rewards, optimal

def epsilon_greedy_constant_alpha(env, steps=10000, epsilon=0.1, alpha=0.1):
    Q = np.zeros(env.k)
    rewards = []
    optimal = []

    for t in range(steps):
        env.step()
        if random.random() < epsilon:
            action = np.random.randint(0, env.k)
        else:
            action = int(np.argmax(Q))

        r = env.pull(action)
        Q[action] += alpha * (r - Q[action])

        rewards.append(r)
        optimal.append(action == int(np.argmax(env.means)))

    return rewards, optimal

def epsilon_greedy_constant_alpha_optimistic(env, steps=10000, epsilon=0.1, alpha=0.1, Q0=5.0):
    Q = np.ones(env.k) * Q0
    rewards = []
    optimal = []

    for t in range(steps):
        env.step()
        if random.random() < epsilon:
            action = np.random.randint(0, env.k)
        else:
            action = int(np.argmax(Q))

        r = env.pull(action)
        Q[action] += alpha * (r - Q[action])

        rewards.append(r)
        optimal.append(action == int(np.argmax(env.means)))

    return rewards, optimal


def modified_epsilon_greedy(env, steps=10000, epsilon=0.1, alpha=0.1):
    """
    Modified epsilon-greedy for NON-STATIONARY bandits.
    Uses constant step-size alpha instead of sample average,
    allowing fast adaptation to drifting reward means.
    """
    Q = np.zeros(env.k)
    rewards = []
    optimal = []

    for t in range(steps):
        # non-stationary drift every step
        env.step()

        # epsilon-greedy selection
        if random.random() < epsilon:
            action = np.random.randint(0, env.k)
        else:
            action = int(np.argmax(Q))

        # observe reward
        r = env.pull(action)

        # CONSTANT-STEP-SIZE UPDATE (Modified!)
        Q[action] += alpha * (r - Q[action])

        # record data
        rewards.append(r)
        optimal.append(action == int(np.argmax(env.means)))

    return rewards, optimal
