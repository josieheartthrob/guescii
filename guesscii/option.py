class Option(object):
    """An option to display on the screen.
    Options can be called for their functionality."""

    #-----Public properties-----

    @property
    def key(self):
        """The option key."""
        return self.__key

    @property
    def name(self):
        """The option name."""
        return self.__name


    #-----Private properties-----

    @property
    def __function(self):
        """The functionality of the option."""
        return self.___function


    # -----Magic methods-----

    def __init__(self, key, name, function):
        """Assumes key and name are strings;
        function is a callable object.

        Create an Option object"""

        # Defensive programming
        try:
            for arg in (key, name):
                assert hasattr(arg, "__str__"), TypeError
                assert callable(arg.__str__), AttributeError
            assert callable(function), TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Initialize attributes
        self.___function = function
        self.__key = key
        self.__name = name

    def __str__(self):
        return "> {0.key} - {0.name}".format(self)

    def __call__(self):
        self.__function()
