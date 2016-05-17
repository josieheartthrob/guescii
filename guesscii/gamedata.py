from string import lowercase

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
        placeholder = (" _"*settings['length'])[1:]
        letters = lowercase[:settings['types']]

        # Initialize attributes
        self.__settings = settings
        self.__placeholders = self._build_placeholders()
        self._guesses = [placeholder for attempt in xrange(
            settings['attempts'])]
        self._hints = ['' for attempt in xrange(settings['attempts'])]
        self._answer = placeholder
        self._header = self._placeholders['header'].format(
            types=letters.replace('', ' ')[1:-1])

    #-----Public properties-----

    # Mutable
    @property
    def answer(self):
        return self._answer

    @property
    def header(self):
        return self._header


    #-----Public methods-----

    def add_guess(self, guess, i):
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
        self._guesses[i] = guess

    def add_hint(self, hint, i):
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
        self._hints[i] = hint


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
        types = self._settings['types']
        length = self._settings['length']
        guess_strings = ('guess: >{}', 'seperator: >{}', 'hint: >{}')

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm
        header = self._build_placeholder(['types: ^{}'], space)
        guesses = [self._build_placeholder(guess_strings, space) for
                   attempt in xrange(self._settings['attempts'])]
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
        types = self._settings['types']

        # Main algorithm
        s = ''
        for placeholder in strings:
            if placeholder.find('types') >= 0:
                space = (types*2)-1 + space
            elif (placeholder.find('guess') >= 0 or
                    placeholder.find('answer') >= 0):
                space = (self._settings['length']*2)-1 + space
            elif placeholder.find('seperator') >= 0:
                space = 6
            elif placeholder.find('hint') >= 0:
                space = self._settings['length']+2
            elif placeholder.find('answer') >=  0:
                space = space
            else:
                raise KeyError("{} isn't a key".format(placeholder))
            s += '{'+placeholder.format(space)+'}'
        return s


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
        types = lowercase[:self._settings['types']]
        if type(combo) is not str:
            raise TypeError('{} must be a combination string.'.format(combo))
        combo = combo.replace(' ', '')
        if len(combo) != self._settings['length']:
            raise ValueError(
                '{} must be exactly '.format(combo) +
                '{} characters long.'.format(self._settings['length']))
        for c in set(combo):
            if c not in types+'_':
                raise ValueError(
                    '{} must be composed of ['.format(combo) +
                    '{}]'.format(types.replace('', ' ')[1:-1]))

    def _check_hint(self, hint):
        for c in set(hint):
            if c not in (EXACT, SIMILAR):
                raise ValueError(
                    '{} must be composed of ['.format(hint) +
                    '{}, {}]'.format(EXACT, SIMILAR))
        if len(hint) > self._settings['length']:
            raise ValueError(
                '{} must be <= '.format(hint) +
                '{} character long.'.format(self._settings['length']))


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

    data.add_guess('aabb', 0)
    print_guesses(data)

    print data
    clear()

    data.add_hint('xxxx', 0)
    print_hints(data)
    print_guesses(data)

    print data
    clear()

    data.answer = 'aabb'
    print data
    clear()

if __name__ == '__main__':
    test()
