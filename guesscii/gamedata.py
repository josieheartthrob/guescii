# Global variables
EXACT = 'x'
SIMILAR = 'o'

class Data(object):
    """A class that contains all the information to repreent the game. Printing an instance of the class will print the game."""

    def __init__(self, settings):
        """Create a Data object.

        Arguments:
            settings ------ A Settings object.

        Public properties:
            answer -------- A string as the answer combination.

              It' i's initialized as a placeholder but can be set to a
              combination string. It's intended use is to reveal the answer
              to the user once they've finished a game.

        Public methods:
            add_guess ----- Add a guess to the list of guesses.
            add_hint ------ Add a hint to the list of hints.
        """
        # Helper variables
        placeholder = (" _"*settings.length)[1:]

        # Initialize attributes
        self.__settings = settings
        self.__placeholders = self._build_placeholders()
        self._guesses = [placeholder for attempt in xrange(settings.attempts)]
        self._hints = ['' for attempt in xrange(settings.attempts)]
        self._answer = placeholder

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
        self._check_combo(guess)
        guess = guess.replace(' ', '')
        guess = guess.replace('', ' ')[1:-1]
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
        self._check_hint(hint)
        self._add_item('_hints', hint, lambda s: len(s) == 0)


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


    #-----Private methods-----

    def _build_placeholders(self):
        """Create a dictionary of guess and hint placeholders."""
        # This method makes heavy-ish use of the string-formatting
        #   mini-language

        # Helper variables
        types = len(self._settings.types)
        length = self._settings.length
        guess_strings = ('guess: >{}', 'seperator: ^{}', 'hint')

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm
        header = self._build_placeholder(['types: ^{}'], space)
        guesses = [self._build_placeholder(guess_strings, space) for
                   attempt in xrange(self._settings.attempts)]
        answer = self._build_placeholder(['answer: >{}'], space)

        placeholders = {'header': header, 'guesses': guesses,
                        'answer': answer, 'seperator': '_'*full+'\n\n'}
        return placeholders

    def _build_placeholder(self, strings, space):
        """Return a buffered placeholder string.

        Arguments:
            strings ----- A list of placeholder strings.
            space ------- An int as the amount of spaces to buffer with.
        """
        # Helper variables
        types = len(self._settings.types)

        # Main algorithm
        s = ''
        for placeholder_string in strings:
            if placeholder_string.find('>') >= 0:
                space_0 = (self._settings.length*2) + space - 1
                space_1 = space - 1
                s += '{' + placeholder_string.format(space_0, space_1) + '}'
            else:
                space_0 = (types*2) + space - 1
                s += '{' + placeholder_string.format(space_0) + '}'
        return s

    def _add_item(self, attribute, item, function):
        """Replace a placeholder in a placeholder list.

        Arguments:
            attribute ----- The placeholder list to modify.
            item ---------- The item to replace with.
            function ------ A funciton that determines which placeholder
                            should be replaced

        Side Effects:
            Modifies the specified attribute by replacing the placeholder
            found by th specified function with the specified item
        """
        replica = getattr(self, attribute)
        i = self._find_placeholder(replica, function)
        exec 'self.{}[i] = item'.format(attribute)

    def _find_placeholder(self, strings, is_placeholder):
        """Return an integer as the index of the first occuring placeholder.

        Arguments:
            strings ------------ A list of placeholders.
            is_placeholder ----- a function that determines wether or not
                                 a string is a placeholder. It takes a string
              as input and returns a bool.
        """

        for i, s in enumerate(strings):
            if is_placeholder(s):
                return i
        raise IndexError


#-----------------------------------------------------------------------------


    #-----Public property prescriptors-----

    @answer.setter
    def answer(self, answer):
        self._check_combo(answer)
        answer = answer.replace(' ', '')
        answer = answer.replace('', ' ')[1:-1]
        self._answer = answer


    #-----Magic methods-----

    def __str__(self):
        s = ''
        for i, placeholder_string in enumerate(self._placeholders['guesses']):
            s += placeholder_string.format(
                guess=self._guesses[i], seperator='|',
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
