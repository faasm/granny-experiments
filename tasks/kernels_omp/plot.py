from glob import glob
from invoke import task
from matplotlib.pyplot import subplots
import matplotlib.pyplot as plt
from os import makedirs
from os.path import join
from pandas import read_csv
from tasks.util.env import SYSTEM_NAME
from tasks.util.kernels import (
    OPENMP_KERNELS,
    OPENMP_KERNELS_PLOTS_DIR,
    OPENMP_KERNELS_RESULTS_DIR,
)
from tasks.util.plot import UBENCH_PLOT_COLORS, SINGLE_COL_FIGSIZE, save_plot

FONT_SIZE = 14
LABEL_SIZE = 12
LINE_WIDTH = 2

plt.rcParams.update(
    {
        "text.usetex": True,  # Use LaTeX for all text
        "font.family": "serif",  # Use serif fonts (like LaTeX default)
        "font.serif": [
            "Times"
        ],  # Use Times font (matches ACM's acmart class default)
        "axes.labelsize": 12,  # Font size for axes labels
        "font.size": 12,  # General font size
        "legend.fontsize": 12,  # Font size for legend
        "xtick.labelsize": 10,  # Font size for x tick labels
        "ytick.labelsize": 10,  # Font size for y tick labels
    }
)


def _read_results():
    result_dict = {}

    for csv in glob(join(OPENMP_KERNELS_RESULTS_DIR, "openmp_*.csv")):
        results = read_csv(csv)

        workload = csv.split("_")[1]
        baseline = csv.split("_")[-1].split(".")[0]

        groupped_results = results.groupby("NumThreads", as_index=False)
        if baseline not in result_dict:
            result_dict[baseline] = {}
        if workload not in result_dict[baseline]:
            result_dict[baseline][workload] = {}

        for nt in groupped_results.mean()["NumThreads"].to_list():
            index = groupped_results.mean()["NumThreads"].to_list().index(nt)
            result_dict[baseline][workload][nt] = {
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
    result_dict = _read_results()
    makedirs(OPENMP_KERNELS_PLOTS_DIR, exist_ok=True)
    fig, ax = subplots(figsize=SINGLE_COL_FIGSIZE)

    num_kernels = len(OPENMP_KERNELS)
    width = float(1 / (num_kernels + 1))
    nprocs = list(range(1, 9))

    ymax = 2
    for ind_kernel, kernel in enumerate(OPENMP_KERNELS):
        ys = []
        xs = []
        x_kern_offset = -(num_kernels / 2) * width + ind_kernel * width
        if num_kernels % 2 == 0:
            x_kern_offset += width / 2

        for ind_np, np in enumerate(nprocs):
            xs.append(ind_np + x_kern_offset)
            y = (
                result_dict["granny"][kernel][np]["mean"]
                / result_dict["native"][kernel][np]["mean"]
            )
            if y > ymax:
                ax.text(
                    x=ind_np + x_kern_offset - 0.05,
                    y=ymax - 0.3,
                    s="{}x".format(round(y, 1)),
                    rotation=90,
                    fontsize=6,
                )

                ys.append(ymax)
            else:
                ys.append(y)

        ax.bar(
            xs,
            ys,
            width,
            label=kernel,
            color=UBENCH_PLOT_COLORS[ind_kernel],
            edgecolor="black",
            zorder=3,
        )

    # Labels
    xs = list(range(len(nprocs)))
    ax.set_xticks(xs, labels=nprocs)

    # Horizontal line at slowdown of 1
    xlim_left = -(0.5 + width)
    xlim_right = len(nprocs) - 0.5
    ax.hlines(
        1,
        xlim_left,
        xlim_right,
        linestyle="dashed",
        colors="red",
        zorder=4,
        linewidth=LINE_WIDTH,
    )

    ax.set_xlim(left=xlim_left, right=xlim_right)
    ax.set_ylim(bottom=0, top=ymax)
    ax.set_xlabel("Number of OpenMP threads", fontsize=FONT_SIZE)
    ax.set_ylabel(
        "Slowdown \n [{} / OpenMP]".format(SYSTEM_NAME), fontsize=FONT_SIZE
    )
    ax.legend(
        loc="upper right", ncol=5, bbox_to_anchor=(1.02, 1.20), fontsize=10
    )
    ax.grid(zorder=0)
    ax.tick_params(axis="both", labelsize=LABEL_SIZE)

    save_plot(fig, OPENMP_KERNELS_PLOTS_DIR, "openmp_kernels_slowdown")
