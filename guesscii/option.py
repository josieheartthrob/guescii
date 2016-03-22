class Option(object):
    """An option to display on the screen.
    Options can be called for their functionality."""

    #-----Public properties-----

    # Immutable
    @property
    def key(self):
        """The option key."""
        return self.__key

    @property
    def name(self):
        """The option name."""
        return self.__name

    # Mutable
    @property
    def function(self):
        """The functionality of the option."""
        # Defensive programming
        try:
            assert type(function) != None, AttributeError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        return self.__function


    #-----Public property prescriptors-----

    @function.setter
    def function(self, function):
        """Assumes function is a callable object.
        Modify the function property"""

        # Polymorphic defensive programming
        try:
            assert callable(function), TypeError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__function = function


    #-----Magic methods-----

    def __init__(self, key, name, function):
        """Assumes key and name are strings;
        function is a callable object or NoneType.

        Create an Option object"""

        # Defensive programming
        try:
            for arg in (key, name):
                type(arg) == str, TypeError
            if function:
                assert callable(function), TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Initialize attributes
        self.__key = key
        self.__name = name
        self.__function = function

    def __str__(self):
        return "> {0.key} - {0.name}".format(self)

    def __call__(self):
        self.function()
