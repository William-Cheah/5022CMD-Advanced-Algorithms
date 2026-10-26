# Q3 – Concurrent Process: Fibonacci with Multithreading

Computes Fib(35), Fib(38) and Fib(40) with one thread per value and, for
comparison, one after another in the main thread. Each version runs for ten
rounds; the program prints the time of every round in nanoseconds, both
averages and the percentage difference.

## Files

| File | Purpose |
|---|---|
| `fibonacci.py` | Recursive `fib(n)` and `count_calls(n)` (number of calls, used for the Big-O analysis) |
| `fib_threads.py` | Threaded and sequential versions, timing, averages and observation |

## How to run

```
python fibonacci.py      # growth of fib(n) for n = 20 to 30
python fib_threads.py    # press Enter twice for the brief's values (35, 38, 40; 10 rounds)
```

A full run takes about 7 minutes. The program prints whether the GIL is enabled.
To repeat the experiment without the GIL, use the free-threaded build (Python 3.13t or later), for example with uv:

```
uv python install 3.14t
uv run --no-project --python 3.14t fib_threads.py
```
