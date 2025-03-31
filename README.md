# GRANNY Experiments

This repo contains the experiments for the [GRANNY paper](
https://www.usenix.org/conference/nsdi25/presentation/segarra).

All instructions in this repo assume that you have checked-out the repository,
and activated the python virtual environment (requires `python3-venv`):

```bash
source ./bin/workon.sh
inv -l # shows the differnt tasks
```

The Granny source-code is merged into the Faasm [repository](
https://github.com/faasm/faasm) tag [`0.27.0`](
https://github.com/faasm/faasm/releases/tag/v0.27.0)

## Experiments in this repository

The following table summarizes the different experiments available, with the
figures in the paper. The experiment results are also versioned in the repo,
so we add a quick command to re-generate the plot.

| Figure | Description (Instructions) | Quick Plot |
|---|---|---|
| Fig 6 | [Improving locality with compaction policy](./tasks/makespan/locality.md) | inv makespan.plot.locality |
| Fig 7 | [Improving utilization with elastic policy](./tasks/makespan/elastic.md) | inv makespan.plot.elastic |
| Fig 8 | [Ephemeral VMs with spot policy](./tasks/makespan/spot.md) | inv makespan.plot.spot |
| Fig 9 | MPI backend performance [MPI Kernels](./tasks/kernels_mpi/README.md.md) and [LAMMPS](./tasks/lammps/README.md) | inv makespan.plot.spot |
| Fig 10 | [OpenMP backend performance](./tasks/kernels_omp/README.md) | inv makespan.plot.spot |
| Fig 11 | [Speedup when migrating Granules](./tasks/migration/README.md) | inv migration.plot |
| Fig 12 | [Speedup when elastically scaling to more vCPUs](./tasks/elastic/README.md) | inv elastic.plot |
