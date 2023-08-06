"""
Entrypoint
"""
from gubert.utils import ViewRenderer
from gubert.views.DiscoverGcloudKubernetesCluster import \
    DiscoverGcloudKubernetesCluster
from gubert.views.DummyExitView import DummyExitView
from gubert.views.SwitchGcloudConfigration import \
    SwitchGcloudConfigurationView

MAIN_STATUS_HELP = "I'm Gubert. What do you want to do?"


def main():
    """
    Entrypoint
    """
    ViewRenderer.show([
        SwitchGcloudConfigurationView(),
        DiscoverGcloudKubernetesCluster(),
        DummyExitView(),
    ], MAIN_STATUS_HELP)


if __name__ == "__main__":
    # TODO argparse for verbose, timeout and gcloud path
    main()
