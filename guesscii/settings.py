import string

class Settings(object):
    """An object that contains the data needed to create a game.

    Public Properties
        types ------- A positive integer greater than 1 that determines
                        the amount of letters to choose from when
                        creating a combination.

        length ------ A positive integer greater than 1 as the length of
                        each combination.

        attmepts ---- A positive integer greater than 1 as the amount of
                        times the user is allowed to guess the combination
                        before the game is lost.
    """
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
            types, length, and attempts are all integers greater than 1.

        Raises:
            A TypeError if any of the arguments passed aren't integers.
            A ValueError if any of the arguments passed aren't
              greater than one.
        """
        # Polymorphic defensive programming
        try:
            for arg in ('types', 'length', 'attempts'):
                assert type(eval(arg)) is int, TypeError(
                    '{} must be an int.'.format(arg))
                assert arg > 1, ValueError(
                    '{} must be greater than 1.'.format(arg))
        except AssertionError as e:
            raise e.args[0]

        # Attribute initializations
        self._types = types
        self._length = length
        self._attempts = attempts

def test():
    settings = Settings(6, 4, 6)
    for attribute in ('types', 'length', 'attempts'):
        print '{}: {}'.format(attribute, getattr(settings, attribute))

if __name__ == '__main__':
    test()
