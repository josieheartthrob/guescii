class GameRepresentation(object):
    """A class that contains all the information to repreent the game. Printing an instance of the class will print the game."""

    def __init__(self, settings):
        """Assumes settings is a settings dictionary.

        Creates a GameRepresentation with the given arguments."""
        self.settings = settings

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
                (" {}"*settings["Combination Length"])[1:]])

        return base_strings

    def __normalize_strings(self, strings, longest):
        """Assumes strings is a list of string objects;
        longest is an integer.

        Each string in strings is part of the representation of the game. (This method only produces the desired results for the representation of the game).
        longest is the index of the longest string in strings

        Returns a list of strings that are all the same size."""
        if type(strings) not in (list, tuple):
            raise TypeError
        try:
            for string in strings:
                assert type(string) == str
            assert type(longest) == int
        except:
            raise ValueError

        normalized_strings = []
        for string in strings:
            if len(string) < len(strings[longest]):
                normalized_strings.append(self.__buffer_string(
                    string, len(strings[longest])))
        return normalized_strings

    def __find_longest_string(self, strings):
        """Assumes strings is a list of string objects;

        Return the longest of the strings in the list."""
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
        return longest_string

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
