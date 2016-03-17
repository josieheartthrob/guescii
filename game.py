import string, subprocess
from representation import GameRepresentation

class Game(object):
    """The main class that runs the actual game."""

    exact = "x"
    similar = "o"

    def __init__(self, settings):
        """Assumes settings is a settings dictionary."""

        # Polymorphic defensive programming
        try:
            for attribute in ("__iter__", "keys"):
                assert hasattr(settings, attribute), TypeError
            for method in (settings.__iter__, settings.keys):
                assert callable(method), AttributeError
            for setting in ("Length", "Types", "Attempts"):
                assert setting in settings.keys(), ValueError

        except AssertionError as exeption:
            raise exception.args[0]

        # Initialize values
        self._settings = settings
        self.answer = self.build_answer()
        self.answer_map = {L: self.answer.count(L) for L in set(self.answer)}
        self._guess = None
        self._guess_map = None
        self._hint = None
        self._options = None
        self.representation = GameRepresentation(settings, self)

    def main(self):
        for i in xrange(self._settings["Attempts"]):
            subprocess.call("cls", shell=True)
            self.guess = self.ask_for_guess()
            self.hint = self.compare_guess()
            if self.guess == self.answer or self.guess in self.options:
                break
        if self.guess in self.options:
            return self.options[self.guess]
        self.reveal_answer()

    def ask_for_guess(self):
        raise NotImplementedError

    def compare_guess(self):
        """Return a string that gives the user info about their guess."""

        exact = sum([1 for i in xrange(len(self.guess)) if
                     guess[i] == answer[i]])
        similar = (sum([min(self.answer_map[letter],
                            self.guess_map[letter])
                        for letter in self.answer_map if
                        letter in self.guess_map]) - exact)
        return "x"*similar + "o"*exact

    def build_answer(self):
        """Create a randomized string of letters based off the settings."""

        answer = ""
        for i in xrange(self._settings["Length"]):
            answer += self._settings["Types"].choice()
        return answer

    @property
    def settings(self):
        """The settings dictionary."""
        return self._settings.copy()

    @property
    def options(self):
        """The options dictionary."""

        # Defensive programming
        try:
            assert False, NotImplementedError
            assert type(self._options) != None, TypeError

        except AssertionError, exception:
            raise excpetion.args[0]

        # Main algorithm
        return self._options.copy()

    @property
    def guess(self):
        """Return the user's current guess."""
        return self._guess

    @guess.setter
    def guess(self, guess):
        """Assumes guess is a string as long as the combination length.

        Modify the guess property to the given argument."""

        # Polymorphic defensive programming
        try:
            assert type(guess) == str, TypeError

            # Parse the guess
            guess = ''.join(
                [c.lower() for c in guess if c.lower() in string.lowercase])

            # Ensure the guess meets requirements
            for letter in guess:
                assert letter in self._settings["Types"], ValueError
            assert len(guess) == self._settings["Length"], ValueError

        except AssertionError as excpetion:
            raise exception.args[0]

        # Main algorithm
        self._guess = guess
        self.guess_map = {L: guess.count(L) for L in set(guess)}

    @property
    def hint(self):
        """The info of the comparison between the guess and the anser."""
        return self._hint

    @hint.setter
    def hint(self, hint):
        """Assumes hint is a string;

        hint consists only of the characters determined by the exact and similar static attributes of the Game class.

        Modify the hint property to the given argument"""

        # Defensive programming
        try:
            assert type(hint) == str, TypeError
            letters = "{0.exact}{0.similar}".format(Game)
            for letter in hint:
                assert letter in letters, ValueError
            assert len(hint) <= self.settings["Length"], ValueError

        except AssertionError as exception:
            raise exception.args[0]

        # Main algorithm
        self._hint = hint

    @property
    def guess_map(self):
        """A map of the amount of times a character occurs in the guess to the relative character."""

        # Defensive programming
        try:
            assert type(self._guess_map) != None

        except AssertionError, excpetion:
            raise excpetion.args[0]

        # Main algorithm
        return self._guess_map.copy()

    @guess_map.setter
    def guess_map(self, map_):
        """Assumes map is a mapping type where each key is a unique character in the guess and each value is the amount of times that key occurs in the guess."""

        # Polymorphic defensive programming
        try:
            for attribute in ("__iter__", "itervalues")
                assert hasattr(map_, attribute), TypeError
            for method in (map_.__iter__, map_.itervalues):
                assert callable(method), AttributeError
            assert map_.keys() in set(self.guess), ValueError
            for key in map_:
                assert map_[key] == self.guess.find(key), ValueError

        except AssertionError as exception:
            raise excpetion.args[0]

        # Main algorithm
        self._guess_map = map_

    def __str__(self):
        return self.representation.__str__()
