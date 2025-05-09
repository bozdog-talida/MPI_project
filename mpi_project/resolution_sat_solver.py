import time
import tracemalloc

def load_cnf_file(path):
    """Load a CNF formula from a DIMACS .cnf file."""
    clauses = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '' or line.startswith(('c', 'p', '%')):
                continue
            literals = list(map(int, line.split()))
            if literals[-1] == 0:
                literals = literals[:-1] 
            clauses.append(literals)
    return clauses

def resolve(c1, c2):
    """Try resolving c1 and c2 on a single complementary literal."""
    for lit in c1:
        if -lit in c2:
            new_clause = set(c1).union(c2)
            new_clause.discard(lit)
            new_clause.discard(-lit)
            return tuple(sorted(new_clause))
    return None

def resolution_solver(formula, timeout=60):
    """Resolution-based SAT solver with timeout instead of clause limit."""
    start_time = time.time()
    clauses = set(tuple(sorted(clause)) for clause in formula)
    new_clauses = set()
    rounds = 0

    while True:
        rounds += 1
        if time.time() - start_time > timeout:
            print("Timeout exceeded — aborting resolution.")
            return None

        current_clauses = list(clauses)
        progress_made = False

        for i in range(len(current_clauses)):
            for j in range(i + 1, len(current_clauses)):
                if time.time() - start_time > timeout:
                    print("Timeout exceeded — aborting resolution.")
                    return None

        res = resolve(current_clauses[i], current_clauses[j])
        if res is not None:
            if len(res) == 0:
                print("Derived empty clause -> UNSAT")
                return False
            if res not in clauses and res not in new_clauses:
                new_clauses.add(res)
                progress_made = True


        if not new_clauses:
            print("No new clauses — satisfiability unknown (likely SAT).")
            return True

        clauses.update(new_clauses)
        new_clauses.clear()

        if rounds % 10 == 0:
            print(f"Round {rounds}: clause count = {len(clauses)}")

# MAIN

if __name__ == "__main__":
    file_path = "test_sat_short.cnf"
    print(f"Loading CNF file: {file_path}")
    formula = load_cnf_file(file_path)

    tracemalloc.start()
    start_time = time.time()

    try:
        result = resolution_solver(formula, timeout=60)  
    except Exception as e:
        result = None
        print("Error during solving:", e)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n===== Final Result =====")
    if result is False:
        print("Result: UNSAT")
    elif result is True:
        print("Result: SAT (no contradiction found)")
    else:
        print("Result: INCONCLUSIVE or TIMEOUT")

    print(f"Time taken: {end_time - start_time:.6f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
