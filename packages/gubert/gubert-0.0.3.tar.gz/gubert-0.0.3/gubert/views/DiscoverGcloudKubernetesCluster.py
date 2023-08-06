"""
Discovering & activating gcloud kubernetes cluster
"""
from typing import List

from gubert.GcloudManager import GcloudManager, GcpKubernetesCluster
from gubert.views.View import View


class DiscoverGcloudKubernetesCluster(View):
    """
    Discovering & activating gcloud kubernetes cluster
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def name() -> str:
        """
        View name for discovering & activating gcloud kubernetes cluster
        """
        return "Discover kubernetes clusters from gcloud"

    def handle(self) -> None:
        """
        Handles kubernetes cluster discovery via gcloud.
        """
        gcloud: GcloudManager = GcloudManager()
        options: List[GcpKubernetesCluster] = \
            sorted(list(gcloud.discover_kubernetes_clusters().values()),
                   key=lambda x: x.name)
        # TODO is it possible to match current kubernetes cluster?
        table_data = [[
            str(i.name or ""),
            str(i.location or ""),
            str(i.master_version or ""),
            str(i.master_ip or ""),
            str(i.machine_type or ""),
            str(i.node_version or ""),
            str(i.num_nodes or ""),
            str(i.status or ""),
        ] for i in options]
        chosen_config = self.table_select(
            title="Choose a cluster to switch on",
            table_data=table_data,
            header=["Name", "Location", "Master version", "Master ip",
                    "Machine type", "Node version", "Nodes", "Status"],
        )
        if chosen_config is None or chosen_config >= len(options):
            return
        gcloud.activate_kubernetes_cluster(options[chosen_config])
