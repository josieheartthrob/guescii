import random, subprocess, re
from page import Page, ParseError
from menu import Menu
from game import Game
from option import Option
from settings import Settings

class Guesscii(object):
    """The main class that handles the program."""

    def __init__(self):
        self.__defaults = Settings()
        self.__settings = self._defaults
        self.__menu = Menu()
        self._pages =  {
            'help': Page('Help', 'coming soon', {
                'b': Option('b', 'back', self._menu.back)}, ['b']),
            'about': Page('About', 'coming soon', {
                'b': Option('b', 'back', self._menu.back)}, ['b']),
            'types': Page('Change amount of letters to choose from', '', {
                'c': Option('c', 'cancel', self._menu.back)}, ['c']),
            'length': Page('Change the length of the combination', '', {
                'c': Option('c', 'cancel', self._menu.back)}, ['c']),
            'attempts': Page('Change the amount of attempts allowed', '', {
                'c': Option('c', 'cancel', self._menu.back)}, ['c'])}
        self._pages['menu'] = Page('Menu', '', {
            'n': Option('n', 'new game', self.new_game),
            'q': Option('q', 'quit', quit),
            's': Option('s', 'settings', self._menu.push),
            'h': Option('h', 'help', self._menu.push),
            'i': Option('i', 'about', self._menu.push),
            '\n': ''}, ['n', 'q', '\n', 's', 'h', 'i'],
            self._parse_menu)
        self._pages['settings'] = Page('Settings', '', {
            'r': Option('r', 'restore defaults', self._restore_defaults),
            't': Option('t', 'types', self._menu.push),
            'l': Option('l', 'length', self._menu.push),
            'a': Option('a', 'attempts', self._menu.push),
            'b': Option('b', 'back', self._menu.back),
            's': Option('s', 'change all settings', self._change_settings),
            '\n': ''}, ['r', '\n', 't', 'l', 'a', '\n', 'b'],
            self._parse_settings)
        self._menu.push(self._pages['menu'])
        self.__game = None

    #--------------------------------------------------------------------------


    # -----Public methods-----

    def main(self):
        """The main loop of the game."""
        while True:
            self._menu()

    def new_game(self):
        """Play the game with the current settings."""
        del self._game
        self._game = Game(self._settings)
        option = self._game.main()

    def continue_game(self):
        """Continue the current game."""
        option = self._game.main()

    # -----Private properties-----

    @property
    def _menu(self):
        return self.__menu

    @property
    def _options(self):
        """The options dictionary."""
        return self.__options.copy()

    @property
    def _game(self):
        """A game instance."""

        # Defensive programming
        try:
            assert self._game is not None, AttributeError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        return self.__game

    @property
    def _defaults(self):
        """The default settings."""
        return self.__defaults

    @property
    def _settings(self):
        """The game's current settings."""
        return self.__settings


    # -----Private property prescriptors-----

    @_game.setter
    def _game(self, game):
        """Assumes game is a Game object.

        Modify the game property."""

        # Polymorphic defensive programming
        try:
            assert hasattr(game, 'main'), TypeError
            assert callable(game.main), AttributeError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__game = game

    @_game.deleter
    def _game(self):
        self.__game = None


    @_settings.setter
    def _settings(self, settings):
        """Assumes settings is a settings object.

        Modify the current settings."""

        # Polymorphic defensive programming
        try:
            assert False, NotImplementedError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__settings = settings

    @_options.setter
    def _options(self, options):
        """Assumes options is a dictionary where each value is an opti-
        on and each key is the key for that option."""
        self.__options = options


    # -----Private methods-----

    def _parse_menu(self, data):
        args, kwargs = (), {}
        if data == 's':
            args = [self._pages['settings']]
        elif data == 'h':
            args = [self._pages['help']]
        elif data == 'i':
            args = [self._pages['about']]
        elif data not in self._pages['menu'].order:
            raise ParseError
        return data, args, kwargs

    def _parse_settings(self, data):
        args, kwargs = (), {}
        if data == 't':
            args = [self._pages['types']]
        elif data == 'l':
            args = [self._pages['length']]
        elif data == 'a':
            args = [self._pages['attempts']]
        elif len(data) > 1:
            data, args = 's', [data]
        elif data not in self._pages['settings'].order:
            raise ParseError
        return data, args, kwargs

    def _restore_defaults(self):
        self._settings = self._defaults

    def _change_settings(self, data):
        # Helper variables
        maximums = {'t': 30, 'l': 20, 'a': 100}
        pattern = re.compile(r'[tla]\W*\d+')

        # Main algorithm
        settings = {}
        for setting in re.findall(pattern, data):
            key = settings[0]
            settings[key] = int(re.findall(r'\d+', setting))
            if settings[key] > maximums[key]:
                raise ValueError
        settings = Settings(types=settings['t'],
            length=settings['l'], attempts=settings['a'])
        self._settings = settings

if __name__ == '__main__':
    guesscii = Guesscii()
    guesscii.main()
