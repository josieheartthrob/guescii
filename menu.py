import subprocess

class Menu(object):
    """Determine when the user wants to quit"""

    # Static variables
    _option_names = {
        "n": "new game",
        "s": "settings",
        "q": "quit"}
    default_settings = {
        "Guess Types": 6,
        "Guess Length:" 4,
        "Guesses": 6}

    invalid_option = "You entered an invalid option.\n" \
                      "Please choose between [{0}]\n"

    # Class methods
    def __init__(self, parent):
        """Assumes parent is a guess object"""
        self.parent = parent
        self.options = {
        "n": parent.play_game,
        "s": change_the_settings,
        "q": quit_the_program}

        self.__option_names = Menu._option_names.copy()


    # Public Properties

    @property
    def options():
        """A dictionary of callable option-functions where each key is a string"""
        return self.__options

    @options.setter
    def options(self, key_pair):
        """Assumes key_pair is an indexed data structure;
        key_pair[0] is an immutable object;
        key_pair[1] is a function;

        Creates a key_pair[0] key in the options dictionary with the value key_pair[1]"""
        self.__options[key_pair[0]] = key_pair[1]

    @options.deleter
    def options(self, key):
        """Assumes key is a key in the options dictionary.
        Deletes the key from the options dictionary."""
        del self.__options[key]


    @property
    def option_names():
        """A dictionary of option-name strings where each key is a string"""
        return self.__option_names

    @options.setter
    def option_name(self, key_pair):
        """Assumes key_pair is an indexed data structure;
        key_pair[0] is an immutable object;
        key_pair[1] is a function;

        Creates a key_pair[0] key in the option names dictionary with the value key_pair[1]"""
        self.__option_names[key_pair[0]] = key_pair[1]

    @options.deleter
    def option_names(self, key):
        """Assumes key is a key in the option names dictionary.
        Deletes the key from the option names dictionary."""
        del self.__option_names[key]


    # Public Methods

    def get_option(self):
        """Displays the menu to the screen and waits for the user to input a valid option.

        Returns the user's option"""

        # Display the menu
        print self
        option = raw_input("> ")

        while option not in self.options:
            # Clear the screen
            subprocess.call("cls", shell=True)

            # Display the invalid option Menu
            print self
            print Menu._invalid_option
            option = raw_input("> ")

        return option


    # Private Mehtods

    def __str__(self):
        menu_str = ""
        for option in self.option_names.keys():
            menu_str += "{0} - {1}\n".format(option, self.option_names[option])
        return menu_str
