import string, subprocess, random
from gamedata import Data, EXACT, SIMILAR
from page import Page

# Global aliases
EXACT_CHAR, SIMILAR_CHAR = EXACT, SIMILAR

# Modified the Docstrings to fit standards
class Game(object):
    """The main class that runs an actual game."""

    def __init__(self, settings, options, order):
        """Assumes settings is a settings dictionary;
        Options is a dictionary of options;
        Order is sequence of characters that represents the option order."""

        options = options.copy()
        options['/g'] = lambda x: x

        self.__settings = settings
        self.__answer = self._build_answer()
        self._order = order
        self._data = Data(settings)
        self._page = Page('', self._data.__str__(),
                           options, order, self._parse)


    #-----Public methods-----

    def main(self):
        """Run an actual game.
        Yield an option object.

        Yields:
            An option object that's either chosen by the user entering menu commands or because the game ended. The option is essential for the game's main loop to run as intended.

        Side Effects:
            Meant to modify the hints, guesses and answer properties of
                the data property.
            Meant modify the body property of the page property.

        Raises:
            An exception if the guess entered by the user is invalid.
        """
        for i in xrange(self._settings.attempts):
            guess = self._page()
            if not guess and type(guess) is not str:
                yield
            self._data.add_guess(guess, i)

            hint = self._build_hint(guess)
            self._data.add_hint(hint, i)

            self._page.body = self._data.__str__()

        self._data.answer = self._answer
        self._page.body = self._data.__str__()
        subprocess.call('cls', shell=True)
        print self._page.body


    #-----Private properties-----

    # Immutable
    @property
    def _settings(self):
        """The settings used to create the game."""
        return self.__settings

    @property
    def _answer(self):
        """The answer combination."""
        return self.__answer


    #-----Private methods-----

    def _build_answer(self):
        """Create a randomized answer combination."""
        answer = ''
        for i in xrange(self._settings.length):
            answer += random.choice(self._settings.types)
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
        if data in self._order:
            return data, (), {}
        else:
            return '/g', [self._data_to_guess(data)], {}

    def _data_to_guess(self, data):
        """Parse data into a combination string.

        Arguments:
            data ----- A string that can be parsed into a combination.
        """
        return data.replace(' ', '')


#------------------Testing--------------------


def test():
    from settings import Settings
    from option import Option

    settings = Settings(6, 4, 5)
    options = {'q': Option('q', 'quit', quit)}
    game = Game(settings, options, ['q'])
    for option in game.main():
        raw_input('> ')
        subprocess.call('cls', shell=True)
        quit()

if __name__ == '__main__':
    test()
