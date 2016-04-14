import string, subprocess, random
from gamedata import Data, EXACT, SIMILAR
from typing import *

# Global aliases
EXACT_CHAR, SIMILAR_CHAR = EXACT, SIMILAR

class Game(object):
    """The main class that runs the actual game."""

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


    #-----Public methods-----

    def main(self):
        """Run the actual game.
        Yield an option object."""
        for i in xrange(self._settings.attempts):
            guess = self._page()

            if guess == self._answer:
                self._data.answer = self._answer
                yield self._page.options['n']
            elif guess in self._page.order:
                yield self._page.options[guess]

            try:
                check_combo(guess, self._settings)
            except AssertionError as e:
                raise e.args[0]

            self._data.add_guess(guess)

            hint = self._build_hint(guess)
            self._data.add_hint(hint)

            self._page.body = self._data.__str__()


    #-----Private methods-----

    def _build_answer(self):
        """Create a  randomized string of lower-case  letters based off
        the settings."""
        answer = ''
        for i in xrange(self._settings.length):
            answer += random.choice(self._types)
        return answer

    def _build_hint(self, guess):
        """Assumes guess is a combo string;
        Return a string that gives the user info about their guess."""
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

        def _parse_user_input(self, data):
            """Assumes data is a string.
            Parse data to call an option or evaluate a guess."""

            # Defensive programming
            try:
                check_type(data, str, TypeError)
            except AssertionError as e:
                raise e.args[0]

            # Main algorithm
            if data in self._page.order:
                return data, (), {}
            else:
                return self._data_to_guess(data), (), {}

        def _data_to_guess(self, data):
            """Assumes data is  a string.
            Create a new combo string based off data.
            Raise an exception if it can't be translated."""

            # Integrated defensive programming and main algorithm
            guess = re.sub(' ', '', data)
            try:
                check_combo(data, self._settings)
                return guess
            except AssertionError as e:
                raise e.args[0]


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
        self.__page = Page(self._types, self._data.__str__(), options,
                           order, self._parse_user_input)
        self.__answer = self._build_answer()
