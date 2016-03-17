class Option(object):
    """An option to display on the screen.
    Set the function for the option after it's been initialized
    Options can be called for their functionality."""

    invalid_option = "You entered an invalid option.\n" \
                      "Please choose between [{0}]\n"

    def __init__(self, key, name):
        """Assumes key and name are strings;
        function is a callable object.

        Create an Option object"""

        # Defensive programming
        try:
            assert type(key), type(name) == str, TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Initialize attributes
        self._function = None
        self.key = key
        self.name = name

    @property
    def function(self):
        """The function to call for the option."""

        # Defensive programming
        try:
            assert type(self._function) != None, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        return self._function

    @function.setter
    def function(self, f):
        """Assumes f is a callable object.

        Set the function property to f."""

        # Polymorphic defensive programming
        try:
            assert callable(f), TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._function = f

    def __str__(self):
        return "> {0.key} - {0.name}".format(self)

    def __call__(self):
        self.function()
