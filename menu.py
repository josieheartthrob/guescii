import subprocess

class Menu(object):
    """Determine when the user wants to quit"""

    # Static variables
    default_settings = {
        "Types": 6,
        "Length:" 4,
        "Attempts": 10}

    _options = {
        "n": Option("n", "new game"),
        "s": Option("s", "settings"),
        "q": Option("q", "quit")}

    invalid_option = "You entered an invalid option.\n" \
                      "Please choose between [{0}]\n"

    # Class methods
    def __init__(self, parent):
        """Assumes parent is a guess object"""
        self.parent = parent
        self.__options = Menu._options.copy()
        self.__options["n"].function

    # Public Properties

    @property
    def options():
        """A dictionary of callable option-functions where each key is a string"""
        return self.__options.copy()

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
        self.__options[option.key] = option

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
        print self
        option = raw_input("> ")

        while option not in self.options.keys():
            # Clear the screen
            subprocess.call("cls", shell=True)

            # Display the Invalid Option Menu
            print self
            print Menu._invalid_option.format(self.options.keys())
            option = raw_input("> ")

        return option


    # Private Mehtods

    def __str__(self):
        s = "[Menu]\n\n"
        for option in self.options:
            s += option.__str__() + "\n"
        return s



class Option(object):
    """An option to display on the menu."""

    def __init__(self, key, name):
        """Assumes key and name are strings;
        function is a callable object.

        Create an Option object"""

        # Polymorphic defensive programming
        try:
            assert type(key), type(name) == str, TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Initialize attributes
        self.__function = None
        self.key = key
        self.name = name

    @property
    def function(self):
        """The function to call for the option."""

        # Polymorphic defensive programming
        try:
            assert type(self.__function) != None, AttributeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        return self.__function

    @function.setter
    def function(self, f):
        """Assumes f is a callable object.

        Set the function property to f."""

        # Polymorphic defensive programming
        try:
            assert callable(f), TypeError

        except AssertionError, exception:
            raise exception.args[0]

        # Main algorithm
        self.__function = f

    def __str__(self):
        return "> {0.key} - {0.name}".format(self)

    def __call__(self):
        self.__function()
