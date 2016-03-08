class Game(object):
    """The main class that runs the actual game."""

    def __init__(self, settings):
        """Assumes settings is a settings dictionary."""
        self.settings = settings
        self.answer = self.build_answer()

    def build_answer(self):
        """Creates a randomized string of letters based off the settings."""

        answer = ""
        for i in xrange(self.settings["Combination Length"]):
            answer += self.settings["Guess Types"].choice()
        return answer

    def ask_for_guess(self):
        """Ask the user for their guess and wait for their input. If the input is invalid, ask again until it's valid"""

        guess = raw_input("> ")

    def __create_base_strings(self, settings):
        """Assumes settings is a settings dictionary"""
        if type(settings) != dict:
            raise TypeError
        settings_keys = ("Guess-Types", "Combination Length", "Guesses")
        if settings_keys not in settings.keys():
            raise ValueError

        base_strings = []
        base_strings.append(settings["Guess-Types"].replace("", " ")[1:-1])

        for i in xrange(settings["Guesses"]):
            base_strings.append(
                ("_"*settings["Combination Length"]).replace("", " "[1:-1]))

        return base_strings

    def __normalize_strings(self, strings):
        """Assumes strings is a list of string objects;

        Each string in strings is part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Returns a list of strings that are all the same size."""
        if type(strings) not in (list, tuple):
            raise TypeError
        try:
            for string in strings:
                assert type(string) == str
        except:
            raise ValueError

        longest_string = ""
        for string in strings:
            if len(string) > len(longest_string):
                longest_string = string

        normalized_strings = []
        for string in strings:
            normalized_strings.append(__buffer_string(string))
        return normalized_strings

    def __buffer_string(self, string_to_modify, length):
        """Assumes string_to_modify is a string;
        length is a positive integer;

        string_to_modify is a part of the representation of the game. (This method only produces the desired results for the representation of the game).

        Returns a copy of the given string with a buffer on both ends."""
        if type(string_to_modify) != str or type(length) != int:
            raise TypeError
        if length < len(string_to_modify):
            raise ValueError

        total_buffer_space = length - len(string_to_modify)
        buffer_space = total_buffer_space // 2

        string_to_modify = (
            string_to_modify[:-1] +
            " "*buffer_space +
            string_to_modify[-1])

        if total_buffer_space % 2 != 0:
            buffer_space += 1

        if string_to_modify[0] in (">", "["):
            string_to_modify = (
                string_to_modify[0] +
                " "*buffer_space +
                string_to_modify[1:])
        else:
            string_to_modify = (
                " "*(buffer_space+1) +
                string_to_modify)

        return string_to_modify
