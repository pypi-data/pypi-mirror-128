"""
Switching configurations of gcloud
"""
from typing import List

from gubert.GcloudManager import GcloudManager, GcloudConfiguration
from gubert.views.View import View


class SwitchGcloudConfigurationView(View):
    """
    Switching configurations of gcloud
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def name() -> str:
        """
        View name for switching configurations of gcloud
        """
        return "Switch gcloud configuration"

    def handle(self) -> None:
        """
        Handles gcloud configuration switch dialog.
        """
        gcloud: GcloudManager = GcloudManager()
        options: List[GcloudConfiguration] = \
            gcloud.configurations_list()
        preselected_entry = \
            [i for i, o in enumerate(options) if o.is_active]
        cursor_index = preselected_entry[0] if preselected_entry else 0
        table_data = [[
            str(i.name or ""),
            str(i.is_active) if i.is_active else "",
            str(i.account or ""),
            str(i.project or ""),
        ] for i in options]
        chosen_config = self.table_select(
            title="Choose a configuration to activate",
            table_data=table_data,
            header=["Name", "Active", "Account", "Project"],
            cursor_index=cursor_index,
        )
        if chosen_config is None or chosen_config >= len(options):
            return
        gcloud.activate_configuration(options[chosen_config].name)
