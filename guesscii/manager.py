import random, subprocess, re
from shellpages import *
from game import Game
from settings import Settings

class Guesscii(object):
    """The main class that handles the program."""

    def __init__(self):
        self.__defaults = Settings()
        self.__settings = self._defaults
        self.__stack = Stack()
        self._pages =  {
            'help': Page('Help', 'coming soon', {
                'b': Option('b', 'back', self._stack.back)}, ['b']),
            'about': Page('About', 'coming soon', {
                'b': Option('b', 'back', self._stack.back)}, ['b']),
            'types': Page('Change amount of letters to choose from', '', {
                'c': Option('c', 'cancel', self._stack.back)}, ['c']),
            'length': Page('Change the length of the combination', '', {
                'c': Option('c', 'cancel', self._stack.back)}, ['c']),
            'attempts': Page('Change the amount of attempts allowed', '', {
                'c': Option('c', 'cancel', self._stack.back)}, ['c'])}
        self._pages['menu'] = Page('Menu', '', {
            'n': Option('n', 'new game', self._stack.push),
            'q': Option('q', 'quit', quit),
            's': Option('s', 'settings', self._stack.push),
            'h': Option('h', 'help', self._stack.push),
            'i': Option('i', 'about', self._stack.push),
            '\n': ''}, ['n', 'q', '\n', 's', 'h', 'i'],
            self._parse_menu)
        self._pages['settings'] = Page('Settings', '', {
            'r': Option('r', 'restore defaults', self._restore_defaults),
            't': Option('t', 'types', self._stack.push),
            'l': Option('l', 'length', self._stack.push),
            'a': Option('a', 'attempts', self._stack.push),
            'b': Option('b', 'back', self._stack.back),
            's': Option('s', 'change all settings', self._change_settings),
            '\n': ''}, ['r', '\n', 't', 'l', 'a', '\n', 'b'],
            self._parse_settings)
        self._stack.push(self._pages['menu'])
        self.__game = None

    #--------------------------------------------------------------------------


    # -----Public methods-----

    def main(self):
        """The main loop of the game."""
        while True:
            self._stack()

    def continue_game(self):
        """Continue the current game."""
        option = self._game.main()

    # -----Private properties-----

    @property
    def _stack(self):
        return self.__stack

    @property
    def _options(self):
        """The options dictionary."""
        return self.__options.copy()

    @property
    def _game(self):
        """A game instance."""

        # Defensive programming
        if not self.__game:
            raise ValueError('There is currently no game')

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

        # Defensive programming
        if not hasattr(game, 'page'):
            raise TypeError('The game must have a page property.')
        elif not callable(game.page):
            raise AttributeError("The game's page property must be" +
                                 " a callable object")

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
        if data == 'n':
            del self._game
            self._game = Game(self._settings, {
                'm': Option('m', 'menu', self._stack.back),
                'q': Option('q', 'quit', quit)},
            ['m', 'q'])
            args = [self._game.page]
        elif data == 'c':
            args = [self._game.page]
        elif data == 's':
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

    def _parse_types(self, data):
        self._parse_setting('t', data)

    def _parse_length(self, data):
        self._parse_setting('l', data)

    def _parse_attempts(self, data):
        self._parse_setting('a', data)

    def _parse_setting(self, setting, data):
        t = len(self._settings.types)
        L = self._settings.length
        a = self._settings.attempts
        args, kwargs = (), {}
        if data != 'c':
            try:
                data = int(data)
            except ValueError:
                raise ParseError('Please enter a positive integer.')
        if setting == 't':
        elif setting == 'l':
        elif setting == 'a':

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
