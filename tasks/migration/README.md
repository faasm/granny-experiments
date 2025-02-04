# Migration Experiment

This experiment explores the benefits of migrating the execution of scientific
applications to benefit from dynamic changes in the compute environment.

First, provision the cluster:

```bash
inv cluster.provision --vm Standard_D8_v5 --nodes 3 cluster.credentials
```

Second, deploy the cluster

```bash
faasmctl deploy.k8s --workers 2
```

Second, upload the WASM files:

```bash
inv migration.wasm.upload
```

Third, run the experiments:

```bash
inv migration.run -w compute -w network
```

Lastly, plot the results:

```bash
inv migration.plot
```

and clean up:

```bash
faasmctl delete
```

## Migration Oracle

As a sanity-check, and in order to evaluate the potential benefits of migrating,
we can run an oracle to see what is the impact of distribution in the execution
time of a simulation.
