"""
Recursive Fibonacci function, plus a call counter used for the Big-O analysis.
"""
import time

def fib(n):
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1) by plain recursion."""
    if n <= 1:
        return n                # fib(0) = 0, fib(1) = 1
    return fib(n-1) + fib(n-2)  # add up the previous 2 number

def count_calls(n):
    """Return how many times fib() is called to compute fib(n)
    C(0) = C(1) = 1 and C(n) = C(n-1) + C(n-2) + 1, worked out with a loop."""

    if n <= 1:
        return 1

    # n    : 0 1 2 3 4 5
    # C(n) : 1 1 3 5 9 15   (number of calls, NOT the Fibonacci numbers)
    # before = C(n-2), current = C(n-1); each loop moves one step forward
    before, current = 1, 1
    for _ in range(2, n+1):
        before, current = current, before + current +1
    return current

if __name__ == '__main__':
    print(f"{'n':>3} | {'fib(n)':>10} | {'calls':>12} | {'time(ms)':>10} | {'x previous':>10} ")
    print("-" * 58)
    previous = None
    for n in range(20,31,2):
        start = time.perf_counter_ns()
        value = fib(n)
        ms = (time.perf_counter_ns() - start) / 1_000_000
        growth = f"{ms / previous:.2f}" if previous else "-"
        print(f"{n:>3} | {value:>10,} | {count_calls(n):>12,} | {ms:>10.2f} | {growth:>10} ")
        previous = ms
    for n in (35,38,40):
        print(f"fib({n}) needs {count_calls(n):,} calls")
