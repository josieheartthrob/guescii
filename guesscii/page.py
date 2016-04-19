import subprocess, time, typing
check = typing.check

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
        check(({'function': typing.options,
                'args': (other,)},))

        # Main algorithm
        self._options = options

    @order.setter
    def order(self, other):
        # Defensive programming
        check(({'function': typing.order,
                'args':(other, self.options)},))

        # Main algorithm
        self._order = order

    @body.setter
    def body(self, other):
        # Defensive programming
        check(({'function': typing.obj_type,
                'args': (other, str, TypeError)},))

        # Main algorithm
        self._body = other


    #-----Magic methods-----

    def __init__(self, header, body, options, order,
                 parse=lambda x: (x, (), {})):
        """Assumes header and body are strings;
        options is a dictionary of options;
        order is the ordre to display the options;

        Create a page object."""

        # Defensive programming
        checks = [{'function': typing.obj_type,
                   'args': (arg, str, TypeError)}
                  for arg in (header, body)]
        checks.extend([{'function': typing.options,
                      'args': (options,)},
                     {'function': typing.order,
                      'args': (order, options)},
                     {'function': typing.functionality,
                      'args': (parse, TypeError)}])
        check(checks)

        # Initialize attributes
        self._header = header
        self._body = body
        self._options = options
        self._order = order
        self._parse = parse

    def __str__(self):
        s = '[{}]\n\n{}\n\n'.format(self.header, self.body)
        for key in self._order:
            s += self.options[key].__str__() + '\n'
        return s

    def __call__(self):
        key = ''
        while key not in self.options.keys():
            subprocess.call('cls', shell=True)
            print self
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
