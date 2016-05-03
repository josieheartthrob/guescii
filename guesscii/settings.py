import string

class Settings(object):
    """An object that contains the data needed to create a game."""

    #-----Public properties-----

    # Modified the Docstrings to fit standards
    @property
    def types(self):
        """The integer amount of different letters to create a combination."""
        return string.lowercase[:self._types]

    @property
    def length(self):
        """The integer length of each combination."""
        return self._length

    @property
    def attempts(self):
        """The integer amount of guesses allowed."""
        return self._attempts


    #-----Magic methods-----

    def __init__(self, types=6, length=4, attempts=10):
        """Create a Settings Object.

        Keyword Arguments:
            types, length, and attempts are  all integers greater than 1.

        Raises:
            an exception if any of the passed arguments aren't positive integers"""

        # Polymorphic defensive programming
        try:
            for arg in (types, length, attempts):
                assert type(arg) == int
                assert arg > 1, ValueError

        except (AssertionError, TypeError) as e:
            raise e.args[0]

        # Attribute initializations
        self._types = types
        self._length = length
        self._attempts = attempts
