# Migration Experiment (Fig.11b)

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
inv migration.run -w all-to-all -w very-network
```

Lastly, plot the results:

```bash
inv migration.plot
```

which will generate a plot in [`/plots/migration/migration_speedup_all-to-all.png`](/plots/migration/migration_speedup_all-to-all.png), we also include it below:

![migration plot](/plots/migration/migration_speedup_all-to-all.png)

and clean up:

```bash
faasmctl delete
```
