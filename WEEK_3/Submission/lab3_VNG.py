from lab3_gen import generate_k_sat_problem
import random

# ==================================
# Configuration holder for boolean variables
# ==================================
class BooleanConfiguration:
    def __init__(self, boolean_values):
        self.boolean_values = boolean_values  # Array of True/False values converted to 1/0


# ==================================
# Evaluation Method Alpha: Tally satisfied clauses
# ==================================
def evaluation_method_alpha(constraint_set, config):
    clause_satisfaction_count = 0
    for constraint in constraint_set:
        for term in constraint:
            position = abs(term) - 1
            current_value = config.boolean_values[position]

            # Positive term and variable is true
            if term > 0 and current_value == 1:
                clause_satisfaction_count += 1
                break
            # Negative term and variable is false
            if term < 0 and current_value == 0:
                clause_satisfaction_count += 1
                break
    return clause_satisfaction_count


# ==================================
# Evaluation Method Beta: Count active literals
# ==================================
def evaluation_method_beta(constraint_set, config):
    active_literal_count = 0
    values = config.boolean_values
    for constraint in constraint_set:
        for term in constraint:
            if values[abs(term) - 1] == 1:
                active_literal_count += 1
    return active_literal_count


# ==================================
# Target achievement test (Solution verification)
# ==================================
def target_achieved(constraint_set, config):
    if config is None:
        return False
    satisfied_constraints = 0
    for constraint in constraint_set:
        for term in constraint:
            position = abs(term) - 1
            value = config.boolean_values[position]
            if (term > 0 and value == 1) or (term < 0 and value == 0):
                satisfied_constraints += 1
                break
    return satisfied_constraints == len(constraint_set)


# ==================================
# Neighborhood Strategy Alpha: Single bit flip deterministic
# ==================================
def neighborhood_strategy_alpha(config, constraint_set):
    optimal_score = -1
    optimal_config = config
    no_improvement_count = 0

    for bit_index in range(len(config.boolean_values)):
        modified_values = config.boolean_values.copy()
        modified_values[bit_index] = 1 - modified_values[bit_index]
        candidate_config = BooleanConfiguration(modified_values)
        score = evaluation_method_beta(constraint_set, candidate_config)

        if score > optimal_score:
            optimal_score = score
            optimal_config = candidate_config
        else:
            no_improvement_count += 1

    if no_improvement_count == len(config.boolean_values):
        print("Local optimum detected (strategy alpha)")
        return None
    return optimal_config


# ==================================
# Neighborhood Strategy Beta: Multi-bit flip randomized (1-2 bits)
# ==================================
def neighborhood_strategy_beta(config, constraint_set, trials=10):
    best_score = -1
    best_config = config

    for _ in range(trials):
        modified_values = config.boolean_values.copy()
        flip_amount = random.choice([1, 2])
        positions_to_flip = random.sample(range(len(config.boolean_values)), flip_amount)

        for position in positions_to_flip:
            modified_values[position] = 1 - modified_values[position]

        candidate_config = BooleanConfiguration(modified_values)
        score = evaluation_method_beta(constraint_set, candidate_config)

        if score > best_score:
            best_score = score
            best_config = candidate_config

    return None if best_config.boolean_values == config.boolean_values else best_config


# ==================================
# Neighborhood Strategy Gamma: Extensive multi-bit flip (1-3 bits)
# ==================================
def neighborhood_strategy_gamma(config, constraint_set, trials=10):
    highest_score = -1
    best_config = config

    for _ in range(trials):
        modified_values = config.boolean_values.copy()
        flip_amount = random.choice([1, 2, 3])
        positions_to_flip = random.sample(range(len(config.boolean_values)), flip_amount)

        for position in positions_to_flip:
            modified_values[position] = 1 - modified_values[position]

        candidate_config = BooleanConfiguration(modified_values)
        score = evaluation_method_beta(constraint_set, candidate_config)

        if score > highest_score:
            highest_score = score
            best_config = candidate_config

    return None if best_config.boolean_values == config.boolean_values else best_config


# ==================================
# Local optimization core engine
# ==================================
def local_optimization_engine(constraint_set, initial_config, strategy_func, k, m, n, max_iterations=1000):
    previous_config = initial_config

    for iteration in range(max_iterations):
        if target_achieved(constraint_set, initial_config):
            print(f"\nTarget achieved at iteration {iteration}")
            print(f"Constraint set: {constraint_set}")
            print(f"Optimal configuration: {initial_config.boolean_values}")
            return initial_config

        if initial_config is None:
            print("Trapped in local minimum!")
            print(f"Previous configuration: {previous_config.boolean_values}")
            return previous_config

        previous_config = initial_config
        initial_config = strategy_func(initial_config, constraint_set)

    return initial_config


# ==================================
# Multi-strategy neighborhood search framework
# ==================================
def multi_strategy_search_framework(constraint_set, k, m, n):
    config = BooleanConfiguration([0] * n)
    print("\nExecuting optimization with strategy alpha")
    config = local_optimization_engine(constraint_set, config, neighborhood_strategy_alpha, k, m, n)

    if target_achieved(constraint_set, config):
        print("Target achieved using strategy alpha")
        return True

    print("\nTransitioning to strategy beta")
    config = local_optimization_engine(constraint_set, config, neighborhood_strategy_beta, k, m, n)
    if target_achieved(constraint_set, config):
        print("Target achieved using strategy beta")
        return True

    print("\nTransitioning to strategy gamma")
    config = local_optimization_engine(constraint_set, config, neighborhood_strategy_gamma, k, m, n)
    if target_achieved(constraint_set, config):
        print("Target achieved using strategy gamma")
        return True

    return False


# ==================================
# Performance evaluation (Success rate measurement)
# ==================================
def performance_evaluation(test_trials, k, m, n):
    successful_runs = 0
    for _ in range(test_trials):
        problem_instance = generate_k_sat_problem(k, m, n)
        if multi_strategy_search_framework(problem_instance, k, m, n):
            successful_runs += 1

    effectiveness_rate = (successful_runs / test_trials) * 100
    print(f"\nEffectiveness rate (%) = {effectiveness_rate:.2f}")
    return effectiveness_rate


# ==================================
# Experimental execution
# ==================================
if __name__ == "__main__":
    problem_constraints = generate_k_sat_problem(3, 75, 75)
    print(performance_evaluation(20, 3, 10, 10))