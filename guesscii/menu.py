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
        self._pages = []

    @property
    def pages(self):
        return self._pages[:]

    #-----Public methods-----

    def push(self, page):
        """Push the specified page to the page stack.

        Arguments:
            page ----- page object

        Side Effects:
            Modifies the private pages property.
        """
        if not callable(page):
            raise TypeError('Only callable objects can be ' +
                             'added to the page stack.')
        self._pages.append(page)

    def back(self):
        """Remove the last page from the page stack.

        Side Effects:
            Modifies the private pages property.
        """
        self._pages = self._pages[:-1]

    def home(self):
        """Remove all pages from the page stack except for the first.

        Side Effects:
            Modifies the private pages property."""
        self._pages = self._pages[:1]



    #-----Magic methods-----

    def __call__(self):
        self._pages[-1]()


#------------------Testing--------------------

def test():
    from page import Page, ParseError
    from option import Option

    menu = Menu()

    def parse_1(data):
        args, kwargs = [], {}
        if data == 'n':
            args = [page_2]
        elif data != 'q':
            raise ParseError('"{}" is not a valid input'.format(data))
        return data, args, kwargs

    def parse_2(data):
        args, kwargs = [], {}
        if data == 'n':
            args = [page_3]
        elif data != 'b':
            raise ParseError('"{}" is not a valid input'.format(data))
        return data, args, kwargs

    def parse_3(data):
        if data not in page_3.order:
            raise ParseError('"{}" is not a valid input'.format(data))
        return data, (), {}

    page_1 = Page('test page', '', {
            'n': Option('n', 'next page', menu.push),
            'q': Option('q', 'quit', quit)},
        ['n', 'q'], parse_1)

    page_2 = Page('test page 2', '', {
            'n': Option('n', 'next page', menu.push),
            'b': Option('b', 'back', menu.back)},
        ['n', 'b'], parse_2)

    page_3 = Page('', 'this is the 3rd test page', {
            'b': Option('b', 'back', menu.back),
            'h': Option('h', '1st page', menu.home)},
        ['b', 'h'], parse_3)

    menu.push(page_1)
    while True:
        menu()

if __name__ == '__main__':
    test()
