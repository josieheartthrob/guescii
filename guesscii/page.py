import subprocess

class Page(object):

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
        self._options = options

    @order.setter
    def order(self, other):
        self._order = order

    @body.setter
    def body(self, other):
        self._body = other


    #-----Magic methods-----

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

    def __str__(self):
        s = '[{}]\n\n'.format(self.header)
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
                self.options[key](*args, **kwargs)
                return
            except KeyError:
                continue

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

# option, args, kwargs = menu page, (), {}
# while True
#     option, args, kwargs = option(*args, **kwargs)

# call settings page option
#     display page
#     get [change settings] input from user
#     parse input to option key, args, kwargs
#         parse input to settings
#         key = settings key, args = (settings), kwargs = {}
#         return key, args, kwargs
#     return option dict[settings key], args, kwargs

# call change settings option with settings arg
#     change current settings
#     change settings page body to inform user changes were saved
#     return settings page option

# call settings page option
#     display the page
#     get [go back] input from the user
#     parse input to option key, args, kwargs
#         key = user input, args = (), kwargs = {}
#         return key, args, kwargs
#     return option dict[key], args, kwargs
