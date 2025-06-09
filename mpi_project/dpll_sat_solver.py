import time
import tracemalloc

def load_cnf_file(path):
    clauses = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(('c', 'p', '%')):
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
                    pass
            if literals:
                clauses.append(literals)
    return clauses

def is_formula_empty(clauses):
    return len(clauses) == 0

def is_empty_clause_present(clauses):
    return any(len(c) == 0 for c in clauses)

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for unit in unit_clauses:
            literal = unit[0]
            if literal in assignment:
                continue
            if -literal in assignment:
                return None  
            assignment.add(literal)
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue  
                new_clause = [l for l in clause if l != -literal]
                if new_clause == clause:
                    continue  
                new_clauses.append(new_clause)
            clauses = new_clauses
            changed = True
            break
    return clauses, assignment

def choose_literal(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            if lit not in assignment and -lit not in assignment:
                return abs(lit)
    return None

def dpll(clauses, assignment=set(), depth=0, step=0, max_depth=3000):
    if depth > max_depth:
        print(f"[Step {step}] Depth {depth} Max depth exceeded")
        return None

    print(f"[Step {step}] Depth {depth} | Trying literal: {choose_literal(clauses, assignment) or '-'} | Assignment:", sorted(assignment))

    result = unit_propagate(clauses, assignment.copy())
    if result is None:
        return False
    clauses, assignment = result

    if is_formula_empty(clauses):
        return assignment
    if is_empty_clause_present(clauses):
        return False

    literal = choose_literal(clauses, assignment)
    if literal is None:
        return assignment

    for val in [literal, -literal]:
        new_assignment = assignment.copy()
        new_assignment.add(val)
        new_clauses = [list(c) for c in clauses]
        result = dpll(new_clauses + [[val]], new_assignment, depth + 1, step + 1, max_depth)
        if result:
            return result

    return False

# MAIN 
if __name__ == "__main__":
    formula = load_cnf_file("CBS_k3_n100_m403_b10_0.cnf")  

    tracemalloc.start()
    start_time = time.time()

    try:
        result = dpll(formula)
    except RecursionError:
        result = None
        print("Recursion depth exceeded!")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n===== Final Result =====")
    if result is False:
        print("Result: UNSAT")
    elif result is None:
        print("Result: INCOMPLETE or ABORTED")
    else:
        print("Result: SAT")
        print("Assignment:", sorted(result))

    print(f"Time taken: {end_time - start_time:.6f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
