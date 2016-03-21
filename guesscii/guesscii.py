import random
from menu import Menu
from game import Game
from option import Option
from settings import Settings

class Guesscii(object):
    """The main class that handles the program."""

    exact = "x"
    similar = "o"

    # -----Public properties-----

    @property
    def options(self):
        """The options dictionary."""
        return self.__options.copy()

    @property
    def game(self):
        """A game instance."""

        # Defensive programming
        try:
            assert type(self.__game) != None, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        return self.__game

    @property
    def defaults(self):
        """The default settings."""
        return self.__defaults.copy()

    @property
    def settings(self):
        """The game's current settings."""
        return self.__settings.copy()


    # -----Public methods-----

    @property
    def main(self):
        """The loop that runs the program."""
        return self.__main

    @property
    def new_game(self):
        """Play the game with the current settings."""
        return self.__new_game

    @property
    def continue_game(self):
        """Continue the current game."""
        raise NotImplementedError

    @property
    def help_page(self):
        raise NotImplementedError

    @property
    def about_page(self):
        raise NotImplementedError

    #--------------------------------------------------------------------------


    # -----Public property prescriptors-----

    @game.setter
    def game(self, game):
        """Assumes game is a Game object.

        Modify the game property."""

        # Polymorphic defensive programming
        try:
            # Check the game object
            for attribute in ("main", "settings"):
                assert hasattr(game, attribute), TypeError

            # Check the game attribute
            assert callable(game.main), AttributeError

            # Check the settings attribute
            for attribute in ('types', 'length', 'attempts'):
                assert hasattr(settings, attribute), TypeError

                # Helper variables
                attribute_type = getattr(settings, attribute)

                # Check the settings' attributes
                assert attribute_type == int, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self.__game = game

    @game.deleter
    def game(self):
        self.__game = None


    @settings.setter
    def settings(self, settings):
        """Assumes settings is a settings object.

        Modify the current settings."""

        # Polymorphic defensive programming
        try:
            assert False, NotImplementedError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self.__settings = settings


    # -----Public method prescriptors-----

    def __main(self):
        option = self.options["m"]
        while True:
            try:
                option = option()
            except ValueError:
                continue

    def __new_game(self):
        del self.game
        self.game = Game(self.settings)
        return self.game.main()


    # -----Magic methods-----

    def __init__(self):
        self.__menu = Menu()
        self.__defaults = Settings()
        self.__settings = self.defaults
        self.__options = {
            "m": Option("m", "menu", self.__menu.get_choice),
            "n": Option("n", "new game", self.new_game),
            "c": Option("c", "continue game", self.continue_game),
            "q": Option("q", "quit", quit),
            "s": Option("s", "settings", self.__menu.change_settings),
            "t": Option("t", "amount of letters chosen from",
                        self.settings.change_types),
            "d": Option("d", "combination length",
                        self.settings.change_length),
            "a": Option("a", "attempts allowed",
                        self.settings.change_attempts),
            "h": Option("h", "help", self.help_page),
            "i": Option("i", "about", self.about_page),
            "b": Option("b", "back", self.__menu.back),
            "\n": ""}
        self.__game = None

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
