from base64 import b64encode
from faasmctl.util.planner import reset as reset_planner
from glob import glob
from invoke import task
from math import ceil
from matplotlib.pyplot import savefig, subplots
from os import makedirs
from os.path import basename, join
from tasks.lammps.env import get_faasm_benchmark
from tasks.migration.util import generate_host_list
from tasks.util.env import (
    LAMMPS_MIGRATION_FAASM_USER,
    LAMMPS_MIGRATION_FAASM_FUNC,
    PLOTS_ROOT,
    PROJ_ROOT,
    RESULTS_DIR,
)
from tasks.util.faasm import (
    get_faasm_exec_time_from_json,
    post_async_msg_and_get_result_json,
)
from time import sleep


def partition(number):
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    return answer


def calculate_cross_vm_links(part):
    """
    Calculate the number of cross-VM links for a given partition

    The number of cross-VM links is the sum for each process of all the
    non-local processes divided by two.
    """
    if len(part) == 1:
        return 0

    count = 0
    for ind in range(len(part)):
        count += sum(part[0:ind] + part[ind+1:]) * part[ind]

    return int(count / 2)


@task()
def run(ctx, nprocs=None):
    """
    Experiment to measure the benefits of migration in isolation
    """
    # Work out the number of processes to run with
    num_procs = [2, 4, 8, 10, 12, 14, 16]
    num_cpus_per_vm = 8
    num_vms = 16
    if nprocs is not None:
        num_procs = [nprocs]

    makedirs(RESULTS_DIR, exist_ok=True)
    result_dir = join(RESULTS_DIR, "migration")
    makedirs(result_dir, exist_ok=True)

    def do_write_csv_line(csv_name, part, xvm_links, actual_time):
        result_file = join(result_dir, csv_name)
        with open(result_file, "a") as out_file:
            out_file.write(
                "{},{},{:.2f}\n".format(part, xvm_links, actual_time)
            )

    for n_proc in num_procs:
        reset_planner(num_vms)

        # Initialise CSV file
        csv_name = "migration_oracle_{}.csv".format(n_proc)
        result_file = join(result_dir, csv_name)
        with open(result_file, "w") as out_file:
            out_file.write("Partition,CrossVMLinks,Time\n")

        partitions = partition(n_proc)
        num_loops = 1
        check_at = 1

        for ind, part in enumerate(partitions):
            if max(part) > num_cpus_per_vm:
                continue

            print("Running oracle prediction for size {} {}/{} with partition: {}".format(n_proc, ind + 1, len(partitions), part))

            host_list = generate_host_list(part)
            file_name = basename(
                get_faasm_benchmark("network")["data"][0]
            )
            user = LAMMPS_MIGRATION_FAASM_USER
            func = LAMMPS_MIGRATION_FAASM_FUNC
            cmdline = "-in faasm://lammps-data/{}".format(file_name)
            input_data = "{} {}".format(check_at, num_loops)

            msg = {
                "user": user,
                "function": func,
                "mpi": True,
                "mpi_world_size": n_proc,
                "cmdline": cmdline,
            }
            msg["input_data"] = b64encode(
                input_data.encode("utf-8")
            ).decode("utf-8")

            # Calculate number of cross-vm links
            cross_vm_links = calculate_cross_vm_links(part)

            # Invoke with or without pre-loading
            result_json = post_async_msg_and_get_result_json(
                msg, host_list=host_list
            )
            actual_time = get_faasm_exec_time_from_json(result_json)
            do_write_csv_line(
                csv_name, part, cross_vm_links, actual_time
            )

            sleep(2)


@task
def plot(ctx):
    plots_dir = join(PLOTS_ROOT, "migration")
    makedirs(plots_dir, exist_ok=True)
    out_file = join(plots_dir, "migration_oracle.pdf")

    results_dir = join(PROJ_ROOT, "results", "migration")
    result_dict = {}

    for csv in glob(join(results_dir, "migration_oracle_*.csv")):
        num_procs = csv.split("_")[-1].split(".")[0]

        result_dict[num_procs] = {
            "links": [],
            "time": []
        }

        with open(csv, "r") as fh:
            first = True
            for line in fh:
                if first:
                    first = False
                    continue

                result_dict[num_procs]["links"].append(int(line.split(",")[-2]))
                result_dict[num_procs]["time"].append(float(line.split(",")[-1]))

    num_plots = len(result_dict)
    num_cols = 4
    num_rows = ceil(num_plots / num_cols)
    fig, axes = subplots(nrows=num_rows, ncols=num_cols)
    fig.suptitle("Correlation between execution time (Y) and x-VM links (X)\n(wload: compute)")

    def do_plot(ax, results, num_procs):
        ax.scatter(results["links"], results["time"], s=0.1)
        ax.set_ylim(bottom=0)
        ax.set_title("{} MPI processes".format(num_procs))

    sorted_keys = sorted(list(result_dict.keys()))
    for i, num_procs in enumerate(sorted_keys):
        do_plot(axes[int(i / 4)][int(i % 4)], result_dict[num_procs], num_procs)

    fig.tight_layout()
    savefig(out_file, format="pdf")  # , bbox_inches="tight")
