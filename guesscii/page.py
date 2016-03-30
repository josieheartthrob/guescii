import subprocess

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


    #-----Private properties-----

    @property
    def _header(self):
        """The header of the page."""
        return self.__header

    @property
    def _body(self):
        """The body of the page."""
        return self.__body


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
            check_order(other):
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._order = order


    #-----Magic methods-----

    def __init__(self, header, body, options, order):
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
        except AssertionError as e:
            raise e.args[0]

        # Initialize attributes
        self.__header = header
        self.__body = body
        self._options = options
        self.__order = order

    def __str__(self):
        s = '[{}]\n\n{}\n'.format(self._header, self._body)
        for key in self._order:
            s += self.options[key] + '\n'
        return s
