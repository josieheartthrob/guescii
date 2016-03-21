import string, subprocess, random
from representation import GameRep, EXACT, SIMILAR

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
        return self.___settings.copy()

    @property
    def __options(self):
        """An ordered list of options to display."""
        return self.___options

    @property
    def __answer(self):
        """The answer combination."""
        return self.___answer

    @property
    def __answer_map(self):
        """The answer map."""
        return self.___answer_map.copy()

    # Mutable
    @property
    def __guess(self):
        """The user's current guess."""
        return self.___guess

    @property
    def __hint(self):
        """The current hint to display to the user."""
        return self.___hint

    @property
    def __guess_map(self):
        """A map of the amount of times a character occurs in the guess
        to the relative character."""

        # Defensive programming
        try:
            assert type(self.___guess_map) != None

        except AssertionError, excpetion:
            raise excpetion.args[0]

        # Main algorithm
        return self.___guess_map.copy()


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
            subprocess.call("cls", shell=True)
            print self
            self.__guess = raw_input("> ")
            self.__hint = self.__build_hint()
            if self.__guess in self.__options:
                yield self.parent.options[self.__guess]
            elif self.__guess == self.answer:
                self.reveal_answer()
                yield self.parent.options["n"]


    #-----Private property prescriptors-----

    @__guess.setter
    def __guess(self, guess):
        """Assumes guess is a string as long as the combination length.

        Modify the guess property to the given argument."""

        # Polymorphic defensive programming
        try:
            assert type(guess) == str, TypeError

            # Parse the guess
            guess = ''.join(
                [c.lower() for c in guess if c.lower() in string.lowercase])

            # Helper variables
            letters = string.lowercase[:self.__settings.types]

            # Check the guess
            for c in guess:
                assert c in letters, ValueError
            assert len(guess) == self.__settings.length, ValueError

        except AssertionError as excpetion:
            raise exception.args[0]

        # Main algorithm
        self.___guess = guess
        self.__guess_map = {L: guess.count(L) for L in set(guess)}

    @__guess_map.setter
    def __guess_map(self, m):
        """Assumes m is a mapping type where each key is a unique char-
        acter in the guess and  each value is the amount  of times that
        key occurs in the guess.

        Modify the __guess_map property."""

        # Polymorphic defensive programming
        try:
            for attribute in ("__iter__", "itervalues"):
                assert hasattr(m, attribute), TypeError
            for method in (m.__iter__, m.itervalues):
                assert callable(method), AttributeError
            assert m.keys() in set(self.__guess), ValueError
            for key in m:
                assert m[key] == self.__guess.count(key), ValueError

        except AssertionError as exception:
            raise excpetion.args[0]

        # Main algorithm
        self.___guess_map = m

    @__hint.setter
    def __hint(self, hint):
        """Assumes hint is a string;

        hint consists  only of the characters  determined by  the EXACT
        and SIMILAR global vairables defined in representation.py

        Modify the hint property to the given argument."""

        # Defensive programming
        try:
            assert type(hint) == str, TypeError
            for letter in hint:
                assert letter in (EXACT, SIMILAR), ValueError
            assert len(hint) <= self.__settings.length, ValueError

        except AssertionError as exception:
            raise exception.args[0]

        # Main algorithm
        self.__hint = hint


    #-----Private method prescriptors-----

    def ___build_hint(self):
        exact = sum([1 for i in xrange(len(self.__guess)) if
                     guess[i] == answer[i]])
        similar = (sum([min(self.__answer_map[letter],
                            self.__guess_map[letter])
                        for letter in self.__answer_map if
                        letter in self.__guess_map]) - exact)
        return EXACT*exact + SIMILAR*similar

    def ___build_answer(self):
        answer = ""
        for i in xrange(self.__settings.length):
            answer += random.choice(self.__settings.types)
        return answer


    #-----Magic methods-----

    def __init__(self, settings, parent):
        """Assumes settings is a settings dictionary;
        Parent is a Guesscii object."""

        # Polymorphic defensive programming
        try:
            # check settings
            for attribute in ('types', 'length', 'attempts'):

                # Helper variables
                attribute_is_int = type(getattr(settings, attribute)) == int

                # Run checks
                assert hasattr(settings, attribute), TypeError
                assert attribute_is_int, AttributeError

            # check parent
            assert hasattr(parent, 'options'), TypeError
            assert hasattr(parent.options, 'iteritems'), AttributeError
            assert callable(parent.options.iteritems), AttributeError
            for key, option in parent.options.iteritems():
                assert type(key) == str, TypeError
                for attribute in ('key', 'name'):
                    assert hasattr(option, attribute), TypeError
                    assert type(getattr(option, attribute)) == str, TypeError

        except AssertionError as exeption:
            raise exception.args[0]

        # Initialize attributes
        self.___parent = parent
        self.___settings = settings
        self.___options = ["n", "q"]
        self.___rep = GameRep(settings)

        self.___answer = self.__build_answer()
        self.___answer_map = {L: self.answer.count(L) for
                              L in set(self.answer)}

        self.___guess = None
        self.___guess_map = None

        self.___hint = None

    def __str__(self):
        return self.__representation.__str__()
