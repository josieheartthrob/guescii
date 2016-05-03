import string, re, typing
check = typing.check

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


    #-----Public property prescriptors-----

    @answer.setter
    def answer(self, answer):
        # Defensive programming
        check([{'function': typing.combo,
                'args': (answer, self._settings)}])

        # Main algorithm
        self._answer = answer.replace('', ' ')[1:-1]


    #-----Private property prescriptors-----

    @_guesses.setter
    def _guesses(self, guesses):
        # Polymorphic defensive programming
        checks = [{'function': typing.method,
                   'args': (guesses, '__getitem__,', TypeError)}]
        guess_checks = [{'function': typing.combo,
                         'args': (guess, self._settings)} for
                        guess in guesses]
        checks.extend(guess_checks)
        check(checks)

        # Main algorithm
        self.__guesses = guesses

    @_hints.setter
    def _hints(self, hints):
        # Polymorphic defensive programming
        check([{'function': typing.hints,
                'args': (hints, (EXACT, SIMILAR), self._settings.length)}])

        # Main algorithm
        self.__hints = hints

    #--------------------------------------------------------------------------



    #-----Public methods-----

    def add_guess(self, guess):
        """Add a guess to the list of guesses.

        Arguments:
            guess ----- string; combination

        Side Effects:
            Modifies the private guesses property by replacing the next
            placeholder with the specified guess.
        """
        # Defensive programming
        check([{'funcion': typing.combo,
                'args': (guess, self._settings)}])

        # Main algorithm
        self._add_item('_guesses', guess, lambda s: s.find("_") >= 0)

    def add_hint(self, hint):
        """Add a hint to the list of hints.

        Arguments:
            hint ----- a string less than or equal to the combination length.
                         It's only composed of the EXACT and SIMILAR global
                         variables.

        Side Effects:
            Modifies the private hints property by replacing the next
            placeholder with the specified hint.
        """
        # Defensive programming
        check([{'function': typing.hint,
                'args': (hint, (EXACT, SIMILAR), self._settings.length)}])

        # Main algorithm
        self._add_item('_hints', hint, lambda s: len(s) == 0)


    #-----Private methods-----

    def _build_placeholders(self):
        """Create a dictionary of guess and hint placeholders."""
        # This method makes use of the string-formatting mini-language

        # Helper variables
        types = self._settings.types
        length = self._settings.length

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm

        # Aligns the amount of specified spaces on either side
        header = self._buffer_string(['types: ^{}'], space)
        placeholders = {'header': header}

        guess_strings = ('guess: >{}', 'seperator: ^{}', 'hint')
        guesses = [self._buffer_string(guess_strings, space) for
                   attempt in xrange(self._settings.attempts)]
        placeholders['guesses'] = guesses

        placeholders['seperator'] = "_"*full + '\n\n'

        answer = 'answer: >{}'
        placeholders['answer'] = self._buffer_string([answer], space)

        return placeholders

    def _build_placeholder(self, strings, space):
        """Assumes string is a string;
        length is a positive integer;

        string is a part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Return a copy of the given string with a buffer on both ends.
        """
        # Defensive programming
        checks = [{'function': typing.method,
                   'args': (string, '__iter__', TypeError)}]
        type_checks = [{'function': typing.obj_type,
                        'args': (s, str, TypeError)} for s in strings]
        checks.extend(type_checks)
        check(checks)

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

    def _find_placeholder(self, strings, is_placeholder):
        """Assumes strings is a list of strings;
        is_placeholder is a  function that takes a  string as input and
        returns a boolean value;

        Return  an integer as the index in  strings where a placeholder
        first occurs."""

        # Polymorphic defensive programming
        checks = [{'function': typing.method,
                  'args': (strings, attribute, TypeError)} for
                 attribute in ('__iter__', '__getitem__')]
        type_checks = [{'function': typing.obj_type,
                        'args': (s, str, TypeError)} for s in strings}]
        checks.extend(type_checks)
        callable_check = {'function': typing.callable,
                          'args': (is_placeholder, TypeError)}
        checks.append(callable_check)
        check(checks)

        # Main algorithm
        for i, s in enumerate(strings):
            if is_placeholder(s):
                return i
        raise IndexError

    def _add_item(self, attribute, item, function):
        """Assumes attribute is a representation attribute;
        item is an object with the relevant typing;
        function is a filter function for the _find_placeholder method;

        add an item to the specified attribute."""

        # Defensive programming
        checks = [{'function': typing.obj_type,
                   'args': (attribute, str, TypeError)},
                  {'function': typing.attribute,
                   'args': (self, attribute, AttributeError)}]
        method_checks = [{'function': typing.method,
                          'args': (getattr(self, attribute),
                                   method, TypeError)
                         } for method in ('__getitem__', '__setitem__')]
        checks.extend(method_checks)
        callable_check = {'function': typing.callable,
                          'args': (fucntion, TypeError)}
        checks.append(callable_check)
        check(checks)

        # Main algorithm
        replica = getattr(self, attribute)
        i = self._find_placeholder(replica, function)
        replica[i] = item
        exec 'self.{} = replica'.format(attribute)


    #-----Magic methods-----

    def __init__(self, settings):
        """Assumes settings is a settings dictionary.

        Create a GameRep with the given arguments."""
        # Defensive programming
        check([{'function': typing.settings, 'args': [settings]}])

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
