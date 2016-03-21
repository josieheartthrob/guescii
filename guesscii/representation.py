import string

# Global variables
EXACT = 'x'
SIMILAR = 'o'

class GameRep(object):
    """A class that contains all the information to repreent the game. Printing an instance of the class will print the game."""

    #-----Public methods-----

    @property
    def add_guess(self):
        """Assumes guess is a string

        guess is as  long as the combination  length and  only contains
        letters from the combination letter pool.

        Modify the private guesses property of the reprentation"""
        return self.__add_guess

    @property
    def add_hint(self):
        """Assumes hint is a string

        hint is less than or equal to the combination length and is on-
        ly composed of the EXACT and SIMILAR global variables

        Replace the next placeholder with an actual game hint."""
        return self.__add_hint

    @property
    def reveal_answer(self):
        """Not implemented."""
        return self.__reveal_answer


    #-----Private methods-----

    @property
    def __build_placeholders(self):
        """Assumes settings is a settings dictionary."""
        return self.___build_placeholders

    @property
    def __buffer_string(self):
        """Assumes string is a string;
        length is a positive integer;

        string is a part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Return a copy of the given string with a buffer on both ends."""
        return self.___buffer_string

    @property
    def __find_placeholder(self):
        """Assumes strings is a list of strings;
        is_placeholder is a  function that takes a  string as input and
        returns a boolean value;

        Return  an integer as the index in  strings where a placeholder
        first occurs."""
        return self.___find_placeholder


    #-----Private properties-----

    # Immutable
    @property
    def __settings(self):
        """The game's settings."""
        return self.___settings

    @property
    def __types(self):
        """The letters the combination chooses from."""
        return self.___types

    @property
    def __placeholders(self):
        """A list of placeholder strings."""
        return self.___placeholders.copy()

    @property
    def __header(self):
        """The header of the game."""
        return self.___header

    # Mutable
    @property
    def __guesses(self):
        """A list of guesses the user has made."""
        return self.___guesses[:]

    @property
    def __hints(self):
        """A list of hints displayed to the user."""
        return self.___hints[:]

    @property
    def __answer(self):
        """A placeholder for the answer."""
        return self.___answer

    #--------------------------------------------------------------------------


    #-----Public method prescriptors-----

    def __add_guess(self, guess):
        # Defensive programming
        try:
            assert type(guess) == str, TypeError
            assert len(guess) == self.__settings.length, ValueError
            for c in set(guess):
                assert c != " ", ValueError
                assert c in self.__header, ValueError

        except AssertionError as e:
            raise e.args[0]

        # Helper variables
        guesses = self.__guesses

        # Main algorithm
        i = self.__find_placeholder(guesses, lambda s: s.find("_") >= 0)
        guesses[i] = guess.replace("", " ")[1:-1]
        self.__guesses = guesses

    def __add_hint(self, hint):
        # Defensive programming
        try:
            for attribute in ("__str__", "__getitem__"):
                assert hasattr(hint, attribute), TypeError
                assert callable(getattr(hint, attribute)), AttributeError
            assert len(hint) <= self.__settings.length, ValueError
            for c in set(hint):
                assert c in "{}{}".format(EXACT, SIMILAR), ValueError

        except AssertionError as e:
            raise e.args[0]

        # Helper variables
        hints = self.__hints

        # Main algorithm
        i = self.__find_placeholder(hints, lambda s: len(s) == 0)
        hints[i] = hint
        self.__hints = hints

    def __reveal_answer(self, answer):
        # Defensive programming
        try:
            assert type(answer) == str, TypeError
            assert len(answer) == (self.__settings.length*2) - 1, ValueError
            for c in answer.split():
                assert c in self.__types, TypeError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.__answer = answer


    #-----Private property prescriptors-----

    @__guesses.setter
    def __guesses(self, guesses):
        # Polymorphic defensive programming
        try:
            assert hasattr(guesses, "__getitem__"), TypeError
            assert callable(guesses.__getitem__), AttributeError
            for guess in guesses:
                assert type(guess) == str, TypeError
                for c in set(guess):
                    assert c in self.__types + "_ ", ValueError
                assert len(guess) == (self.__settings.length*2) -1, ValueError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.___guesses = guesses

    @__hints.setter
    def __hints(self, hints):
        # Polymorphic defensive programming
        try:
            assert hasattr(hints, "__getitem__"), TypeError
            assert callable(hints.__getitem__), AttributeError
            for hint in hints:
                assert hasattr(hint, "__getitem__"), TypeError
                assert callable(hint.__getitem__), AttributeError
                for c in set(hint):
                    assert type(c) == str
                    assert c in (EXACT, SIMILAR), ValueError
                assert len(hint) <= self.__settings.length, ValueError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.___hints = hints


    #-----Private method prescriptors-----

    def ___build_placeholders(self):
        # Helper variables
        types = self.__settings.types
        length = self.__settings.length

        # Derived Helper variables
        base = (max(types, length)*2) - 1
        space = abs(types-length) + 2
        full = base + space + 1

        # Main algorithm
        placeholders = {'header': self.__buffer_string(('types: ^{}',), space)}

        guesses = [self.__buffer_string(('guess: >{}', 'seperator: ^{}',
                                         'hint'), space) for
                   attempt in xrange(self.__settings.attempts)]
        placeholders['guesses'] = guesses

        placeholders['seperator'] = "_"*full + '\n\n'
        placeholders['answer'] = self.__buffer_string(("answer: >{}",), space)

        return placeholders

    def ___buffer_string(self, strings, space):
        # Defensive programming
        try:
            assert hasattr(strings, '__iter__'), TypeError
            assert callable(strings.__iter__), AttributeError
            for s in strings:
                assert type(s) == str, TypeError
            assert type(space) == int, TypeError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        s = ''
        for string in strings:
            if string.find('>') >= 0:
                space_0 = (self.__settings.length*2) + space - 1
                space_1 = space + 1
                s += '{' + string.format(space_0, space_1) + '}'
            else:
                space_0 = (self.__settings.types*2) + space - 1
                s += '{' + string.format(space_0) + '}'

        return s

    def ___find_placeholder(self, strings, is_placeholder):
        # Polymorphic defensive programming
        try:
            for attribute in ("__iter__", "__getitem__"):
                assert hasattr(strings, attribute), TypeError
                assert callable(getattr(strings, attribute)), AttributeError
            for string in strings:
                assert hasattr(string, "__str__"), TypeError
                assert callable(string.__str__), AttributeError
            assert callable(is_placeholder), TypeError

        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        for i, s in enumerate(strings):
            if is_placeholder(s):
                return i
        raise IndexError


    #-----Magic methods-----

    def __init__(self, settings):
        """Assumes settings is a settings dictionary.

        Create a GameRep with the given arguments."""

        # Polymorphic defensive programming
        try:
            for attribute in ('types', 'length', 'attempts'):

                # Helper variables
                attribute_type = type(getattr(settings, attribute))

                # Run checks
                assert hasattr(settings, attribute), TypeError
                assert attribute_type == int, AttributeError

        except AssertionError as e:
            raise e.args[0]

        # Helper variables
        placeholder = (" _"*settings.length)[1:]

        # Initialize attributes
        self.___settings = settings
        self.___types = string.lowercase[:settings.types]
        self.___placeholders = self.__build_placeholders()
        self.___header = "".join([" "+c for c in self.__types])[1:]
        self.___guesses = [placeholder for attempt in
                           xrange(settings.attempts)]
        self.___hints = ["" for attempt in xrange(settings.attempts)]
        self.___answer = placeholder

    def __str__(self):
        s = '[{}]'.format(self.__placeholders[
                          'header'].format(types=self.__header))+'\n\n'
        for i, string in enumerate(self.__placeholders['guesses']):
            s += string.format(guess=self.__guesses[i], seperator='|',
                               hint=self.__hints[i])+'\n\n'
        s += self.__placeholders['seperator']+'\n\n'
        s += self.__placeholders['answer'].format(answer=self.__answer)+'\n\n'
        return s
