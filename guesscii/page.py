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

              It should return an a key to access one of the page's options,
              and arguments and keyword arguments to call the option with.
              It should raise a ParseError if the data entered by the user
              is invalid.
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
        i = len(self.body)
        while True:
            subprocess.call('cls', shell=True)
            print self
            if len(self.body) > i:
                self.body = self.body[:i]
            try:
                key, args, kwargs = self._parse(raw_input('> '))
                return self.options[key](*args, **kwargs)
            except ParseError as e:
                self.body += '\n\n'+e.args[0]

class ParseError(Exception):
    def __init__(self, message='Invalid input.'):
        Exception.__init__(self, message)

#-----------------------------------------------------------------------------


def test():
    from option import Option
    def say(something):
        subprocess.call('cls', shell=True)
        print something
        raw_input('> ')

    def bye():
        say('bye')
        subprocess.call('cls', shell=True)
        quit()

    def parse(data):
        key, args, kwargs = data, (), {}
        if data == 'h':
            args = ('hi',)
        elif data != 'b':
            raise ParseError('"{}" is not a valid input.'.format(data))
        return key, args, kwargs

    page = Page('test page', 'some\narbitrary\nwords',
        {'h': Option('h', 'say hi', say),
         'b': Option('b', 'say bye', bye)},
        ['h', 'b'], parse)

    while True:
        page()

if __name__ == '__main__':
    test()
