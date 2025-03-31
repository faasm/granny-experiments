# Migration Experiment

This experiment explores the benefits of migrating the execution of scientific
applications to benefit from dynamic changes in the compute environment.

First, provision the cluster:

```bash
inv cluster.provision --vm Standard_D8_v5 --nodes 3 --name ${CLUSTER_NAME}
inv cluster.credentials --name ${CLUSTER_NAME}
```

Second, deploy the cluster

```bash
(faasm-exp-faabric) faasmctl deploy.k8s --workers 2
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
