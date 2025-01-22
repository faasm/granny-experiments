# ParRes Kernels Experiment (OpenMP)

This experiment runs a set of the [ParRes Kernels](https://github.com/ParRes/Kernels)
as a microbenchmark for Granny's OpenMP implementation.

## Start AKS cluster

Create a new cluster:

```bash
inv cluster.provision --vm Standard_D8_v5 --nodes 2 cluster.credentials
```

## Faasm

Deploy the cluster:

```bash
faasmctl deploy.k8s --workers=1
```

Upload the WASM file:

```bash
inv kernels-omp.wasm.upload
```

and run the experiment with:

```bash
inv kernels-omp.run.wasm
```

finally, delete the cluster:

```bash
faasmctl delete
```

## OpenMPI

Deploy the native cluster:

```bash
inv kernels-omp.native.deploy
```

```bash
inv kernels-omp.run.native
```

finally, delete the native cluster

```bash
inv kernels-omp.native.delete
```

## Plot

To plot the results, just run:

```bash
inv kernels-omp.plot
```

the plot will be available in [`./plots/kernels-omp/openmp_kernels_slowdown.pdf`](
./plots/kernels-omp/openmp_kernels_slowdown.pdf), we also include it below:

![OpenMP Kernels Slowdown Plot](./plots/kernels-omp/openmp_kernels_slowdown.png)

## Clean-up

Finally, delete the AKS cluster:

```bash
inv cluster.delete
```
