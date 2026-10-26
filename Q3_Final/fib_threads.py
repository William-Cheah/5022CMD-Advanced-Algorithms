"""
fib_threads.py
Q3: compute several Fibonacci numbers with and without multithreading,
time each round in nanoseconds and compare the averages.
"""

import platform
import sys
import threading
import time
from fibonacci import fib

DEFAULT_VALUES = [35, 38, 40]       # required by brief
DEFAULT_ROUNDS = 10                 # required by brief
MAX_VALUE = 40                      # larger values would take minute per round

def ask_values():
    """Ask which Fibonacci numbers to compute. Pressing Enter to keep the brief's values."""
    while True:
        text = input("Fibonacci values separated by commas (Press Enter = 35, 38, 40):").strip()
        if text == "":
            return DEFAULT_VALUES
        try:
            values = [int(num) for num in text.split(",")]    # text.split(",") = ["1","2","3"], int(num)=[1,2,3]
        except ValueError:
            print("Please enter whole numbers separated by commas, such as 23,27,30!")
            continue
        # set will remove duplicate, if size is shorten after set, mean include duplicate
        if len(set(values)) != len(values):
            print("Each value must be different!")
        elif min(values) < 0 or max(values)>MAX_VALUE:
            print(f"Each value must be from 0 to {MAX_VALUE}!")
        else:
            return values

def ask_rounds():
    """Ask how many rounds to run. Pressing Enter to keep the brief's 10 rounds"""
    while True:
        text = input("Number of rounds (Press Enter = 10 rounds): ").strip()
        if text == "":
            return DEFAULT_ROUNDS
        if text.isdigit() and 1 <= int(text) <= 20:
            return int(text)
        print("Please enter a whole number from 1 to 20!")

def worker(n, results):
    """Job of one thread: compute fib(n) and store it in the shared dictionary."""
    results[n] = fib(n)


def run_with_threads(values):
    """One thread per value. Return (results, T), where
    T = end of the thread that finished last - start of the thread that started first (ns)."""
    results = {}
    threads = []
    for n in values:
        threads.append(threading.Thread(target=worker, args=(n, results)))
    t1 = time.perf_counter_ns()
    for t in threads:
        t.start()       # start every thread (does not wait)
    for t in threads:
        t.join()        # wait for each thread to finish, one by one
    t2 = time.perf_counter_ns()
    return results, t2 - t1


def run_sequential(values):
    """Compute the same values one after another in the main thread. Return (results, T)."""
    results = {}
    t1 = time.perf_counter_ns()
    for n in values:
        worker(n, results)
    t2 = time.perf_counter_ns()
    return results, t2 - t1


def run_rounds(title, run_function, values, rounds):
    """Run run_function for the given number of rounds, print each round
    and return the list of times."""
    print(f"\n===== {title} =====")
    times = []
    for r in range(1, rounds + 1):
        results, total_ns = run_function(values)
        answers = " | ".join(f"Fib({n}) = {results[n]:,}" for n in values)
        print(f"Round {r:>2} | {answers} | T = {total_ns:>16,} ns")
        times.append(total_ns)
    average = sum(times) / len(times)
    print(f"Average T ({title.lower()}): {average:,.0f} ns")
    return times


def main():
    print("***** Fibonacci: Multithreading vs Sequential *****")
    values = ask_values()
    print("")
    rounds = ask_rounds()
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    print(f"\nPython {platform.python_version()} | GIL enabled: {gil} | "
          f"values {values} | {rounds} rounds")

    threaded = run_rounds("WITH multithreading", run_with_threads, values, rounds)
    sequential = run_rounds("WITHOUT multithreading", run_sequential, values, rounds)

    avg_threaded = sum(threaded) / len(threaded)
    avg_sequential = sum(sequential) / len(sequential)
    # (threaded - sequential) = gap; / sequential = gap relative to the baseline; * 100 = percentage
    difference = (avg_threaded - avg_sequential) / avg_sequential * 100
    word = "slower" if difference > 0 else "faster"
    print("\n===== Observation =====")
    print(f"Average with multithreading   : {avg_threaded:,.0f} ns")
    print(f"Average without multithreading: {avg_sequential:,.0f} ns")
    print(f"Multithreading was {abs(difference):.2f}% {word} than running sequentially.")


if __name__ == "__main__":
    main()

