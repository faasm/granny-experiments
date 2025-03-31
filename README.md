# GRANNY Experiments

This repo contains the experiments for the [Granny paper](https://arxiv.org/abs/2302.11358).

When following any instructions in this repository, it is recommended to have a dedicated terminal with virtual environment of this repo activated: (`source ./bin/workon.sh`).

This virtual environment provides commands for provision/deprovision K8s clusters on Azure (with AKS), accessing low-level monitoring tools (we recommend `k9s`), and also commands for deploy Faabric clusters, run the experiments, and plot the results.

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
