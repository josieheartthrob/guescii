import random
from menu import Menu
from game import Game
from option import Option
from settings import Settings

class Guesscii(object):
    """The main class that handles the program."""

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
        return self.__settings


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
        return self.__continue_game

    @property
    def help_page(self):
        return self.__help_page

    @property
    def about_page(self):
        return self.__about_page

    #--------------------------------------------------------------------------


    # -----Public property prescriptors-----

    @game.setter
    def game(self, game):
        """Assumes game is a Game object.

        Modify the game property."""

        # Polymorphic defensive programming
        try:
            assert hasattr(game, 'main'), TypeError
            assert callable(game.main), AttributeError

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

    def __continue_game(self):
        raise NotImplementedError

    def __help_page(self):
        raise NotImplementedError

    def __about_page(self):
        raise NotImplementedError


    # -----Magic methods-----

    def __init__(self):
        self.__options = {
            "n": Option("n", "new game", self.new_game),
            "q": Option("q", "quit", quit),
            "h": Option("h", "help", self.help_page),
            "i": Option("i", "about", self.about_page),
            "\n": ""}
        self.__menu = Menu(self)
        self.__defaults = Settings()
        self.__settings = self.defaults
        self.__game = None

        options = {
            "m": Option("m", "menu", self.__menu.get_choice),
            "s": Option("s", "settings", self.__menu.change_settings),
            "t": Option("t", "amount of letters chosen from",
                        self.settings.change_types),
            "d": Option("d", "combination length",
                        self.settings.change_length),
            "a": Option("a", "attempts allowed",
                        self.settings.change_attempts),
            "b": Option("b", "back", self.__menu.back),
            "\n": ""}
        for key, option in options.iteritems():
            self.__options[key] = option

if __name__ == '__main__':
    guesscii = Guesscii()
    guesscii.main()
