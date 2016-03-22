import string, subprocess, random
from representation import GameRep, EXACT, SIMILAR

# Global aliases
EXACT_CHAR, SIMILAR_CHAR = EXACT, SIMILAR

class Game(object):
    """The main class that runs the actual game."""

    #-----Public methods-----

    @property
    def main(self):
        """Run the actual game.
        Yield an option object."""
        return self.__main


    #-----Private properties-----

    # Immutable
    @property
    def __settings(self):
        """The settings dictionary."""
        return self.___settings

    @property
    def __types(self):
        """A string of all the differenct characters the combination chooses from."""
        return self.___types

    @property
    def __options(self):
        """A dictionary of option objects where each key is a string."""
        return self.___options

    @property
    def __option_order(self):
        """An ordered list of options to display."""
        return self.___option_order

    @property
    def __answer(self):
        """The answer combination."""
        return self.___answer


    #-----Private methods-----

    @property
    def __build_answer(self):
        """Create a  randomized string of lower-case  letters based off
        the settings."""
        return self.___build_answer

    @property
    def __build_hint(self):
        """Return a string that gives the user info about their guess."""
        return self.___build_hint

    #--------------------------------------------------------------------------


    #-----Public method prescriptors-----

    def __main():
        for i in xrange(self.__settings.attempts):
            guess = ''
            while (len(guess) != self.__settings.length or
                   guess not in self.__option_order):

                # Clear the screen and display the game
                subprocess.call("cls", shell=True)
                print self

                guess = raw_input("> ")
                # parse the guess
                guess = ''.join([c.lower() for c in guess if
                                 c.lower() in self.__types])

            if guess in self.__option_order:
                yield self.parent.options[guess]

            self.__rep.add_guess(guess)

            hint = self.__build_hint(guess)
            self.__rep.add_hint(hint)

            if guess == self.__answer:
                self.__rep.answer = self.__answer
                yield self.parent.options["n"]


    #-----Private method prescriptors-----

    def ___build_hint(self, guess):
        # Polymorphic defensive programming
        try:
            assert type(guess) == str, TypeError

            # Helper variables
            letters = string.lowercase[:self.__settings.types]

            # Check the guess
            for c in guess:
                assert c in letters, ValueError
            assert len(guess) == self.__settings.length, ValueError

        except AssertionError as excpetion:
            raise exception.args[0]

        # Helper variables
        guess_map = {c: guess.count(c) for c in set(guess)}
        answer_map = {c: self.__answer.count(c) for c in  set(self.__answer)}

        # Main algorithm
        exact = sum([1 for i, c in enumerate(guess) if c == answer[i]])
        similar = (sum([min(guess_map[c], answer_map[c]) for
                        c in answer_map if c in guess_map]) - exact)
        return EXACT_CHAR*exact + SIMILAR_CHAR*similar

    def ___build_answer(self):
        answer = ""
        for i in xrange(self.__settings.length):
            answer += random.choice(self.__settings.types)
        return answer


    #-----Magic methods-----

    def __init__(self, settings, options, order=['n', 'q']):
        """Assumes settings is a settings dictionary;
        Options is a dictionary of options;
        Order is sequence of characters that represents the option order."""

        # Polymorphic defensive programming
        try:
            # check settings
            for attribute in ('types', 'length', 'attempts'):

                # Helper variables
                attribute_type = type(getattr(settings, attribute))

                # Run checks
                assert hasattr(settings, attribute), TypeError
                assert attribute_type == int, AttributeError

            # check options
            for attribute in ('iteritems', 'keys'):
                assert hasattr(options, attribute), TypeError
                assert callable(getattr(options, attribute)), AttributeError
            for key, option in options.iteritems():
                assert type(key) == str, TypeError
                if type(option) != str:
                    for attribute in ('key', 'name'):
                        assert hasattr(option, attribute), TypeError
                        option_attribute = getattr(option, attribute)
                        assert type(option_attribute), TypeError
                    assert key == option.key
                    assert callable(option)

            # check order
            assert hasattr(order, '__getitem__'), TypeError
            assert callable(order.__getitem__), AttributeError
            for c in order:
                assert type(c) == str
                assert c in options.keys()

        except AssertionError as exeption:
            raise exception.args[0]

        # Initialize attributes
        self.___options = options
        self.___settings = settings
        self.___types = string.lowercase[:settings.types]
        self.___option_order = order
        self.___rep = GameRep(settings)
        self.___answer = self.__build_answer()

    def __str__(self):
        s = self.__representation.__str__()
        for key in self.__option_order:
            s += self.__options[key].__str__()+'\n'
        return s
