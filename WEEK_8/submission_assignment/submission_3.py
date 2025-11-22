import numpy as np

# Constants (same semantics, new naming/style)
RENTAL_PAYOFF = 10
SHIFT_COST = 2
LOT_SURCHARGE = 4
CAPACITY = 20
MAX_SHIFT = 5
GAMMA = 0.9

# Value and policy arrays
VALUE = np.zeros((CAPACITY + 1, CAPACITY + 1))
POLICY = np.zeros((CAPACITY + 1, CAPACITY + 1), dtype=int)

def immediate_gain(b1: int, b2: int, move: int) -> float:
    """Return immediate reward from current bike counts and chosen transfer."""
    rental_income = RENTAL_PAYOFF * (min(b1, 3) + min(b2, 4))
    move_penalty = SHIFT_COST * abs(move)
    park_penalty = (LOT_SURCHARGE if b1 > 10 else 0) + (LOT_SURCHARGE if b2 > 10 else 0)
    return rental_income - move_penalty - park_penalty

def transition(b1: int, b2: int, move: int) -> tuple[int, int]:
    """Deterministic next state approximation (simplified demand/return heuristic)."""
    # Apply move then approximate net rentals/returns (+3, +2 heuristic kept)
    after_move_1 = min(CAPACITY, max(0, b1 - move))
    after_move_2 = min(CAPACITY, max(0, b2 + move))
    next_1 = min(CAPACITY, max(0, after_move_1 + 3))
    next_2 = min(CAPACITY, max(0, after_move_2 + 2))
    return next_1, next_2

def evaluate_policy(iter_tol: float = 1e-6):
    """Iterative policy evaluation until convergence for current POLICY."""
    while True:
        delta = 0.0
        for i in range(CAPACITY + 1):
            for j in range(CAPACITY + 1):
                act = int(POLICY[i, j])
                n1, n2 = transition(i, j, act)
                old = VALUE[i, j]
                VALUE[i, j] = immediate_gain(i, j, act) + GAMMA * VALUE[n1, n2]
                delta = max(delta, abs(old - VALUE[i, j]))
        if delta < iter_tol:
            break

def improve_policy() -> bool:
    """Policy improvement step. Returns True if policy stable."""
    stable = True
    for i in range(CAPACITY + 1):
        for j in range(CAPACITY + 1):
            best_a = POLICY[i, j]
            best_val = -float('inf')
            for a in range(-MAX_SHIFT, MAX_SHIFT + 1):
                # Feasibility check for move
                if not (0 <= i - a <= CAPACITY and 0 <= j + a <= CAPACITY):
                    continue
                n1, n2 = transition(i, j, a)
                val = immediate_gain(i, j, a) + GAMMA * VALUE[n1, n2]
                if val > best_val:
                    best_val = val
                    best_a = a
            if best_a != POLICY[i, j]:
                POLICY[i, j] = best_a
                stable = False
    return stable

def run_policy_iteration():
    while True:
        evaluate_policy()
        if improve_policy():
            break
    return POLICY, VALUE

if __name__ == "__main__":
    pol, val = run_policy_iteration()
    print("Refactored Deterministic Policy (Bike Transfer):")
    print(pol)
    print("Associated Value Estimates:")
    print(val)