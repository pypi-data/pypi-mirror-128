"""
Operations over configurations of gcloud utility
"""
from dataclasses import dataclass
from json import loads
from re import compile as regexp_compile
from subprocess import check_output
from typing import Optional, List, Any, Dict

from singleton_decorator import singleton

from gubert.utils import VersionTuple

project_regexp = regexp_compile("/projects/(.+?)/")


@dataclass
class GcloudConfiguration(object):
    """
    Basic information about gcloud configuration
    """
    name: str
    is_active: bool
    account: str
    project: Optional[str]
    properties: Dict[str, Any]


@dataclass
class GcpKubernetesCluster(object):
    """
    GCP kubernetes cluster accessible from active service account
    """
    name: str
    location: str
    master_version: str
    master_ip: str
    machine_type: str
    node_version: str
    num_nodes: int
    status: str
    project: str


@singleton
class GcloudManager(object):
    """
    Operations over configurations of gcloud utility
    """

    def __init__(self, verbose: bool = False,
                 timeout: int = 10) -> None:
        super().__init__()
        self.timeout = timeout
        self.version = self._get_gcloud_version()
        if verbose:
            print(f"Gcloud version discovered: {self.version}")

    def _check_gcloud_version(self) -> None:
        if self.version < (200, 0, 0):
            raise RuntimeError(
                "Your gcloud version is older than required! "
                "Minimal supported version: 200.0.0")

    def configurations_list(self) -> List[GcloudConfiguration]:
        """
        Returns list of discovered gcloud configurations
        """
        out = check_output(["gcloud", "config", "configurations",
                            "list", "--format=json"],
                           timeout=self.timeout)
        parsed = loads(out)
        return [GcloudConfiguration(
            name=conf["name"],
            is_active=conf["is_active"],
            account=conf["properties"]["core"]["account"],
            project=conf["properties"]["core"]["project"],
            properties=conf["properties"],
        ) for conf in parsed]

    def discover_kubernetes_clusters(
            self
    ) -> Dict[str, GcpKubernetesCluster]:
        """
        Returns list of accessible gcloud configurations
        """
        out = check_output(["gcloud", "container", "clusters",
                            "list", "--format=json"],
                           timeout=self.timeout)
        parsed = loads(out)
        clusters: Dict[str, GcpKubernetesCluster] = {
            cluster.name: cluster for cluster in
            (self._parse_raw_cluster(cluster)
             for cluster in parsed)
        }
        return clusters

    def activate_kubernetes_cluster(
            self, cluster: GcpKubernetesCluster,
    ) -> str:
        """
        Activates gcloud kubernetes cluster
        """
        parsed = check_output(["gcloud", "container", "clusters",
                               "get-credentials", cluster.name,
                               "--region", cluster.location,
                               "--project", cluster.project,
                               "--format=json"],
                              timeout=self.timeout)
        return loads(parsed)

    @staticmethod
    def _parse_raw_cluster(
            cluster: Dict[str, Any],
    ) -> GcpKubernetesCluster:
        return GcpKubernetesCluster(
            name=cluster["name"],
            location=cluster["location"],
            master_version=cluster["currentMasterVersion"],
            master_ip=cluster["endpoint"],
            machine_type=cluster["nodeConfig"]["machineType"],
            node_version=cluster["currentNodeVersion"],
            num_nodes=cluster["currentNodeCount"],
            status=cluster["status"],
            project=project_regexp.findall(cluster["selfLink"])[0]
        )

    def activate_configuration(self, name: str) -> str:
        """
        Activates gcloud configuration
        """
        parsed = check_output(["gcloud", "config", "configurations",
                               "activate", name, "--format=json"],
                              timeout=self.timeout)
        return loads(parsed)

    def _get_gcloud_version(self) -> VersionTuple:
        out = check_output(["gcloud", "version", "--format=json"],
                           timeout=self.timeout)
        parsed = loads(out)
        return VersionTuple(parsed["Google Cloud SDK"])


if __name__ == "__main__":
    GcloudManager().discover_kubernetes_clusters()
