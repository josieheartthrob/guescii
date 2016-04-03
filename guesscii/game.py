import string, subprocess, random
from gamedata import Data, EXACT, SIMILAR
from typing import *

# Global aliases
EXACT_CHAR, SIMILAR_CHAR = EXACT, SIMILAR

class Game(object):
    """The main class that runs the actual game."""

    #-----Public methods-----

    @property
    def main(self):
        """Run the actual game.
        Yield an option object."""
        return self._main


    #-----Private properties-----

    # Immutable
    @property
    def _settings(self):
        """The settings object."""
        return self.__settings

    @property
    def _types(self):
        """A string of all the differenct characters the combination chooses from."""
        return self.__types

    @property
    def _answer(self):
        """The answer combination."""
        return self.__answer


    #-----Private methods-----

    @property
    def _build_answer(self):
        """Create a  randomized string of lower-case  letters based off
        the settings."""
        return self.__build_answer

    @property
    def _build_hint(self):
        """Return a string that gives the user info about their guess."""
        return self.__build_hint

    #--------------------------------------------------------------------------


    #-----Public method prescriptors-----

    def _main():
        for i in xrange(self._settings.attempts):
            guess = self._page(self._parse_user_input)
            self._data.add_guess(guess)

            hint = self._build_hint(guess)
            self._data.add_hint(hint)

            if guess == self._answer:
                self._data.answer = self._answer
                yield self._page.options['n']
            elif guess in self._page.order:
                yield self._page.options[guess]

            self._page.body = self._data.__str__()


    #-----Private method prescriptors-----

    def __build_hint(self, guess):
        # Polymorphic defensive programming
        try:
            check_type(guess, str, TypeError)
            check_inside(guess, self._types, ValueError)
        except AssertionError as excpetion:
            raise exception.args[0]

        # Here's a funny thing: In Tatham's source code they reference a wolfr-
        # am alpha page that  has the formula for this. But I actually  figured
        # this out before  I even knew Tatham's code was  open-source - because
        # I'm a fucking math-genius.

        # Helper variables
        guess_map = {c: guess.count(c) for c in set(guess)}
        answer_map = {c: self._answer.count(c) for c in  set(self._answer)}

        # Main algorithm
        exact = sum([1 for i, c in enumerate(guess) if c == answer[i]])
        similar = (sum([min(guess_map[c], answer_map[c]) for
                        c in answer_map if c in guess_map]) - exact)
        return EXACT_CHAR*exact + SIMILAR_CHAR*similar

    def __build_answer(self):
        answer = ''
        for i in xrange(self._settings.length):
            answer += random.choice(self._types)
        return answer

    def __parse_user_input(self, data):
        # Defensive programming
        try:
            check_type(data, str, TypeError)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        key = self._guess_key
        if data in self._page.order:
            key, data = data, ()
        else:
            data = re.sub(' ', '', data)
            try:
                check_combo(data, self._settings)
            except AssertionError:
                key = None
        return key, (data,), {}



    #-----Magic methods-----

    def __init__(self, settings, options, order):
        """Assumes settings is a settings dictionary;
        Options is a dictionary of options;
        Order is sequence of characters that represents the option order."""

        # Polymorphic defensive programming
        try:
            check_settings(settings)
            check_options(options)
            check_order(order, options)
        except AssertionError as exeption:
            raise exception.args[0]

        # Initialize attributes
        self.__settings = settings
        self.__types = string.lowercase[:settings.types]
        self.__data = Data(settings)
        self.__page = Page(self._types, self._data.__str__(), options, order)
        self.__answer = self._build_answer()
