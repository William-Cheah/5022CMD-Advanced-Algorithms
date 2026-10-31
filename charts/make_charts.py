"""
make_charts.py
Draws the two line charts used in the report from the measured results:
  Figure 1.13(b) - hash table vs 1D array search time (data: Table 1.6, output of Q1_Final/performance_test.py)
  Figure 3.8     - time per round with and without multithreading (data: output of Q3_Final/fib_threads.py,
                   standard build and free-threaded build)
Requires matplotlib (pip install matplotlib). Run: python make_charts.py
"""
import matplotlib.pyplot as plt

BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#2b2b2a", "#6b6a66", "#e6e5e1"


def tidy(ax):
    """Light grid, no top/right border."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=MUTED)
    ax.grid(True, which="major", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def q1_chart():
    """Median time per search against n, on log-log axes."""
    n = [100, 1000, 10000, 50000]
    data = {"Found": ([151, 174, 189, 157], [1094, 9656, 105227, 620982]),
            "Not found": ([208, 252, 231, 494], [2203, 20819, 207292, 1320930])}
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.9), dpi=220, sharey=True)
    for ax, (case, (hash_ns, array_ns)) in zip(axes, data.items()):
        ax.plot(n, array_ns, color=ORANGE, lw=2, marker="o", label="1D array (linear search)")
        ax.plot(n, hash_ns, color=BLUE, lw=2, marker="o", label="Hash table (linear probing)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        tidy(ax)
        ax.set_title(f"{case} search", loc="left", color=INK)
        ax.set_xlabel("Number of records, n (log scale)", color=MUTED)
    axes[0].set_ylabel("Median time per search (ns, log scale)", color=MUTED)
    axes[0].legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig("q1_chart.png", facecolor="white")


def q3_chart():
    """Time per round for both builds, with and without threads."""
    rounds = range(1, 11)
    runs = {
        "Standard build (GIL enabled)": (
            [15.5964545, 15.5291135, 15.5755963, 15.6435574, 15.623209, 15.6114171, 15.9100565, 15.6346498, 15.6410372, 15.6078529],
            [15.5704836, 15.5666081, 15.6191381, 15.7128976, 15.6465973, 15.5758458, 15.5662609, 15.5378724, 15.6006038, 15.5792816]),
        "Free-threaded build (GIL disabled)": (
            [11.4219325, 12.9137344, 14.1077876, 14.6273643, 19.523651, 18.7279765, 19.1517807, 18.9784549, 12.1431787, 14.9698412],
            [22.2647012, 16.3713709, 16.3148946, 17.2197085, 18.4337573, 16.348285, 16.3295971, 16.3847858, 16.3402182, 16.3697681]),
    }
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.9), dpi=220, sharey=True)
    for ax, (title, (threaded, sequential)) in zip(axes, runs.items()):
        ax.plot(rounds, sequential, color=ORANGE, lw=2, marker="o", label="Without multithreading")
        ax.plot(rounds, threaded, color=BLUE, lw=2, marker="o", label="With multithreading")
        tidy(ax)
        ax.set_xticks(list(rounds))
        ax.set_xlabel("Round", color=MUTED)
        ax.set_title(title, loc="left", color=INK)
    limit = 0.679 * 16.35          # fib(40) is 67.9% of all calls; 16.35 s = typical sequential round
    axes[1].axhline(limit, color=MUTED, lw=1, ls="--")
    axes[1].text(1, limit - 0.9, f"theoretical best = {limit:.1f} s", color=MUTED, fontsize=8.5)
    axes[0].set_ylabel("Time per round, T (seconds)", color=MUTED)
    axes[0].legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig("q3_chart.png", facecolor="white")


if __name__ == "__main__":
    q1_chart()
    q3_chart()
    print("Saved q1_chart.png and q3_chart.png")
