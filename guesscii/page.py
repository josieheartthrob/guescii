import subprocess

class Page(object):
    """"""

    def __init__(self, header, body, options, order,
                 parse=lambda x: (x, (), {})):
        """Create a page object.

        Arguments:
            header ----- A string that let's the user know what the
                            page is about.
            body ------- A string that gives the user any information.
            options ---- a dictionary of option objects where each key is
                            the relative item's (option object's) key
            order ------ An ordered container object as the order in which
                            to display the options to the page

        Keyword Arguments:
            parse ------ A callable object that parses the data entered by
                            the user when the page is called.

                            It should return an a key to access one of the
                            page's options, and arguments and keyword
                            arguments to call the option with.
        """
        self._header = header
        self._body = body
        self._options = options
        self._order = order
        self._parse = parse

    #-----Public properties-----

    @property
    def options(self):
        return self._options.copy()

    @property
    def order(self):
        return self._order[:]

    @property
    def header(self):
        return self._header

    @property
    def body(self):
        return self._body


    #-----Public property prescriptors-----

    @options.setter
    def options(self, other):
        if not callable(other):
            raise TypeError(
                '{} must be a callable object'.format(type(other)))
        self._options = options

    @order.setter
    def order(self, other):
        self._order = other

    @body.setter
    def body(self, other):
        if not hasattr(other, '__str__'):
            raise TypeError('{} must be a string'.format(other))
        self._body = other


    #-----Magic methods-----

    def __str__(self):
        s = ''
        if self._header:
            s += '[{}]\n\n'.format(self.header)
        if self._body:
            s += self._body + '\n\n'
        for key in self._order:
            s += self.options[key].__str__() + '\n'
        return s

    def __call__(self):
        key = ''
        while True:
            try:
                subprocess.call('cls', shell=True)
                print self
                key, args, kwargs = self._parse(raw_input('> '))
                return self.options[key](*args, **kwargs)
            except KeyError:
                continue


#-----------------------------------------------------------------------------


def test():
    import time
    from option import Option
    def say(something):
        subprocess.call('cls', shell=True)
        print something
        time.sleep(1)

    def parse(data):
        key, args, kwargs = data, (), {}
        if data == 'h':
            args = ('hi',)
        elif data == 'b':
            args = ('bye',)
        else:
            print 'invalid input'
            raise ValueError
        return key, args, kwargs

    page = Page('test page', 'some\narbitrary\nwords',
        {'h': Option('h', 'say hi', say),
         'b': Option('b', 'say bye', say)},
        ['h', 'b'], parse)

    for i in xrange(3):
        page()

if __name__ == '__main__':
    test()
