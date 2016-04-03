import subprocess
from page import Page
from typing import check_page

class Menu(object):
    """An interface class that displays information to the user and ac-
    cesses data from its parent Guesscii instance."""

    #-----Public methods-----

    @property
    def push(self):
        """Assumes page is a page object
        push the specified page to the stack."""
        return self._push

    @property
    def back(self):
        """Display the previous page."""
        return self._back


    #-----Private properties-----

    # Mutable
    @property
    def _page_stack(self):
        """The stack of pages."""
        return self.__page_stack[:]


    # -----Public method prescriptors-----

    def _push(self, page):
        # Defensive programming
        try:
            check_page(page)
        except AssertionError as e:
            raise e.args[0]

        self._page_stack.append(page)

    def _back(self):
        self._page_stack = self._page_stack[:-1]
        return self()


    # -----Magic methods-----

    def __init__(self, home):
        """Assumes home is a page object that doesn't have a back option.

        Create a Menu object."""

        # Defensive programming
        try:
            check_page(home)
            for option in home.options.itervalues():
                assert option != self.back, ValueError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__page_stack = [home]

    def __call__(self):
        self._page_stack[-1]()
