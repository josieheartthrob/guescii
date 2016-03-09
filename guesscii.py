import random, test_guess, subprocess
from menu import Menu
from game import Game

class Guesscii(object):
    """The main class that handles the program"""

    def __init__(self):
        self.menu = Menu
        self._game = None

    @property
    def game(self):
        """A game instance"""
        return self._game

    @game.setter
    def game(self, game):
        """Assumes game is a game.Game object or None
        Modifies the game property"""
        if type(game) != Game:
            raise TypeError

        self._game = game

    def main(self):
        selected_option = self.menu.get_option()
        while selected_option != self.menu.options["q"]:
            self.menu.options[selected_option]()
            selected_option = self.menu.get_option()
        self.menu.options[selected_option]()

    def play_game(self):
        """Sets the game property to a new instance of the game class using the menu's current settings and calls the game's main method.
        Once the game is finished it clears the game property."""
        self.game = Game(self.menu.settings)
        subprocess.call("clear", shell=True)
        self.game.main()
        self.game = None

if __name__ == '__main__':
    guess = Guescii()
    guess.main()


DEFAULTS = {
    "GUESS TYPES": range(6), "COMBINATION LENGTH": 4, "GUESSES": 6}

PLAY_STATES = {
    "NEW GAME": "n", "CUSTOMIZE SETTINGS": "c", "QUIT": "q"}

ERRORS = {
    "INT": "Input incomaptible, please enter an integer\n"}

def main():
    # Set Defaults
    settings = get_defaults()

    # Main algorithm
    play_state = ask_to_play()
    while play_state != PLAY_STATES["QUIT"]:

        if play_state == PLAY_STATES["NEW GAME"]:
            play_game(settings)

        elif play_state == PLAY_STATES["CUSTOMIZE SETTINGS"]:
            settings = customize_settings()

        play_state = ask_to_play()

    quit()

def play_game(settings):
    """Assumes settings is a settings dictionary"""
    combination = make_random_sequence(
        settings["guess types"], settings["combination length"])
    guess = get_guess(settings["guess types"], settings["guesses"])
    while guess != combination:
        print check_guess(guess)
        guess = get_guess(settings["guess types"], settings["guesses"])
    print "You Win!"

def customize_settings():
    """returns a settings dictionary"""

    restore_defaults = raw_input("restore defaults? y | n\n\n> ")
    while restore_defaults not in ("y", "n"):
        restore_defaults = raw_input(
            "invalid input\nplease type \"y\" or \"n\":\n\n> ")

    if restore_defaults == "n":
        settings = {"guess types": 0, "combination length": 0, "guesses": 0}
        settings["guess types"] = ensure_int(
            "amount of guess types: ", sign="positive")
        settings["combination length"] = ensure_int(
            "length of each guess: ", sign="positive")
        settings["guesses"] = ensure_int(
            "amount of guesses: ", sign="positive")
    else:
        settings = get_defaults()
    return settings

def get_defaults():
    """Returns the default settings dictionary"""
    settings = {
        "guess types": DEFAULTS["GUESS TYPES"],
        "combination length": DEFAULTS["COMBINATION LENGTH"],
        "guesses": DEFAULTS["GUESSES"]}
    return settings

def ask_to_play():
    # Helper variable
    game_options = "{0}: {1} | {2}: {3} | {4}: {5}".format(
        "new game", PLAY_STATES["NEW GAME"],
        "customize settings", PLAY_STATES["CUSTOMIZE SETTINGS"],
        "quit", PLAY_STATES["QUIT"])

    # Main algorithm
    return raw_input(game_options)

def make_random_sequence(linear_sequence, random_sequence_length):
    """Assumes linear_sequence is a linearly iterable container of a
        linear sequence of integers;
    random_sequence_length is a positive integer;

    returns a list the length of random_sequence_length of
        randomized integers where each integer is in linear_sequence"""

    random_sequence = []
    for i in xrange(random_sequence_length):
        random_sequence.append(random.choice(linear_sequence))
    return random_sequence

def get_guess(guess_types, combination):
    """Assumes guess_types is a linear sequence of integers;
    combination is a randomized sequence of integers where each integer is
        in guess_types;

    repeatedly asks the user for a guess of what the combination is until
        the guess is compatible;
    returns the guess as a list of integers"""

    # Helper variable
    ask_again = "Guess is incompatible.\n" \
                "Please enter {0} numbers from {1},\n" \
                "Seperated by spaces: ".format(
                    len(combination), guess_types)

    # Main algorithm
    guess_str = raw_input("Enter your guess: ")
    while not guess_is_compatible(guess_str):
        geuss_str = raw_input(ask_again)
    return int_str_to_list(guess_str)

def guess_is_compatible(guess_types, combo_len, guess_str):
    """Assumes guess_types is a linear sequence of integers;
    combo_len is a positive integer;
    geuss_str is a string of integers

    returns a boolean value that represents wether or not guess_str is
        a compatible guess"""

    try:
        guess = int_str_to_list(guess_str)
        for i in xrange(combo_len):
            assert guess[i] in guess_types
    except:
        return False
    return True

def int_str_to_list(int_str):
    """Assumes int_str is a string of integers
    returns a list where each item is an integer from and in the
        same order as int_str"""
    int_list = []
    for num in int_str.split():
        int_list.append(int(num))
    return int_list

def ensure_int(message, error_msg=ERRORS["INT"], sign="ambiguous"):
    while True:
        try:
            value = get_int(message, sign)
            return value
        except:
            message = error_msg

def get_int(message, sign="ambiguous"):
        value = int(raw_input(message))
        if sign == "ambiguous":
            return value
        elif sign == "positive":
            return abs(value)
        elif sign == "negative":
            return -abs(value)
        else:
            raise ValueError


if __name__ == '__main__':
    main()
