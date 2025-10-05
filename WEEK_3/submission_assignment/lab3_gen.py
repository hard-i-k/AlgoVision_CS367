import random

def generate_k_sat_problem(k, num_clauses, num_variables):
    """
    Generate a random k-SAT problem instance.
    
    Args:
        k: Number of literals per clause
        num_clauses: Total number of clauses (m)
        num_variables: Total number of variables (n)
    
    Returns:
        List of clauses where each clause is a list of literals
    """
    clauses = []
    
    for _ in range(num_clauses):
        clause = []
        selected_vars = random.sample(range(1, num_variables + 1), k)
        
        for var in selected_vars:
            # Randomly decide if literal should be positive or negative
            if random.random() < 0.5:
                literal = -var  # Negative literal
            else:
                literal = var   # Positive literal
            clause.append(literal)
        
        clauses.append(clause)
    
    return clauses

def print_formula(clauses):
    """Pretty print the SAT formula"""
    formula_str = ""
    for i, clause in enumerate(clauses):
        if i > 0:
            formula_str += " ∧ "
        
        clause_str = "("
        for j, literal in enumerate(clause):
            if j > 0:
                clause_str += " ∨ "
            
            if literal < 0:
                clause_str += f"¬x{abs(literal)}"
            else:
                clause_str += f"x{literal}"
        
        clause_str += ")"
        formula_str += clause_str
    
    return formula_str

# Test the generator
if __name__ == "__main__":
    # Generate a small example
    test_clauses = generate_k_sat_problem(3, 5, 4)
    print("Generated 3-SAT problem:")
    print("Clauses:", test_clauses)
    print("Formula:", print_formula(test_clauses))