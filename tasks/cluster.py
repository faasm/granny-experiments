from invoke import task
from os.path import join
from subprocess import run
from tasks.util.env import (
    ACR_NAME,
    AKS_CLUSTER_NAME,
    AKS_NODE_COUNT,
    AKS_REGION,
    AKS_VM_SIZE,
    AZURE_PUB_SSH_KEY,
    AZURE_RESOURCE_GROUP,
    CONFIG_DIR,
    KUBECTL_BIN,
)
from tasks.util.version import get_k8s_version


# AKS commandline reference here:
# https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest
def _run_aks_cmd(name, az_args=None):
    cmd = [
        "az",
        "aks {}".format(name),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
    ]

    if az_args:
        cmd.extend(az_args)

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def list(ctx):
    """
    List all AKS resources
    """
    _run_aks_cmd("list")


@task(optional=["sgx"])
def provision(
    ctx,
    nodes=AKS_NODE_COUNT,
    vm=AKS_VM_SIZE,
    location=AKS_REGION,
    name=AKS_CLUSTER_NAME,
    sgx=False,
    granny=True,
):
    """
    Provision the AKS cluster
    """
    k8s_ver = get_k8s_version()
    sgx = sgx and (sgx.lower() != "false")
    granny_kubelet_config = join(CONFIG_DIR, "granny_aks_kubelet_config.json")
    granny_os_config = join(CONFIG_DIR, "granny_aks_os_config.json")

    if sgx and "Standard_DC" not in vm:
        print(
            "Error provisioning SGX cluster: only `Standard_DC` VMs are supported"
        )
        return

    _run_aks_cmd(
        "create",
        [
            "--name {}".format(name),
            "--node-count {}".format(nodes),
            "--node-vm-size {}".format(vm),
            "--os-sku Ubuntu",
            "--kubernetes-version {}".format(k8s_ver),
            "--ssh-key-value {}".format(AZURE_PUB_SSH_KEY),
            "--location {}".format(location),
            # Could not create a role assignment for ACR. Are you an Owner on this subscription?
            # "--attach-acr {}".format(ACR_NAME.split(".")[0]),
            "{}".format(
                "--kubelet-config {}".format(granny_kubelet_config)
                if granny
                else ""
            ),
            "{}".format(
                "--linux-os-config {}".format(granny_os_config)
                if granny
                else ""
            ),
            "{}".format(
                "--enable-addons confcom --enable-sgxquotehelper"
                if sgx
                else ""
            ),
        ],
    )


@task
def details(ctx):
    """
    Show the details of the cluster
    """
    _run_aks_cmd(
        "show",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
        ],
    )


@task
def delete(ctx, name=AKS_CLUSTER_NAME):
    """
    Delete the AKS cluster
    """
    _run_aks_cmd(
        "delete",
        [
            "--name {}".format(name),
            "--yes",
        ],
    )


@task
def credentials(ctx, name=AKS_CLUSTER_NAME, out_file=None):
    """
    Get credentials for the AKS cluster
    """
    # Set up the credentials
    _run_aks_cmd(
        "get-credentials",
        [
            "--name {}".format(name),
            "--overwrite-existing",
            "--file {}".format(out_file) if out_file else "",
        ],
    )

    # Check we can access the cluster
    cmd = "{} get nodes".format(KUBECTL_BIN)
    print(cmd)
    run(cmd, shell=True, check=True)
