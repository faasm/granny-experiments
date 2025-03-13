# Granny Experiments

This repo contains the experiments for the [Granny paper](https://arxiv.org/abs/2302.11358).

When following any instructions in this repository, it is recommended to have a dedicated terminal with virtual environment of this repo activated: (`source ./bin/workon.sh`).

This virtual environment provides commands for provision/deprovision K8s clusters on Azure (with AKS), accessing low-level monitoring tools (we recommend `k9s`), and also commands for deploy Faabric clusters, run the experiments, and plot the results.

## Experiments in this repository

Microbenchmarks:
* [Polybench](./tasks/polybench/README.md) - experiment to measure the baseline overhead of using WebAssembly to execute the [PolyBench/C](https://web.cse.ohio-state.edu/~pouchet.2/software/polybench/) kernels.
* [Kernels (MPI)](./tasks/kernels_mpi/README.md) - microbenchmark of Faabric's MPI implementation using a subset of the [ParRes Kernels](https://github.com/ParRes/Kernels)
* [Kernels (OpenMP)](./tasks/kernels_omp/README.md) - microbenchmark of Faabric's OpenMP implementation using a subset of the [ParRes Kernels](https://github.com/ParRes/Kernels).
* [LULESH](./tasks/lulesh/README.md) - experiment using Granny to run a one-off  explicit shock dynamic simulation with LLNL's [LULESH](https://github.com/LLNL/LULESH).
* [LAMMPS](./tasks/lammps/README.md) - experiment using Faabric to run a one-off molecule simulation using [LAMMPS](https://www.lammps.org)
* [Migration](./tasks/migration/README.md) - microbenchmark showcasing the benefits of migrating an MPI application to improve locality.
* [Elastic] - TODO

Macrobenchmarks:
* [Makespan](./tasks/makespan/README.md) - experiment using Faabric to run a trace of scientific applications over a shared cluster of VMs. Comes in three flavours:
* [MPI Migration for Locality] - TODO
* [OpenMP Elastic Scaling to improve utilisation] - TODO
* [MPI + OpenMP Migration to reduce VM working set] - TODO
