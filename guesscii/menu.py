import subprocess
from option import Option
from page import Page

class Menu(object):
    """An interface class that displays information to the user and ac-
    cesses data from its parent Guesscii instance."""

    #-----Public methods-----

    @property
    def push(self):
        """Not implemented."""
        return self._push

    @property
    def back(self):
        """Display the previous page."""
        return self._back


    #-----Public properties-----

    @property
    def pages(self):
        """A dictionary of pages."""
        return self._pages


    #-----Private properties-----

    # Mutable
    @property
    def _page_stack(self):
        """The stack of pages."""
        return self.__page_stack[:]

    #--------------------------------------------------------------------------


    # -----Public method prescriptors-----

    def _get_choice(self, page):
        key = ''
        while key not in page.order:
            subprocess.call('cls', shell=True)
            print page
            key = raw_input('> ')
        return page.options[key]()

    def _push(self, page):
        # Defensive programming
        try:
            check_page(page)
        except AssertionError as e:
            raise e.args[0]

        self._page_stack.append(page)

    def _back(self):
        self._page_stack = self._page_stack[:-1]
        return self._page_stack[-1]()


    # -----Magic methods-----

    def __init__(self, pages, home):
        """Assumes pages is a dictionary of Page objects;
        home is a key in pages.

        Create a Menu object."""
        # Defensive programming
        for method in ('iteritems', 'keys'):
            check_method(pages, method, TypeError)
        for key, page in pages.iteritems():
            chek_type(key, str, KeyError)
            check_page(page)
        assert home in pages.keys(), TypeError

        # Initialize attributes
        self._pages = pages
        self.__page_stack = [pages[key] for key in stack]
