import subprocess
from typing import check_options, check_order, check_type

def parse_input(data):
    # Defensive programming
    try:
        check_type(data, str, TypeError)
    except AssertionError as e:
        raise e.args[0]



class Page(object):

    #-----Public properties-----

    @property
    def options(self):
        """A dictionary where  each value is an option and each  key is
        the option's key"""
        return self._options.copy()

    @property
    def order(self):
        """The order the options are displayed."""
        return self._order[:]

    @property
    def header(self):
        """The header of the page."""
        return self._header

    @property
    def body(self):
        """The body of the page."""
        return self._body


    #-----Public property prescriptors-----

    @options.setter
    def options(self, other):
        # Defensive programming
        try:
            check_options(other)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._options = options

    @order.setter
    def order(self, other):
        # Defensive programming
        try:
            check_order(other)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._order = order

    @body.setter
    def body(self, other):
        check_type(other, str, TypeError)
        self._body = other


    #-----Magic methods-----

    def __init__(self, header, body, options, order,
                 parse=lambda x: (x, (), {})):
        """Assumes header and body are strings;
        options is a dictionary of options;
        order is the ordre to display the options;

        Create a page object."""

        # Defensive programming
        try:
            for arg in (header, body):
                check_type(arg, str)
            check_options(options)
            check_order(order)
            check_callable(parse, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Initialize attributes
        self._header = header
        self._body = body
        self._options = options
        self._order = order
        self._parse = parse

    def __str__(self):
        s = '[{}]\n\n{}\n'.format(self.header, self.body)
        for key in self._order:
            s += self.options[key] + '\n'
        return s

    def __call__(self,):
        key = ''
        while key not in self.options.keys():
            subprocess.call('cls', shell=True)
            print page
            try:
                key, args, kwargs = self._parse(raw_input('> '))
            except (ValueError, TypeError):
                raise TypeError
        return self.options[key], args, kwargs

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
