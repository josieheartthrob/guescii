import subprocess, typing, time

# Modified Docstrings to fit standards
class Menu(object):
    """Display information to the user and access game data."""

    #-----Private properties-----

    # Made the pages property modifiable and implemented it throughout the code
    # Mutable
    @property
    def _pages(self):
        """The stack of pages."""
        return self.__pages[:]

    @_pages.setter
    def _pages(self, pages):
        # Defensive programming
        try:
            typing.method(pages, '__getitem__', TypeError)
            for page in pages:
                typing.page(page)
        except AssertionError as e:
            raise e.args[0]

        self.__pages = pages


    #-----Public methods-----

    def push(self, page):
        """Push the specified page to the stack.

        Arguments:
            page ----- page object

        Side Effects:
            Modifies the private pages property.

        Raises:
            An exception if the page is invalid."""

        # Defensive programming
        try:
            typing.page(page)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        pages = self._pages
        pages.append(page)
        self._pages = pages

    def back(self):
        """Go to the previous page.

        Side Effects:
            Modify the private pages property"""
        pages = self._pages[:-1]
        self._pages = pages


    #-----Magic methods-----

    def __init__(self):
        """Create a Menu object."""
        self.__pages = []

    def __call__(self):
        """Call the page at the top of the stack."""
        self._pages[-1]()


# Added a seperator comment
#------------------Testing------------------

def test():
    from page import Page
    from option import Option

    # changed the name of the m variable to menu
    menu = Menu()

    def parse_1(data):
        args, kwargs = [], {}
        if data == 'n':
            args = [page_2]
        elif data != 'q':
            raise ValueError
        return data, args, kwargs

    page_1 = Page('test page', '', {
            'n': Option('n', 'next page', menu.push),
            'q': Option('q', 'quit', quit)},
        ['n', 'q'], parse_1)

    page_2 = Page('test page 2', '', {
        'b': Option('b', 'back', menu.back)}, ['b'])

    menu.push(page_1)
    while True:
        menu()

if __name__ == '__main__':
    test()
