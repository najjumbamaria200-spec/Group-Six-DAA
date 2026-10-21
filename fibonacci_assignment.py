"""
CSC2107: Design & Analysis of Algorithms
Assignment 5.1 - Naive vs. Memoized Fibonacci

Run:  python fibonacci_assignment.py
Outputs (written next to this file):
    results.csv, results.json, fig_calls_A_log.png,
    fig_calls_B.png, fig_calls_both.png, fig_time.png
"""

import csv
import json
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIMIT = sys.getrecursionlimit()      # normally 1000


# ----------------------------------------------------------------------
# PART 1 - Implementation
# ----------------------------------------------------------------------
calls_A = 0
calls_B = 0
fibtable = {}


def fib_A(n):
    """Algorithm A: plain recursion."""
    global calls_A
    calls_A += 1
    if n == 0 or n == 1:
        value = n
    else:
        value = fib_A(n - 1) + fib_A(n - 2)
    return value


def fib_B(n):
    """Algorithm B: recursion with memoization (dict used as fibtable)."""
    global calls_B
    calls_B += 1
    if n in fibtable:                 # "if fibtable[n] exists"
        return fibtable[n]
    if n == 0 or n == 1:
        value = n
    else:
        value = fib_B(n - 1) + fib_B(n - 2)
    fibtable[n] = value
    return value


def run_A(n):
    """Run Algorithm A once. Returns (value, calls, seconds)."""
    global calls_A
    calls_A = 0
    t0 = time.perf_counter()
    v = fib_A(n)
    t = time.perf_counter() - t0
    return v, calls_A, t


def run_B(n):
    """Run Algorithm B once with an empty table. Returns (value, calls, seconds)."""
    global calls_B
    calls_B = 0
    fibtable.clear()                  # clear fibtable before each run
    t0 = time.perf_counter()
    v = fib_B(n)
    t = time.perf_counter() - t0
    return v, calls_B, t


def fib_exact(n):
    """Reference value (iterative, exact big integers)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def verify_0_to_20():
    ok = True
    for n in range(21):
        a = run_A(n)[0]
        b = run_B(n)[0]
        if not (a == b == fib_exact(n)):
            ok = False
            print(f"MISMATCH at n={n}: A={a}, B={b}")
    return ok


# ----------------------------------------------------------------------
# PART 2 - Experiments
# ----------------------------------------------------------------------
def experiments():
    rows_A, rows_B = [], []

    # (a) Algorithm A: stop when a run takes longer than 60 s
    largest_A = None
    for n in (5, 10, 15, 20, 25, 30, 35):
        v, c, t = run_A(n)
        rows_A.append({"algorithm": "A", "n": n, "calls": c, "time_s": t})
        largest_A = n
        print(f"A  n={n:<4} calls={c:<12} time={t:.6f}s")
        if t > 60:
            print("   -> run exceeded 60 s, stopping.")
            break

    # (b) Algorithm B (n=1000 needs a higher recursion limit, see Part 4)
    sys.setrecursionlimit(10000)
    for n in (10, 50, 100, 200, 500, 1000):
        v, c, t = run_B(n)
        rows_B.append({"algorithm": "B", "n": n, "calls": c, "time_s": t})
        print(f"B  n={n:<4} calls={c:<12} time={t:.6f}s")
    sys.setrecursionlimit(DEFAULT_LIMIT)
    return rows_A, rows_B, largest_A


def save_table(rows_A, rows_B):
    path = os.path.join(HERE, "results.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algorithm", "n", "calls", "time (s)"])
        for r in rows_A + rows_B:
            w.writerow([r["algorithm"], r["n"], r["calls"], f"{r['time_s']:.6f}"])


def make_plots(rows_A, rows_B):
    nA = [r["n"] for r in rows_A]
    cA = [r["calls"] for r in rows_A]
    nB = [r["n"] for r in rows_B]
    cB = [r["calls"] for r in rows_B]

    # Algorithm A, log y-axis
    plt.figure(figsize=(6.2, 4.2))
    plt.plot(nA, cA, "o-", color="tab:red", label="Algorithm A (measured)")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("number of calls (log scale)")
    plt.title("Algorithm A: calls vs n")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "fig_calls_A_log.png"), dpi=150)
    plt.close()

    # Algorithm B, linear axes with 2n-1 reference
    plt.figure(figsize=(6.2, 4.2))
    plt.plot(nB, cB, "o-", color="tab:blue", label="Algorithm B (measured)")
    xs = list(range(1, 1001))
    plt.plot(xs, [2 * x - 1 for x in xs], "--", color="gray", label="2n - 1")
    plt.xlabel("n")
    plt.ylabel("number of calls")
    plt.title("Algorithm B: calls vs n")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "fig_calls_B.png"), dpi=150)
    plt.close()

    # Both on one chart, log y-axis
    plt.figure(figsize=(6.2, 4.2))
    plt.plot(nA, cA, "o-", color="tab:red", label="Algorithm A")
    plt.plot(nB, cB, "s-", color="tab:blue", label="Algorithm B")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("number of calls (log scale)")
    plt.title("Calls vs n, both algorithms")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "fig_calls_both.png"), dpi=150)
    plt.close()

    # Time chart
    plt.figure(figsize=(6.2, 4.2))
    plt.plot(nA, [r["time_s"] for r in rows_A], "o-", color="tab:red", label="Algorithm A")
    plt.plot(nB, [r["time_s"] for r in rows_B], "s-", color="tab:blue", label="Algorithm B")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("time in seconds (log scale)")
    plt.title("Execution time vs n")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "fig_time.png"), dpi=150)
    plt.close()


# ----------------------------------------------------------------------
# PART 3 - Analysis helpers
# ----------------------------------------------------------------------
def check_formulas(rows_A, rows_B):
    """calls_A(n) == 2*F(n+1)-1  and  calls_B(n) == 2n-1 (n >= 1)."""
    okA = all(r["calls"] == 2 * fib_exact(r["n"] + 1) - 1 for r in rows_A)
    okB = all(r["calls"] == 2 * r["n"] - 1 for r in rows_B)
    # also check every n from 1..30 for A and 1..900 for B
    for n in range(1, 25):
        okA &= run_A(n)[1] == 2 * fib_exact(n + 1) - 1
    sys.setrecursionlimit(10000)
    for n in range(1, 900):
        okB &= run_B(n)[1] == 2 * n - 1
    sys.setrecursionlimit(DEFAULT_LIMIT)
    return okA, okB


def extrapolate_A_1000(rows_A):
    """Estimate calls and time for Algorithm A at n = 1000."""
    calls = 2 * fib_exact(1001) - 1
    best = rows_A[-1]
    rate = best["calls"] / best["time_s"]          # calls per second
    seconds = calls / rate
    years = seconds / (365.25 * 24 * 3600)
    # scientific notation without float overflow
    s = str(calls)
    calls_sci = f"{s[0]}.{s[1:4]}e+{len(s) - 1}"
    ys = f"{int(years):d}"
    years_sci = f"{ys[0]}.{ys[1:4]}e+{len(ys) - 1}"
    return {"calls": calls, "calls_sci": calls_sci, "rate": rate,
            "years_sci": years_sci, "n_used": best["n"]}


# ----------------------------------------------------------------------
# PART 4 - Pushing to n = 1000
# ----------------------------------------------------------------------
def part4_failure():
    """4.1  Algorithm B with n=1000 under the default recursion limit."""
    sys.setrecursionlimit(DEFAULT_LIMIT)
    try:
        run_B(1000)
        return "no error"
    except RecursionError as e:
        return f"RecursionError: {e}"


def fix1_raise_limit(n=1000):
    """Fix 1: keep recursion, raise the limit."""
    sys.setrecursionlimit(max(DEFAULT_LIMIT, 2 * n + 100))
    try:
        return run_B(n)
    finally:
        sys.setrecursionlimit(DEFAULT_LIMIT)


def fib_B_bottom_up(n):
    """Fix 2: iterative bottom-up using the same table. No recursion at all.
    Returns (value, number_of_table_writes, seconds)."""
    t0 = time.perf_counter()
    table = {0: 0, 1: 1}
    for k in range(2, n + 1):
        table[k] = table[k - 1] + table[k - 2]
    return table[n], len(table), time.perf_counter() - t0


def fib_two_vars(n):
    """Fix 2 variant: O(1) extra space."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_B_warmup(n, step=100):
    """Fix 3 (extra): keep recursion but fill the table in chunks so no call
    chain is ever deeper than `step`."""
    for k in range(step, n + 1, step):
        fib_B(k)
    return fib_B(n)


# Part 4.3 - the "if fibtable[n]" truthiness trap
calls_trap = 0
fibtable_trap = {}


def fib_B_truthy(n):
    """Algorithm B with the check written as a TRUTHINESS test:
        if fibtable.get(n):      # <- 0 is falsy, so F(0)=0 looks 'missing'
    """
    global calls_trap
    calls_trap += 1
    if fibtable_trap.get(n):
        return fibtable_trap[n]
    if n == 0 or n == 1:
        value = n
    else:
        value = fib_B_truthy(n - 1) + fib_B_truthy(n - 2)
    fibtable_trap[n] = value
    return value


def part4_trap(n=30):
    global calls_trap
    fibtable_trap.clear()
    calls_trap = 0
    v = fib_B_truthy(n)
    return v, calls_trap


# ----------------------------------------------------------------------
def main():
    print(f"Python {sys.version.split()[0]}, default recursion limit = {DEFAULT_LIMIT}\n")

    print("== Part 1: correctness check, n = 0..20 ==")
    ok = verify_0_to_20()
    print("A and B agree with the reference for n=0..20:", ok, "\n")

    print("== Part 2: experiments ==")
    rows_A, rows_B, largest_A = experiments()
    save_table(rows_A, rows_B)
    make_plots(rows_A, rows_B)
    print(f"Largest n reached by Algorithm A: {largest_A}\n")

    print("== Part 3: formula checks ==")
    okA, okB = check_formulas(rows_A, rows_B)
    print("calls_A(n) == 2F(n+1)-1 :", okA)
    print("calls_B(n) == 2n-1      :", okB)
    ex = extrapolate_A_1000(rows_A)
    print(f"Estimated calls for A at n=1000: {ex['calls_sci']}")
    print(f"Measured rate (n={ex['n_used']}): {ex['rate']:.3e} calls/s")
    print(f"Estimated time: {ex['years_sci']} years\n")

    print("== Part 4 ==")
    failure = part4_failure()
    print("4.1 default limit, n=1000:", failure)
    v, c, t = fix1_raise_limit(1000)
    print(f"Fix 1 (setrecursionlimit): calls={c}, time={t:.6f}s, F(1000) correct: {v == fib_exact(1000)}")
    v2, writes, t2 = fib_B_bottom_up(1000)
    print(f"Fix 2 (bottom-up, table): table entries={writes}, time={t2:.6f}s, correct: {v2 == fib_exact(1000)}")
    v3 = fib_two_vars(1000)
    print(f"Fix 2b (two variables): correct: {v3 == fib_exact(1000)}")
    fibtable.clear()
    global calls_B
    calls_B = 0
    v4 = fib_B_warmup(1000)
    print(f"Fix 3 (warm-up, default limit): correct: {v4 == fib_exact(1000)}")
    tv, tc = part4_trap(30)
    _, bc, _ = run_B(30)
    print(f"4.3 truthiness check, n=30: value={tv}, calls={tc} (correct 'exists' version: {bc} calls)")
    print(f"    2n-1 = {2 * 30 - 1}")

    results = {
        "python": sys.version.split()[0],
        "default_limit": DEFAULT_LIMIT,
        "verified_0_20": ok,
        "largest_n_A": largest_A,
        "rows_A": rows_A,
        "rows_B": rows_B,
        "formula_A_ok": okA,
        "formula_B_ok": okB,
        "extrapolation": {"calls_sci": ex["calls_sci"], "rate": ex["rate"],
                          "years_sci": ex["years_sci"], "n_used": ex["n_used"]},
        "failure": failure,
        "fix1": {"calls": c, "time": t},
        "fix2": {"entries": writes, "time": t2},
        "trap": {"calls_truthy": tc, "calls_exists": bc},
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved results.csv, results.json and the figures.")


if __name__ == "__main__":
    main()
