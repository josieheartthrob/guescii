import string, subprocess, random
from source.gamedata import Data, EXACT, SIMILAR
from shellpages import Page, ParseError

# Global aliases
EXACT_CHAR, SIMILAR_CHAR = EXACT, SIMILAR

class Game(object):
    """The main class that runs an actual game."""

    def __init__(self, settings, options, order):
        """Assumes settings is a settings dictionary;
        Options is a dictionary of options;
        Order is sequence of characters that represents the option order."""

        options = options.copy()
        options['/g'] = self._guess

        self.__place = 0

        self._settings = settings.copy()
        self._answer = self._build_answer()
        self._data = Data(settings)

        self._page = Page(self._data.header, self._data.__str__(),
                          options, order, self._parse)


    #-----Public properties-----

    @property
    def page(self):
        return self._page


    #-----Private properties-----

    @property
    def _place(self):
        return self.__place

    @_place.setter
    def _place(self, other):
        if other-self.__place != 1:
            raise ValueError('place can only increment by 1')
        elif self.__place+1 == self._settings['attempts']:
            self._data.answer = self._answer
        self.__place = other


    #-----Private methods-----

    def _build_answer(self):
        """Create a randomized answer combination."""
        # Helper Variables
        types = string.lowercase[:self._settings['types']]

        # Main algorithm
        answer = ''
        for i in xrange(self._settings['length']):
            answer += random.choice(types)
        return answer

    def _build_hint(self, guess):
        """Return a string that gives the user info about their guess.

        Arguments:
            guess ----- a string entered by the user
        """

        # Here's a funny thing: In Tatham's source code they reference a
        # wolfram alpha page that has the formula for this. But I actually
        # figured this out before I even knew Tatham's code was open-source -
        # because I'm a fucking math-genius.

        # Helper variables
        guess_map = {c: guess.count(c) for c in set(guess)}
        answer_map = {c: self._answer.count(c) for c in  set(self._answer)}

        # Main algorithm
        exact = sum([1 for i, c in enumerate(guess) if c == self._answer[i]])
        similar = (sum([min(guess_map[c], answer_map[c]) for
                        c in answer_map if c in guess_map]) - exact)
        return EXACT_CHAR*exact + SIMILAR_CHAR*similar

    def _parse(self, data):
        """Parse data to call an option or evaluate a guess.

        Arguments:
            data ----- a string entered by the user
        """
        # Helper Variables
        types = string.lowercase[:self._settings['types']]
        guess = data.replace(' ', '')

        # Main algorithm
        if data in self._page.options.keys():
            return data, (), {}
        elif self._data.answer.replace(' ', '') == self._answer:
            raise ParseError('Game over. Please choose an option.')
        elif len(guess) != self._settings['length']:
            raise ParseError('Guess must be exactly ' +
                '{} letters long'.format(self._settings['length']))
        elif not set(guess).issubset(set(types)):
            raise ParseError('Guess must be composed of ' +
                '[{}]'.format(types.replace('', ' ')[1:-1]))
        else:
            return '/g', [guess], {}

    def _guess(self, combo):
        """Display accuracy of the given combination to the user.

        Arguments:
            combo ----- A combination string

        Side Effects:
            Modifies the private data property's answer, guesses,
            and hints properties.

            Modifies the private page property's body property.
        """
        self._data.add_guess(combo, self._place)

        hint = self._build_hint(combo)
        self._data.add_hint(hint, self._place)

        if combo == self._answer:
            self._data.answer = self._answer

        self._place += 1
        self._page.body = self._data.__str__()


#------------------Testing--------------------


def test():
    from shellpages import Option
    from sys import exit

    def close():
        raw_input('> ')
        subprocess.call('cls', shell=True)
        exit()

    settings = {'types': 6, 'length': 4, 'attempts': 5}
    options = {'q': Option('q', 'quit', close)}
    game = Game(settings, options, ['q'])
    while True:
        game._page()

if __name__ == '__main__':
    test()
