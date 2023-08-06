"""
Abstract view
"""
from abc import ABC
from typing import Optional, List

from simple_term_menu import TerminalMenu
from tabulate import tabulate


class View(ABC):
    """
    Abstract view
    """

    SEARCH_HINT: str = "  Press '/' to search across options"
    GO_BACK: str = "Go Back"

    def __init__(self):
        self.context = dict()

    @staticmethod
    def name() -> str:
        """
        Returns view name intended to be shown on view render
        """
        raise NotImplementedError("This must be implemented!")

    def handle(self) -> None:
        """
        View handler. Context is allowed for both view
        enrichment and for mutation.
        """
        raise NotImplementedError("This must be implemented!")

    @staticmethod
    def table_select(
            title: str,
            table_data: List[List[str]],
            header: List[str],
            cursor_index: int = 0,
    ) -> Optional[int]:
        """
        Simple interactive list with column layout.
        Lines must not be multiline!
        :param title: Select title string
        :param table_data: table data
        :param header: header list
        :param cursor_index: preselected row position
        :return: selected index or (max index + 1 / None) if got back
        """
        for row in table_data:
            for cell in row:
                if "\n" in row:
                    raise ValueError(f"Multiline cells are "
                                     f"not supported: '{cell}'!")
        table = tabulate(table_data + [[View.GO_BACK]] + [header],
                         tablefmt="plain").split("\n")
        rendered_options = table[:-1]
        status = ["  " + table[-1], View.SEARCH_HINT]
        return TerminalMenu(
            status_bar=status,
            cursor_index=cursor_index,
            title=title,
            menu_entries=rendered_options,
        ).show()
