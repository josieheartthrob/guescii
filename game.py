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
