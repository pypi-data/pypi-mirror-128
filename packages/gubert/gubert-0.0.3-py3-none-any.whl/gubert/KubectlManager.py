"""
Operations over configurations of kubectl utility
"""
from dataclasses import dataclass
from json import loads, dumps
from re import sub
from subprocess import check_output
from typing import Dict, Any, Optional

from singleton_decorator import singleton

from gubert.utils import VersionTuple


@dataclass
class KubernetesUser(object):
    """
    User record from kubeconfig
    """
    name: str
    provider: str


@dataclass
class KubernetesCluster(object):
    """
    Cluster record from kubeconfig
    """
    name: str
    server: str


@dataclass
class KubernetesContext(object):
    """
    Context record from kubeconfig
    """
    name: str
    cluster: KubernetesCluster
    user: KubernetesUser


@singleton
class KubernetesManager(object):
    """
    Operations over configurations of kubectl utility
    """

    def __init__(self, verbose: bool = False,
                 timeout: int = 10) -> None:
        super().__init__()
        self.timeout = timeout
        self.version = self.version()
        self.verbose = verbose
        if verbose:
            print(f"kubectl version discovered: {self.version}")

    def parse_configuration(self) -> Dict[str, KubernetesContext]:
        """
        Parses available contexts
        """
        out = check_output(["kubectl", "config",
                            "view", "-o", "json"],
                           timeout=self.timeout)
        parsed = loads(out)
        if self.verbose:
            print("Kubeconfig:\n" + dumps(parsed, indent=2))

        users: Dict[str, KubernetesUser] = {
            user.name: user for user in
            (self._parse_raw_user(user)
             for user in parsed["users"])
        }
        clusters: Dict[str, KubernetesCluster] = {
            cluster.name: cluster for cluster in
            (self._parse_raw_cluster(cluster)
             for cluster in parsed["clusters"])
        }
        contexts: Dict[str, KubernetesContext] = {
            context.name: context for context in
            (self._parse_raw_context(context, clusters, users)
             for context in parsed["contexts"])
        }
        return contexts

    @staticmethod
    def _parse_raw_user(user: Dict[str, Any]) -> KubernetesUser:
        name: str = user["name"]
        user_info: Dict[str, Any] = user.get("user", {})
        auth_provider: Dict[str, Any] = \
            user_info.get("auth-provider", {})
        auth_provider_name: str = auth_provider.get("name", "default")
        return KubernetesUser(name=name, provider=auth_provider_name)

    @staticmethod
    def _parse_raw_cluster(
            cluster: Dict[str, Any],
    ) -> KubernetesCluster:
        name: str = cluster["name"]
        cluster_info: Dict[str, Any] = cluster["cluster"]
        server: str = cluster_info["server"]
        return KubernetesCluster(name=name, server=server)

    @staticmethod
    def _parse_raw_context(
            context: Dict[str, Any],
            clusters: Dict[str, KubernetesCluster],
            users: Dict[str, KubernetesUser],
    ) -> KubernetesContext:
        name: str = context["name"]
        context_info: Dict[str, Any] = context["context"]
        cluster_name: str = context_info["cluster"]
        user_name: str = context_info["user"]
        cluster_ref: Optional[KubernetesCluster] = \
            clusters.get(cluster_name)
        if not cluster_ref:
            raise ValueError(f"Context '{name}' references "
                             f"to unknown cluster '{cluster_name}'")
        user_ref: Optional[KubernetesUser] = \
            users.get(user_name)
        if not user_ref:
            raise ValueError(f"Context '{name}' references "
                             f"to unknown user '{user_name}'")
        return KubernetesContext(name=name,
                                 cluster=cluster_ref,
                                 user=user_ref)

    def version(self) -> VersionTuple:
        """
        Returns version of discovered kubectl
        """
        out = check_output(["kubectl", "version",
                            "--short", "--client", "-o", "json"],
                           timeout=self.timeout)
        parsed = loads(out)
        git_version: str = parsed["clientVersion"]["gitVersion"]
        return VersionTuple(sub("[^.0-9]", "", git_version))


if __name__ == "__main__":
    KubernetesManager(True).parse_configuration()
