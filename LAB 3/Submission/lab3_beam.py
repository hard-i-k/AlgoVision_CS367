from lab3_gen import generate_k_sat_problem
import random

# Data structure for storing variable assignments in search
class SearchState:
    def __init__(self, assignment):
        self.assignment = assignment

# Evaluation function: Calculate number of satisfied clauses
def evaluate_satisfied_clauses(formula, search_state):
    satisfied_count = 0
    assignment = search_state.assignment
    for clause in formula:
        clause_satisfied = False
        for lit in clause:
            var_index = abs(lit) - 1
            if (lit > 0 and assignment[var_index] == 1) or (lit < 0 and assignment[var_index] == 0):
                clause_satisfied = True
                break
        if clause_satisfied:
            satisfied_count += 1
    return satisfied_count

# Alternative scoring: Count matching literals in each clause
def count_matching_literals(formula, search_state):
    match_score = 0
    var_assignment = search_state.assignment
    for clause in formula:
        for lit in clause:
            variable_idx = abs(lit) - 1
            if (lit > 0 and var_assignment[variable_idx] == 1) or (lit < 0 and var_assignment[variable_idx] == 0):
                match_score += 1
                break
    return match_score

# Verify if current assignment solves the SAT problem
def check_complete_solution(formula, search_state):
    assignment = search_state.assignment
    for clause in formula:
        clause_is_true = any(
            (literal > 0 and assignment[abs(literal) - 1] == 1) or
            (literal < 0 and assignment[abs(literal) - 1] == 0)
            for literal in clause
        )
        if not clause_is_true:
            return False
    return True

# Find optimal neighboring state by flipping single bits
def find_optimal_neighbor(current_state, formula):
    optimal_state = current_state
    max_score = evaluate_satisfied_clauses(formula, current_state)

    for bit_position in range(len(current_state.assignment)):
        modified_assignment = current_state.assignment[:]
        modified_assignment[bit_position] = 1 - modified_assignment[bit_position]  # toggle bit
        neighbor_state = SearchState(modified_assignment)
        neighbor_score = evaluate_satisfied_clauses(formula, neighbor_state)

        if neighbor_score > max_score:
            optimal_state = neighbor_state
            max_score = neighbor_score

    return None if optimal_state.assignment == current_state.assignment else optimal_state

# Generate best beam_width successor states for beam search
def generate_top_successors(current_state, formula, beam_width=3):
    successor_list = []
    for bit_idx in range(len(current_state.assignment)):
        new_assignment = current_state.assignment[:]
        new_assignment[bit_idx] = 1 - new_assignment[bit_idx]
        successor_list.append(SearchState(new_assignment))
    successor_list.sort(key=lambda state: count_matching_literals(formula, state), reverse=True)
    return successor_list[:beam_width]

# Local search using hill climbing strategy
def local_search_hill_climbing(formula, k, m, n, max_iterations=1000):
    current_state = SearchState([0] * n)
    for iteration in range(max_iterations):
        if check_complete_solution(formula, current_state):
            print(f"\nSolution discovered at iteration {iteration}")
            print(f"Variable assignment: {current_state.assignment}")
            return current_state
        improved_state = find_optimal_neighbor(current_state, formula)
        if improved_state is None:
            print("Local optimum reached.")
            return None
        current_state = improved_state
    return None

# Beam search algorithm for SAT solving
def beam_search_algorithm(formula, k, m, n, max_iterations=1000, beam_width=3):
    initial_state = SearchState([random.choice([0, 1]) for _ in range(n)])
    if check_complete_solution(formula, initial_state):
        print("Immediate solution discovered:", initial_state.assignment)
        return True

    active_beam = generate_top_successors(initial_state, formula, beam_width)

    for iteration in range(max_iterations):
        next_beam = []
        if not active_beam:
            print("Search beam depleted. Local optimum reached.")
            return False

        for state in active_beam:
            if check_complete_solution(formula, state):
                print(f"\nSolution discovered at iteration {iteration + 1}")
                print(f"Variable assignment: {state.assignment}")
                return True

            improved_state = find_optimal_neighbor(state, formula)
            if improved_state:
                next_beam.append(improved_state)

        active_beam = sorted(next_beam, key=lambda s: count_matching_literals(formula, s), reverse=True)[:beam_width]
    return False

# Compute algorithm success percentage
def compute_success_rate(test_instances, k, m, n):
    successful_runs = 0
    for _ in range(test_instances):
        problem_instance = generate_k_sat_problem(k, m, n)
        if beam_search_algorithm(problem_instance, k, m, n):
            successful_runs += 1
    return (successful_runs / test_instances) * 100

# Demo execution
if __name__ == "__main__":
    demo_problem = generate_k_sat_problem(3, 25, 25)
    print("Example Problem Instance:")
    print(demo_problem)
    print("\n--- Executing Beam Search Algorithm ---")
    success_percentage = compute_success_rate(20, 3, 25, 25)
    print(f"\nSuccess Rate: {success_percentage:.2f}%")
