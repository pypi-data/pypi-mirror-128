"""
Dummy view
"""

from gubert.views.View import View


class DummyExitView(View):
    """
    Dummy view
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def name() -> str:
        """
        Dummy view name
        """
        return "Exit"

    def handle(self) -> None:
        """
        Dummy handler
        """
        raise SystemExit("Exit requested")
