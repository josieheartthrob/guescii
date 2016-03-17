import subprocess
from option import Option

class Menu(object):
    """Determine when the user wants to quit"""

    # Static variables

    _options = {
        "n": Option("n", "new game"),
        "s": Option("s", "settings"),
        "q": Option("q", "quit")}

    # Class methods
    def __init__(self, parent):
        """Assumes parent is a guess object"""
        self.parent = parent
        self._options = Menu._options.copy()
        self._options["n"].function = parent.play_game
        self._options["s"].function = self.change_settings
        self._options["q"].function = quit
        self._order = ["n", "s", "q"]
        self._option_was_invalid = False

    # Public Methods

    def new_option(self, option):
        """Assumes option is an Option object.

        Add a new option to the options dictionary."""

        # Polymorphic defensive programming
        try:
            for attribute in ("key", "name", "function"):
                assert hasattr(option, attribute), TypeError
            assert callable(option), TypeError
            assert option.key not in ("n", "s", "q"), ValueError
            assert (option.name not in
                    ("new game", "settings", "quit")), ValueError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._options[option.key] = option

    def delete_option(self, option):
        """Assumes option is a string;
        option is in the options dictionary;

        option is the key for the option to be delted from the options dictionary.

        Delte the option from the options dictionary."""

        # Polymorphic defensive programming
        try:
            assert type(option) == str, TypeError
            assert option in self.options.keys(), KeyError
            assert option not in ("n", "s", "q"), ValueError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        del self.options[option]

    def get_choice(self):
        """Display the menu to the screen and wait for the user to enter a valid option.

        Return the user's chosen option."""

        # Display the menu
        subprocess.call("cls", shell=True)
        print self
        option = raw_input("> ")
        if option not in self.option.keys();
            self.option_was_invalid = True
            raise ValueError
        else:
            self.option_was_invalid = False
        return self.options[option]

    def change_settings(self):
        raise NotImplementedError

    # Public Properties

    @property
    def options():
        """A dictionary of callable option-functions where each key is a string."""
        return self._options.copy()

    @property
    def option_was_invalid(self):
        """Return True if the previous optioin entered was invalid."""
        return self._option_was_invalid

    @option_was_invalid.setter
    def option_was_invalid(self, value):
        """Assumes value is a boolean value.
        Set option_was_invalid to the given value."""

        # Defensive programming
        try:
            type(value) == bool, TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._option_was_invalid = value

    @property
    def order(self):
        """The order of options to display to the menu."""
        return self._order

    @order.setter
    def order(self, order):
        """Assumes order is a list of option keys where each relative option is in the menu options.

        Modify the order of options to display to the menu."""

        # Polymorphic defensive programming
        try:
            assert False, NotImplementedError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self._order = order

    # Private Mehtods

    def __str__(self):
        s = "[Menu]\n\n"
        for key in order:
            s += self.options[key].__str__() + "\n"
        if self.option_was_invalid:
            s += "\n" + Option.invalid_option.format(self.options.keys())
        return s
