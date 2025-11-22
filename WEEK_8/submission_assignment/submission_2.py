
import numpy as np
from scipy.stats import poisson

# Core constants (minimal renames from original)
MAX_BIKES = 20
MAX_MOVE = 5  # action bounds
RENTAL_REWARD = 10
MOVE_COST = 2  # cost per bike moved
OVERFLOW_FEE = 4  # parking cost when >10 bikes
DISCOUNT = 0.9

# Demand and return rates (unchanged values)
RENTAL_REQUEST_RATE = [3, 4]
RETURN_RATE = [3, 2]

def poisson_prob(n, lam):
    return poisson.pmf(n, lam)

def compute_expected_value(state, action, value_fn):
    bikes1 = min(MAX_BIKES, state[0] - action)
    bikes2 = min(MAX_BIKES, state[1] + action)
    move_penalty = MOVE_COST * abs(action)
    expected_total = 0.0

    for rent1 in range(MAX_BIKES + 1):
        p_rent1 = poisson_prob(rent1, RENTAL_REQUEST_RATE[0])
        actual_rent1 = min(bikes1, rent1)
        left1 = bikes1 - actual_rent1
        for rent2 in range(MAX_BIKES + 1):
            p_rent2 = poisson_prob(rent2, RENTAL_REQUEST_RATE[1])
            actual_rent2 = min(bikes2, rent2)
            left2 = bikes2 - actual_rent2
            rental_gain = RENTAL_REWARD * (actual_rent1 + actual_rent2) - move_penalty
            p_rents = p_rent1 * p_rent2

            for ret1 in range(MAX_BIKES + 1):
                p_ret1 = poisson_prob(ret1, RETURN_RATE[0])
                new1 = min(MAX_BIKES, left1 + ret1)
                for ret2 in range(MAX_BIKES + 1):
                    p_ret2 = poisson_prob(ret2, RETURN_RATE[1])
                    new2 = min(MAX_BIKES, left2 + ret2)
                    parking = (OVERFLOW_FEE if new1 > 10 else 0) + (OVERFLOW_FEE if new2 > 10 else 0)
                    immediate = rental_gain - parking
                    prob = p_rents * p_ret1 * p_ret2
                    expected_total += prob * (immediate + DISCOUNT * value_fn[new1, new2])
    return expected_total

def policy_iteration():
    value_fn = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1))
    policy = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1), dtype=int)

    stable = False
    while not stable:
        # Policy evaluation (simple iterative sweep until small change)
        while True:
            delta = 0.0
            for i in range(MAX_BIKES + 1):
                for j in range(MAX_BIKES + 1):
                    old = value_fn[i, j]
                    act = policy[i, j]
                    value_fn[i, j] = compute_expected_value((i, j), act, value_fn)
                    delta = max(delta, abs(old - value_fn[i, j]))
            if delta < 1e-4:
                break

        # Policy improvement
        stable = True
        for i in range(MAX_BIKES + 1):
            for j in range(MAX_BIKES + 1):
                actions = range(-min(MAX_MOVE, i), min(MAX_MOVE, j) + 1)
                old_action = policy[i, j]
                best_val = -float('inf')
                best_act = old_action
                for a in actions:
                    val = compute_expected_value((i, j), a, value_fn)
                    if val > best_val:
                        best_val = val
                        best_act = a
                policy[i, j] = best_act
                if best_act != old_action:
                    stable = False
    return policy, value_fn

if __name__ == "__main__":
    pol, val = policy_iteration()
    print("Policy (with SciPy restored):")
    print(pol)