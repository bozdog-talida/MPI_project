# SAT Solver Comparison – Resolution, DP, and DPLL

This project contains original Python implementations of three classical SAT solving algorithms:

- Resolution
- Davis–Putnam (DP)
- Davis–Putnam–Logemann–Loveland (DPLL)

Each solver is tested on standard CNF benchmarks to compare runtime and memory usage.

---

## 📁 Project Structure

- `resolution_sat_solver.py` – Implements the Resolution method.
- `dp_sat_solver.py` – Implements the Davis–Putnam algorithm.
- `dpll_sat_solver.py` – Implements the DPLL algorithm.
- `benchmarks/` – Contains sample `.cnf` files in DIMACS format.

---

## ▶️ How to Run

All scripts can be run from the terminal. Make sure Python 3 is installed.

```bash
python resolution_sat_solver.py
python dp_sat_solver.py
python dpll_sat_solver.py
