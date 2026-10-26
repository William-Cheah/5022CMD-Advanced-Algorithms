"""
Experiment: hash table vs 1D array search time for 100 - 50,000 records.
Every case is timed 5 times and the median is reported; the average number of
probes per hash table search is also recorded and compared with Knuth's formula.
"""
import platform
import random
import statistics
import time
from linear_search import linear_search
from hash_table import HashTable
from medicine import Medicine

SIZES = [100, 1000, 10000, 50000]
SEARCHES = 200      # searches per case
RUNS = 5            # repeats per case; the median is reported

def make_medicines(n: int):
    """Create n medicines with unique random IDs (same every run)"""
    random.seed(42)
    ids = random.sample(range(100000, 999999), n)
    return [Medicine(pid, f"Medicine{pid}", "General", "10.00", 100, False) for pid in ids]

def time_searches(search, keys):
    """Run search(key) for every key; return average nanoseconds per search"""
    start = time.perf_counter_ns()
    for key in keys:
        search(key)
    end = time.perf_counter_ns()
    return (end - start) / len(keys)

def median_time(search, keys):
    """Repeat time_searches RUNS times and return the median, which is less
    affected by background activity than a single run"""
    return statistics.median(time_searches(search, keys) for _ in range(RUNS))

def average_probes(table, keys):
    """Average number of slots inspected per hash table search"""
    return sum(table.count_probes(key) for key in keys) / len(keys)

def knuth_probes(alpha):
    """Expected probes for linear probing (Knuth, 1998): (successful, unsuccessful)"""
    return 0.5 * (1 + 1 / (1 - alpha)), 0.5 * (1 + 1 / (1 - alpha) ** 2)


def run_test(n: int):
    medicines = make_medicines(n)
    # put the SAME data into both structures
    array = []
    table = HashTable(n * 2 + 1)        # about twice as many slots as items
    for med in medicines:
        array.append(med)
        table.insert(med.product_id, med)

    # 200 IDs that exist, and 200 random IDs from the same range that do not exist
    rng = random.Random(7)
    stored = {med.product_id for med in medicines}
    existing = [rng.choice(medicines).product_id for _ in range(SEARCHES)]
    missing = []
    while len(missing) < SEARCHES:
        candidate = rng.randint(100000, 999998)
        if candidate not in stored:
            missing.append(candidate)

    alpha = table.load_factor()
    expect_found, expect_missing = knuth_probes(alpha)
    for case, keys, expected in (("Found", existing, expect_found),
                                 ("Not Found", missing, expect_missing)):
        hash_ns = median_time(table.get, keys)
        array_ns = median_time(lambda key: linear_search(array, key), keys)
        probes = average_probes(table, keys)
        print(f"{n:>7,} | {case:<9} | {probes:>6.2f} | {expected:>6.2f} | "
              f"{hash_ns:>10,.0f} | {array_ns:>12,.0f} | {array_ns / hash_ns:>8,.0f}x")


if __name__ == "__main__":
    print(f"Python {platform.python_version()} | {platform.system()} {platform.release()} | "
          f"{platform.processor()}")
    print(f"Median of {RUNS} runs, {SEARCHES} searches per case, load factor about 0.5\n")
    print(f"{'n':>7} | {'Search':<9} | {'Probes':>6} | {'Knuth':>6} | "
          f"{'Hash (ns)':>10} | {'Array (ns)':>12} | {'Faster by':>9}")
    print("-" * 78)
    for size in SIZES:
        run_test(size)
