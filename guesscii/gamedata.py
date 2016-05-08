import string, re

# Global variables
EXACT = 'x'
SIMILAR = 'o'

class Data(object):
    """A class that contains all the information to repreent the game. Printing an instance of the class will print the game."""

    #-----Public properties-----

    # Mutable
    @property
    def answer(self):
        return self._answer


    #-----Public methods-----

    def add_guess(self, guess):
        """Add a guess to the list of guesses.

        Arguments:
            guess ----- string; combination

        Side Effects:
            Modifies the private guesses property by replacing the next
            placeholder with the specified guess.
        """
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
        self._add_item('_hints', hint, lambda s: len(s) == 0)


    #-----Constructor method-----

    def __init__(self, settings):
        """Assumes settings is a settings dictionary.

        Create a GameRep with the given arguments."""
        # Helper variables
        placeholder = (" _"*settings.length)[1:]

        # Initialize attributes
        self.__settings = settings
        self.__placeholders = self._build_placeholders()
        self.__guesses = [placeholder for attempt in
                          xrange(settings.attempts)]
        self.__hints = ['' for attempt in xrange(settings.attempts)]
        self._answer = placeholder


#-----------------------------------------------------------------------------


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

    def _build_placeholders(self):
        """Create a dictionary of guess and hint placeholders."""
        # This method makes use of the string-formatting mini-language

        # Helper variables
        types = len(self._settings.types)
        length = self._settings.length

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm

        # Aligns the amount of specified spaces on either side
        header = self._build_placeholder(['types: ^{}'], space)
        placeholders = {'header': header}

        guess_strings = ('guess: >{}', 'seperator: ^{}', 'hint')
        guesses = [self._build_placeholder(guess_strings, space) for
                   attempt in xrange(self._settings.attempts)]
        placeholders['guesses'] = guesses

        placeholders['seperator'] = "_"*full + '\n\n'

        answer = 'answer: >{}'
        placeholders['answer'] = self._build_placeholder([answer], space)

        return placeholders

    def _build_placeholder(self, strings, space):
        """Assumes string is a string;
        length is a positive integer;

        string is a part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Return a copy of the given string with a buffer on both ends.
        """
        types = len(self._settings.types)
        s = ''
        for string in strings:
            if string.find('>') >= 0:
                space_0 = (self._settings.length*2) + space - 1
                space_1 = space - 1
                s += '{' + string.format(space_0, space_1) + '}'
            else:
                space_0 = (types*2) + space - 1
                s += '{' + string.format(space_0) + '}'
        return s

    def _find_placeholder(self, strings, is_placeholder):
        """Assumes strings is a list of strings;
        is_placeholder is a  function that takes a  string as input and
        returns a boolean value;

        Return  an integer as the index in  strings where a placeholder
        first occurs."""

        for i, s in enumerate(strings):
            if is_placeholder(s):
                return i
        raise IndexError

    def _add_item(self, attribute, item, function):
        """Assumes attribute is a representation attribute;
        item is an object with the relevant typing;
        function is a filter function for the _find_placeholder method;

        add an item to the specified attribute."""

        replica = getattr(self, attribute)
        i = self._find_placeholder(replica, function)
        replica[i] = item
        exec 'self.{} = replica'.format(attribute)


#-----------------------------------------------------------------------------


    #-----Public property prescriptors-----

    @answer.setter
    def answer(self, answer):
        self._check_combo(answer)
        answer = answer.replace(' ', '')
        answer = answer.replace('', ' ')[1:-1]
        self._answer = answer


    #-----Private property prescriptors-----

    @_guesses.setter
    def _guesses(self, guesses):
        guesses = list(guesses[:])
        for i, guess in enumerate(guesses):
            self._check_combo(guess)
            guesses[i] = guess.replace(' ', '')
            guesses[i] = guess.replace('', ' ')[1:-1]
        self.__guesses = guesses

    @_hints.setter
    def _hints(self, hints):
        hints = list(hints[:])
        for i, hint in enumerate(hints):
            self._check_hint(hint)
            hints[i] = hint
        self.__hints = hints


    #-----Magic methods-----

    def __str__(self):
        s = ''
        for i, string in enumerate(self._placeholders['guesses']):
            s += string.format(guess=self._guesses[i], seperator='|',
                               hint=self._hints[i])+'\n\n'
        s += self._placeholders['seperator']+'\n'
        s += self._placeholders['answer'].format(answer=self._answer)+'\n\n'
        return s


    #-----Error checking methods-----

    def _check_combo(self, combo):
        if type(combo) is not str:
            raise TypeError('{} must be a combination string.'.format(combo))
        combo = combo.replace(' ', '')
        if len(combo) != self._settings.length:
            raise ValueError(
                '{} must be exactly '.format(combo) +
                '{} characters long.'.format(self._settings.length))
        for c in set(combo):
            if c not in self._settings.types+'_':
                raise ValueError(
                    '{} must be composed of ['.format(combo) +
                    '{}]'.format(self._settings.types.replace('', ' ')[1:-1]))

    def _check_hint(self, hint):
        for c in set(hint):
            if c not in (EXACT, SIMILAR):
                raise ValueError(
                    '{} must be composed of ['.format(hint) +
                    '{}, {}]'.format(EXACT, SIMILAR))
        if len(hint) > self._settings.length:
            raise ValueError(
                '{} must be <= '.format(hint) +
                '{} character long.'.format(self._settings.length))


#-----------------------------------------------------------------------------


def test():
    import subprocess
    from settings import Settings

    def clear():
        raw_input('> ')
        subprocess.call('cls', shell=True)

    def print_guesses(data):
        for guess in data._guesses:
            print guess
        clear()

    def print_hints(data):
        for hint in data._hints:
            print hint
        clear()

    data = Data(Settings())
    print data
    clear()

    print_guesses(data)

    data.add_guess('aabb')
    print_guesses(data)

    print data
    clear()

    data.add_hint('xxxx')
    print_hints(data)
    print_guesses(data)

    print data
    clear()

    data.answer = 'aabb'
    print data
    clear()

if __name__ == '__main__':
    test()
