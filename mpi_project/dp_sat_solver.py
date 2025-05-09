import os
import time
import tracemalloc

def load_cnf_file(path):
    clauses = []
    print(f"Opening file: {path}")
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('p') or line.startswith('%'):
                print(" Skipped")
                continue
            parts = line.split()
            literals = []
            for part in parts:
                try:
                    lit = int(part)
                    if lit == 0:
                        break
                    literals.append(lit)
                except ValueError:
                    print(f" Invalid literal: {part}")
            print(f" Parsed clause: {literals}")
            if literals:
                clauses.append(literals)
    print("Final loaded clauses:", clauses)
    return clauses

def is_empty_clause_present(clauses):
    return any(len(c) == 0 for c in clauses)

def is_formula_empty(clauses):
    return len(clauses) == 0

def get_variables(clauses):
    return set(abs(lit) for clause in clauses for lit in clause)

def resolve_on_variable(clauses, var, existing_clauses):
    pos = [c for c in clauses if var in c]
    neg = [c for c in clauses if -var in c]
    resolvents = []

    for c1 in pos:
        for c2 in neg:
            new_clause = list(set(c1 + c2))
            new_clause = [lit for lit in new_clause if lit != var and lit != -var]
            frozen = frozenset(new_clause)
            if frozen not in existing_clauses:
                resolvents.append(new_clause)
                existing_clauses.add(frozen)

    return resolvents

def remove_var_clauses(clauses, var):
    return [c for c in clauses if var not in c and -var not in c]

def dp_solver(clauses, start_time, timeout=30):
    existing_clauses = set(frozenset(c) for c in clauses)

    def recursive_solver(current_clauses):
        if time.time() - start_time > timeout:
            print("Timeout exceeded (30 seconds)")
            return None

        if is_formula_empty(current_clauses):
            print("Formula is empty -> SAT")
            return True
        if is_empty_clause_present(current_clauses):
            print("Empty clause found -> UNSAT")
            return False

        variables = get_variables(current_clauses)
        var = next(iter(variables))  

        print(f"Resolving on variable: {var}")

        resolvents = resolve_on_variable(current_clauses, var, existing_clauses)
        reduced_clauses = remove_var_clauses(current_clauses, var) + resolvents
        print(f"-> Total clauses after resolution: {len(reduced_clauses)}")

        return recursive_solver(reduced_clauses)

    return recursive_solver(clauses)

# MAIN 
if __name__ == "__main__":
    print("File exists:", os.path.exists("CBS_k3_n100_m403_b10_0.cnf"))
    formula = load_cnf_file("CBS_k3_n100_m403_b10_0.cnf")

    tracemalloc.start()
    start_time = time.time()

    try:
        result = dp_solver(formula, start_time)
    except RecursionError:
        result = None
        print("Recursion depth exceeded!")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n===== Final Result =====")
    if result is True:
        print("Result: SAT")
    elif result is False:
        print("Result: UNSAT")
    else:
        print("Result: INCOMPLETE or ABORTED")

    print(f"Time taken: {end_time - start_time:.6f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
