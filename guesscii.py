import random, test_guess
from menu import Menu
from game import Game

class Guesscii(object):
    """The main class that handles the program"""

    def __init__(self):
        self.menu = Menu()
        self._default_settings = {
            "Types": 6,
            "Length:" 4,
            "Attempts": 10}
        self._current_settings = self.default_settings
        self._game = None

    def main(self):
        while True:
            try:
                option = self.menu.get_choice()
            except ValueError:
                continue
            option()

    def play_game(self):
        """Play the game with the given settings."""

        # Polymorphic defensive programming
        try:
            assert type(settings) == dict

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self.game = Game(self.settings)
        self.game.main()
        del self.game

    @property
    def game(self):
        """A game instance."""

        # Defensive programming
        try:
            assert type(self._game) != None, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        return self._game

    @game.setter
    def game(self, game):
        """Assumes game is a Game object.

        Modify the game property."""

        # Polymorphic defensive programming
        try:
            for attribute in ("main", "settings"):
                assert hasattr(game, attribute), TypeError
            assert callable(game.main), AttributeError
            assert type(game.settings) == dict, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._game = game

    @game.deleter
    def game(self):
        self._game = None

    @property
    def default_settings(self):
        """The default settings."""
        return self._default_settings.copy()

    @property
    def current_settings(self):
        """The game's current settings."""
        return self._current_settings.copy()

    @current_settings.setter
    def current_settings(self, settings):
        """Assumes settings is a settings dictionary.
        Modify the current settings."""

        # Polymorphic defensive programming
        try:
            assert False, NotImplementedError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._current_settings = settings

if __name__ == '__main__':
    guesscii = Guescii()
    guesscii.main()

# def play_game(settings):
#     """Assumes settings is a settings dictionary"""
#     combination = make_random_sequence(
#         settings["guess types"], settings["combination length"])
#     guess = get_guess(settings["guess types"], settings["guesses"])
#     while guess != combination:
#         print check_guess(guess)
#         guess = get_guess(settings["guess types"], settings["guesses"])
#     print "You Win!"
#
# def customize_settings():
#     """returns a settings dictionary"""
#
#     restore_defaults = raw_input("restore defaults? y | n\n\n> ")
#     while restore_defaults not in ("y", "n"):
#         restore_defaults = raw_input(
#             "invalid input\nplease type \"y\" or \"n\":\n\n> ")
#
#     if restore_defaults == "n":
#         settings = {"guess types": 0, "combination length": 0, "guesses": 0}
#         settings["guess types"] = ensure_int(
#             "amount of guess types: ", sign="positive")
#         settings["combination length"] = ensure_int(
#             "length of each guess: ", sign="positive")
#         settings["guesses"] = ensure_int(
#             "amount of guesses: ", sign="positive")
#     else:
#         settings = get_defaults()
#     return settings
