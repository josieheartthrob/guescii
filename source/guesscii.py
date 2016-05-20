import random, subprocess, re, string
from sys import exit
from shellpages import *
from source.game import Game

class Guesscii(object):
    """The main class that handles the program."""

    def __init__(self):
        # changed defaults for testing purposes
        self.__defaults = {'types': 3, 'length': 3, 'attempts': 9}
        self.__settings = self._defaults
        self.__stack = Stack()
        self._pages =  {
            'help': Page('Help', 'coming soon', {
                'b': Option('b', 'back', self._stack.back)}, ['b'],
                self._default_parse),
            'about': Page('About', 'coming soon', {
                'b': Option('b', 'back', self._stack.back)}, ['b'],
                self._default_parse),
            'types': Page('Change amount of letters to choose from', '', {
                    '/s': self._change_settings,
                    'c': Option('c', 'cancel', self._stack.back)},
                ['c'], self._parse_types),
            'length': Page('Change the length of the combination', '', {
                    '/s': self._change_settings,
                    'c': Option('c', 'cancel', self._stack.back)},
                ['c'], self._parse_length),
            'attempts': Page('Change the amount of attempts allowed', '', {
                    '/s': self._change_settings,
                    'c': Option('c', 'cancel', self._stack.back)},
                ['c'], self._parse_attempts)}
        # took away help and about pages for testing purposes
        self._pages['menu'] = Page('Menu', '', {
            'n': Option('n', 'new game', self._new_game),
            'q': Option('q', 'quit', close),
            's': Option('s', 'settings', self._stack.push),
            #'h': Option('h', 'help', self._stack.push),
            #'i': Option('i', 'about', self._stack.push),
            '\n': ''}, ['n', 'q', '\n', 's'],#, 'h', 'i'],
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
        for attribute in ('iteritems', 'keys'):
            if not hasattr(settings, attribute):
                raise TypeError('{} must be a dictionary.'.format(
                    type(settings)))
        if not {'types', 'length', 'attempts'}.issubset(set(settings.keys())):
            raise ValueError('{} must be a settings dictionary.'.format(
                settings))
        for value in settings.values():
            if type(value) is not int:
                raise ValueError('{} must be a settings dictionary.'.format(
                    settings))
        self.__settings = settings

    @_options.setter
    def _options(self, options):
        """Assumes options is a dictionary where each value is an opti-
        on and each key is the key for that option."""
        self.__options = options


    # -----Private methods-----

    def _parse_menu(self, data):
        args, kwargs = (), {}

        if data == 'c':
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
        return self._parse_setting('t', data)

    def _parse_length(self, data):
        return self._parse_setting('l', data)

    def _parse_attempts(self, data):
        return self._parse_setting('a', data)

    def _parse_setting(self, setting, data):
        # Helper Variables
        maximums = {'t': 30, 'l': 20, 'a': 100}

        t = self._settings['types']
        L = self._settings['length']
        a = self._settings['attempts']

        # Main algorithm
        args, kwargs = (), {}

        if data != 'c':
            try:
                data = int(data)
            except ValueError:
                raise ParseError('Please enter a positive integer.')
            if data > maximums[setting]:
                raise ParseError('{} must be less than {}'.format(
                    key, maximums[settings]))
            elif data < 2:
                raise ParseError('{} must be greater than 1'.format(key))

            if setting == 't':
                t = data
            elif setting == 'l':
                L = data
            elif setting == 'a':
                a = data

            data, args = '/s', ['t:{} l:{} a:{}'.format(t, L, a)]

        return data, args, kwargs

    def _change_settings(self, data):
        # Helper variables
        character_map = {'t': 'types', 'l': 'length', 'a': 'attempts'}
        pattern = re.compile(r'[tla]\W*\d+')

        # Main algorithm
        settings = {}
        for setting in re.findall(pattern, data):
            key = character_map[setting[0]]
            settings[key] = int(re.findall(r'\d+', setting)[0])

        self._settings = settings
        raw_input('Settings saved. \n\n> ')

    def _default_parse(self, data):
        if data != 'b':
            raise ParseError('Invalid input. Please enter an option.')
        return data, (), {}

    def _restore_defaults(self):
        self._settings = self._defaults

    def _new_game(self):
        if (self._stack[-1].title.replace(' ', '') ==
                string.lowercase[:self._settings['types']]):
            self._stack.back()
        del self._game
        self._game = Game(self._settings, {
            'n': Option('n', 'new game', self._new_game),
            'm': Option('m', 'menu', self._stack.back),
            'q': Option('q', 'quit', close)}, ['n', 'm', 'q'])
        self._stack.push(self._game.page)

def close():
    subprocess.call('cls', shell=True)
    exit()

if __name__ == '__main__':
    guesscii = Guesscii()
    guesscii.main()
