import string
from representation import GameRepresentation

class Game(object):
    """The main class that runs the actual game."""

    correct = "x"
    similar = "o"

    def __init__(self, settings):
        """Assumes settings is a settings dictionary."""

        # Polymorphic defensive programming
        try:
            assert type(settings) == dict, TypeError

            # Make sure the dictionary has the right keys
            for setting in ("Types", "Length", "Attempts"):
                assert setting in settings.keys(), ValueError

        except AssertionError as exeption:
            raise exception.args[0]

        # Initialize values
        self.__settings = settings
        self.representation = GameRepresentation(settings)
        self.answer = self.build_answer()
        self.answer_map = {L: self.answer.count(L) for L in set(self.answer)}
        self.__guess = None
        self.__info = None

    def main(self):
        for i in xrange(self.__settings["Attempts"]):
            self.guess = self.ask_for_guess()
            if self.guess == self.answer:
                break
            self.info = self.compare_guess()

    def ask_for_guess(self):
        raise NotImplementedError

    def compare_guess(self):
        """Return a string that gives the user info about their guess."""

        total_similar = sum(self.answer_map.itervalues())
        correct, similar = self.differentiate_letters(self.guess, total_similar)
        return self.parse_into_answer_info(correct, similar)

    @property
    def settings(self):
        """The settings dictionary."""
        return self.__settings.copy()

    @property
    def guess(self):
        """Return the user's current guess."""
        return self.__guess

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
                assert letter in self.__settings["Types"], ValueError
            assert len(guess) == self.__settings["Length"], ValueError

        except AssertionError as excpetion:
            raise exception.args[0]

        # Main algorithm
        self.__guess = guess

    @property
    def info(self):
        """The info of the comparison between the guess and the anser."""
        return self.__info

    @info.setter
    def info(self, information):
        """Assumes information is a string;

        information consists only of the characters determined by the correct and similar static attributes of the Game class.

        Modify the info property to the given argument"""

        # Defensive programming
        try:
            assert type(information) == str, TypeError
            letters = "{0.correct}{0.similar}".format(Game)
            for letter in information:
                assert letter in letters, ValueError
            assert len(information) <= self.settings["Length"], ValueError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self.__info = information

    def build_answer(self):
        """Create a randomized string of letters based off the settings."""

        answer = ""
        for i in xrange(self.__settings["Length"]):
            answer += self.__settings["Types"].choice()
        return answer

    def differentiate_letters(self, similar):
        """Assumes similar is a positive integer;
        Guess is a string as long as the combination length

        similar is the total amount of similar letters in the guess

        Return the amount of correct letters and the ammount of similar letters in the guess."""

        # Defensive programming
        try:
            assert type(similar) == int, TypeError
            assert similar >= 0, ValueError

        except AssertionError as exception:
            raise exception.args[0]

        # Main algorithm
        correct = 0
        for i in xrange(len(self.guess)):
            if self.guess[i] == self.answer[i]:
                similar -= 1
                correct += 1
        return correct, similar

    def parse_into_answer_info(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
