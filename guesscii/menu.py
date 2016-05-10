import subprocess, time

class Menu(object):
    """A database of pages to display pages to the user.

    Public methods:
        push ----- Go to another page
        back ----- Go to the previous page

    Calling the menu calls the last page on the page stack.

    The push and back methods are intended to be used right before
        calling the menu again.
    """

    def __init__(self):
        """Create a Menu object."""
        self.__pages = []


    #-----Public methods-----

    def push(self, page):
        """Push the specified page to the page stack.

        Arguments:
            page ----- page object

        Side Effects:
            Modifies the private pages property.
        """
        print 'pushing a page'
        raw_input('>>')
        pages = self._pages
        pages.append(page)
        self._pages = pages

    def back(self):
        """Remove the last page from the page stack.

        Side Effects:
            Modifies the private pages property.
        """
        pages = self._pages[:-1]
        self._pages = pages


    #-----Private properties-----

    @property
    def _pages(self):
        return self.__pages[:]

    @_pages.setter
    def _pages(self, pages):
        try:
            for page in pages:
                assert callable(page), page
        except AssertionError as e:
            raise TypeError('{} must be callable.'.format(type(e.args[0])))
        self.__pages = pages


    #-----Magic methods-----

    def __call__(self):
        print 'pages length:', len(self._pages)
        raw_input('>>')
        self._pages[-1]()


#------------------Testing--------------------

def test():
    from page import Page
    from option import Option

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
