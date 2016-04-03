import string, re
from typing import *

# Global variables
EXACT = 'x'
SIMILAR = 'o'

class Data(object):
    """A class that contains all the information to repreent the game. Printing an instance of the class will print the game."""

    #-----Public properties-----

    # Mutable
    @property
    def answer(self):
        """A placeholder for the answer."""
        return self._answer


    #-----Public methods-----

    @property
    def add_guess(self):
        """Assumes guess is a string

        guess is as  long as the combination  length and  only contains
        letters from the combination letter pool.

        Modify the private guesses property of the reprentation"""
        return self._add_guess

    @property
    def add_hint(self):
        """Assumes hint is a string

        hint is less than or equal to the combination length and is on-
        ly composed of the EXACT and SIMILAR global variables

        Replace the next placeholder with an actual game hint."""
        return self._add_hint


    #-----Private properties-----

    # Immutable
    @property
    def _settings(self):
        """The game's settings."""
        return self.__settings

    @property
    def _placeholders(self):
        """A list of placeholder strings."""
        return self.__placeholders.copy()

    # Mutable
    @property
    def _guesses(self):
        """A list of guesses the user has made."""
        return self.__guesses[:]

    @property
    def _hints(self):
        """A list of hints displayed to the user."""
        return self.__hints[:]


    #-----Private methods-----

    @property
    def _build_placeholders(self):
        """Assumes settings is a settings dictionary."""
        return self.__build_placeholders

    @property
    def _buffer_string(self):
        """Assumes string is a string;
        length is a positive integer;

        string is a part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Return a copy of the given string with a buffer on both ends."""
        return self.__buffer_string

    @property
    def _find_placeholder(self):
        """Assumes strings is a list of strings;
        is_placeholder is a  function that takes a  string as input and
        returns a boolean value;

        Return  an integer as the index in  strings where a placeholder
        first occurs."""
        return self.__find_placeholder

    @property
    def _add_item(self):
        """Assumes attribute is a representation attribute;
        item is an object with the relevant typing;
        function is a filter function for the _find_placeholder method;

        add an item to the specified attribute."""
        return self.__add_item

    #--------------------------------------------------------------------------


    #-----Public property prescriptors-----

    @answer.setter
    def answer(self, answer):
        # Defensive programming
        try:
            check_combo(answer, self._settings)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._answer = answer.replace('', ' ')[1:-1]


    #-----Public method prescriptors-----

    def _add_guess(self, guess):
        # Defensive programming
        try:
            check_combo(guess, self._settings)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._add_item('_guesses', guess, lambda s: s.find("_") >= 0)

    def _add_hint(self, hint):
        # Defensive programming
        try:
            check_hint(hint, (EXACT, SIMILAR), self._settings.length)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._add_item('_hints', hint, lambda s: len(s) == 0)


    #-----Private property prescriptors-----

    @_guesses.setter
    def _guesses(self, guesses):
        # Polymorphic defensive programming
        try:
            check_method(guesses, '__getitem__', TypeError)
            for guess in guesses:
                check_combo(guess, self._settings)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__guesses = guesses

    @_hints.setter
    def _hints(self, hints):
        # Polymorphic defensive programming
        try:
            check_hints(hints, (EXACT, SIMILAR), self._settings.length)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__hints = hints


    #-----Private method prescriptors-----

    def __build_placeholders(self):
        # Helper variables
        types = self._settings.types
        length = self._settings.length

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm
        placeholders = {'header': self._buffer_string(('types: ^{}',), space)}

        guesses = [self._buffer_string(('guess: >{}', 'seperator: ^{}',
                                         'hint'), space) for
                   attempt in xrange(self._settings.attempts)]
        placeholders['guesses'] = guesses

        placeholders['seperator'] = "_"*full + '\n\n'
        placeholders['answer'] = self._buffer_string(("answer: >{}",), space)

        return placeholders

    def __buffer_string(self, strings, space):
        # Polymorphic defensive programming
        try:
            check_method(string, '__iter__', TypeError)
            for s in strings:
                check_type(s, str, TypeError)
            check_type(space, int, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        s = ''
        for string in strings:
            if string.find('>') >= 0:
                space_0 = (self._settings.length*2) + space - 1
                space_1 = space - 1
                s += '{' + string.format(space_0, space_1) + '}'
            else:
                space_0 = (self._settings.types*2) + space - 1
                s += '{' + string.format(space_0) + '}'

        return s

    def __find_placeholder(self, strings, is_placeholder):
        # Polymorphic defensive programming
        try:
            for attribute in ('__iter__', '__getitem__'):
                check_method(strings, attribute, TypeError)
            for string in strings:
                check_type(string, str, TypeError)
            check_callable(is_placeholder, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        for i, s in enumerate(strings):
            if is_placeholder(s):
                return i
        raise IndexError

    def __add_item(self, attribute, item, function):
        # Defensive programming
        try:
            check_type(attribute, str, TypeError)
            check_attribute(self, attribute, AttributeError)
            for method in ('__getitem__', '__setitem__'):
                check_method(getattr(self, attribute), method, TypeError)
            check_callable(function, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        replica = getattr(self, attribute)
        i = self._find_placeholder(replica, function)
        replica[i] = item
        exec 'self.{} = replica'.format(attribute)


    #-----Magic methods-----

    def __init__(self, settings):
        """Assumes settings is a settings dictionary.

        Create a GameRep with the given arguments."""

        # Polymorphic defensive programming
        try:
            check_settings(settings)
        except AssertionError as e:
            raise e.args[0]

        # Helper variables
        placeholder = (" _"*settings.length)[1:]

        # Initialize attributes
        self.__settings = settings
        self.__placeholders = self._build_placeholders()
        self.__guesses = [placeholder for attempt in
                          xrange(settings.attempts)]
        self.__hints = ['' for attempt in xrange(settings.attempts)]
        self._answer = placeholder

    def __str__(self):
        for i, string in enumerate(self._placeholders['guesses']):
            s += string.format(guess=self._guesses[i], seperator='|',
                               hint=self._hints[i])+'\n\n'
        s += self._placeholders['seperator']+'\n'
        s += self._placeholders['answer'].format(answer=self._answer)+'\n\n'
        return s


# header = ''.join([' '+c for c in letters])[1:]
