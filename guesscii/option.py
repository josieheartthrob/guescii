from typing import *

class Option(object):
    """An option to display on the screen.
    Options can be called for their functionality."""

    #-----Public properties-----

    # Immutable
    @property
    def key(self):
        """The option key."""
        return self._key

    @property
    def name(self):
        """The option name."""
        return self._name


    #-----Private properties-----

    @property
    def _function(self):
        """The functionality of the option."""
        return self.__function


    #-----Magic methods-----

    def __init__(self, key, name, function):
        """Assumes key and name are strings;
        function is a callable object or NoneType.

        Create an Option object"""

        # Defensive programming
        try:
            for arg in (key, name):
                check_type(arg, str, TypeError)
            check_functionality(function, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Initialize attributes
        self._key = key
        self._name = name
        self.__function = function

    def __str__(self):
        return '> {0.key} - {0.name}'.format(self)

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)
