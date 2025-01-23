# Makespan Experiment (Eviction version)

Create a new cluster:

```bash
inv cluster.provision --vm Standard_D8_v5 --nodes 33
inv cluster.credentials
```

## Native

First, deploy the native `k8s` cluster:

```bash
inv makespan.native.deploy --num-vms 32
```

Now, you can run the different baselines:

```bash
inv makespan.run.native-batch --workload mpi-evict --num-vms 32 --num-tasks 200
inv makespan.run.native-slurm --workload mpi-evict --num-vms 32 --num-tasks 200
```

Lastly, remove the native `k8s` cluster:

```bash
inv makespan.native.delete
```

## Granny (MPI)

First, deploy the k8s cluster:

```bash
faasmctl deploy.k8s --workers=32
```

Second, upload the corresponding WASM files:

```bash
inv makespan.wasm.upload
```

Third, run the experiment:

```bash
# TODO: will probably ditch --workload=mpi
# inv makespan.run.granny --workload mpi
# Set the --migrate flag to enable migrating Granules at runtime
# TODO: rename the workload to `mpi`
inv makespan.run.granny --num-vms 32 --num-tasks 100 --workload mpi-migrate [--migrate]
```

During an experiment, you may monitor the state of the cluster (in a separete
shell) by using:

```bash
faasmctl monitor.planner
```

## Plot the results

To plot the results, just run:

```bash
# TODO: this does not work atm
# TODO: move from tasks/motivation/plot.py
inv makespan.plot.migration
```
