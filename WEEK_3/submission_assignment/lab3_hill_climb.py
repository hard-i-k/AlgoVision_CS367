from lab3_gen import generate_k_sat_problem
import random

# Container class for variable truth value assignments
class VariableAssignment:
    def _init_(self, values):
        self.values = values

# Scoring function A: tallies satisfied clauses in formula
def scoring_function_a(formula, assignment_obj):
    satisfied_clauses = 0
    for clause in formula:
        for literal in clause:
            if (literal > 0 and assignment_obj.values[literal - 1] == 1) or (literal < 0 and assignment_obj.values[abs(literal) - 1] == 0):
                satisfied_clauses += 1
                break
    return satisfied_clauses

# Scoring function B: counts matching literals per clause
def scoring_function_b(formula, assignment_obj):
    total_matches = 0
    truth_values = assignment_obj.values
    for clause in formula:
        for literal in clause:
            if (literal > 0 and truth_values[literal - 1] == 1) or (literal < 0 and truth_values[abs(literal) - 1] == 0):
                total_matches += 1
                break
    return total_matches

# Verify if assignment satisfies complete formula
def verify_complete_satisfaction(formula, assignment_obj):
    clauses_satisfied = 0
    for clause in formula:
        for literal in clause:
            if (literal > 0 and assignment_obj.values[literal - 1] == 1) or (literal < 0 and assignment_obj.values[abs(literal) - 1] == 0):
                clauses_satisfied += 1
                break
    return clauses_satisfied == len(formula)

# Create improved successor assignment
def create_improved_successor(current_assignment, formula):
    highest_score = -1
    optimal_assignment = current_assignment
    for variable_idx in range(len(current_assignment.values)):
        modified_values = current_assignment.values[:]
        modified_values[variable_idx] = 1 - modified_values[variable_idx]  # toggle bit
        candidate_assignment = VariableAssignment(modified_values)
        candidate_score = scoring_function_b(formula, candidate_assignment)
        if candidate_score > highest_score:
            highest_score = candidate_score
            optimal_assignment = candidate_assignment

    # Return None if no improvement found
    return None if optimal_assignment.values == current_assignment.values else optimal_assignment

# Hill climbing optimization for k-SAT problem solving
def hill_climbing_optimization(formula, k, m, n, max_iterations=1000):
    current_assignment = VariableAssignment([0] * n)
    for iteration in range(max_iterations):
        if verify_complete_satisfaction(formula, current_assignment):
            print(f"\nSolution discovered after {iteration} iterations!")
            print(f"Problem clauses: {formula}")
            print(f"Solution assignment: {current_assignment.values}")
            return True

        improved_assignment = create_improved_successor(current_assignment, formula)
        if improved_assignment is None:
            print("Trapped in local optimum.")
            return False
        current_assignment = improved_assignment

    return False

# Measure solution discovery rate (penetrance metric)
def measure_solution_rate(test_runs, k, m, n):
    successful_solves = 0
    for _ in range(test_runs):
        problem_formula = generate_k_sat_problem(k, m, n)
        if hill_climbing_optimization(problem_formula, k, m, n):
            successful_solves += 1
    return (successful_solves / test_runs) * 100

# Demonstration execution
if __name__ == "__main__":
    test_formula = generate_k_sat_problem(3, 50, 50)
    print("Sample problem formula:")
    print(test_formula)
    print("\n--- Executing Hill Climbing Algorithm ---")
    print(f"Solution Rate: {measure_solution_rate(20, 3, 50, 50):.2f}%")