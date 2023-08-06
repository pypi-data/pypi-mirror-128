"""
Various utility classes
"""
from typing import List

from simple_term_menu import TerminalMenu

from gubert.views.View import View


class VersionTuple(tuple):
    """
    Representation of version X.Y.Z
    """

    def __new__(cls, s):
        return super().__new__(cls, map(int, s.split(".")))

    def __repr__(self):
        return ".".join(map(str, self))

    def __str__(self):
        return self.__repr__()


class ViewRenderer(object):
    """
    Utility class for showing menu to choose of views to render
    """

    @staticmethod
    def show(views: List[View], title: str) -> None:
        """
        Renders menu of views
        """
        while True:
            status: List[str] = [View.SEARCH_HINT]
            chosen: int = TerminalMenu(
                status_bar=status,
                title=title,
                menu_entries=[view.name() for view in views],
            ).show()
            if chosen is None or chosen >= len(views):
                return
            action: View = views[chosen]
            try:
                action.handle()
            except SystemExit:
                return
