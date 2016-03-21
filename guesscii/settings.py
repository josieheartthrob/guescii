class Settings(object):
    """An object that contains the data needed to create a game."""

    #-----Public properties-----

    @property
    def types(self):
        """An integer that represents the amount of letters in the pool
        of letters the game chooses from when creating a random combin-
        ation."""
        return self.__types

    @property
    def length(self):
        """An integer that represents the length of the answer combina-
        tion as well as each guess."""
        return self.__length

    @property
    def attempts(self):
        """An integer  that represents the amount of  attempts the user
        is given to guess the answer combination."""
        return self.__attempts


    #-----Magic Methods-----

    def __init__(self, types=6, length=4, attempts=10):
        """Assumes  types, length, and attempts are  all integers grea-
        ter than 1."""

        # Polymorphic defensive programming
        try:
            for arg in (types, length, attempts):
                assert type(arg) == int
                assert arg > 1, ValueError

        except (AssertionError, TypeError) as e:
            raise e.args[0]

        # Attribute initializations
        self.__types = types
        self.__length = length
        self.__attempts = attempts