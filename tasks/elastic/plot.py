from glob import glob
from invoke import task
from matplotlib.pyplot import subplots
import matplotlib.pylab as plt
from os import makedirs
from os.path import join
from pandas import read_csv
from tasks.util.elastic import ELASTIC_PLOTS_DIR, ELASTIC_RESULTS_DIR
from tasks.util.plot import (
    SINGLE_COL_FIGSIZE,
    get_color_for_baseline,
    save_plot,
)

plt.rcParams.update({
    "text.usetex": True,            # Use LaTeX for all text
    "font.family": "serif",         # Use serif fonts (like LaTeX default)
    "font.serif": ["Times"],        # Use Times font (matches ACM's acmart class default)
    "axes.labelsize": 12,           # Font size for axes labels
    "font.size": 12,                # General font size
    "legend.fontsize": 12,          # Font size for legend
    "xtick.labelsize": 10,          # Font size for x tick labels
    "ytick.labelsize": 10           # Font size for y tick labels
})


def _read_results():
    result_dict = {}

    for csv in glob(join(ELASTIC_RESULTS_DIR, "openmp_*.csv")):
        results = read_csv(csv)
        baseline = csv.split("_")[1]

        groupped_results = results.groupby("NumThreads", as_index=False)
        if baseline not in result_dict:
            result_dict[baseline] = {}

        for nt in groupped_results.mean()["NumThreads"].to_list():
            index = groupped_results.mean()["NumThreads"].to_list().index(nt)
            result_dict[baseline][nt] = {
                "mean": groupped_results.mean()["ExecTimeSecs"].to_list()[
                    index
                ],
                "sem": groupped_results.sem()["ExecTimeSecs"].to_list()[index],
            }

    return result_dict


@task(default=True)
def plot(ctx):
    """
    Plot the slowdown of OpenMP's ParRes kernels
    """
    results = _read_results()
    makedirs(ELASTIC_PLOTS_DIR, exist_ok=True)
    fig, ax = subplots(figsize=SINGLE_COL_FIGSIZE)

    assert len(results["elastic"]) == len(
        results["no-elastic"]
    ), "Results mismatch! (elastic: {} - no-elastic: {})".format(
        len(results["elastic"]), len(results["no-elastic"])
    )

    xs = list(results["elastic"].keys())
    ys = [
        float(results["no-elastic"][x]["mean"] / results["elastic"][x]["mean"])
        for x in xs
    ]

    ax.bar(
        xs,
        ys,
        color=get_color_for_baseline("omp-elastic", "granny"),
        edgecolor="black",
        zorder=3
    )

    # Labels
    ax.set_xticks(xs)

    # Horizontal line at slowdown of 1
    xlim_left = 0.5
    xlim_right = len(xs) + 0.5
    ax.hlines(1, xlim_left, xlim_right, linestyle="dashed", colors="red", zorder=4)

    ax.set_xlim(left=xlim_left, right=xlim_right)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Number of OpenMP threads")
    ax.set_ylabel("Speed-Up \n [No-Elastic / Elastic]")
    ax.grid(zorder=0)

    save_plot(fig, ELASTIC_PLOTS_DIR, "elastic_speedup")
