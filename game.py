class Game(object):
    """The main class that runs the actual game."""

    def __init__(self, settings):
        """Assumes settings is a settings dictionary."""
        if type(settings) != dict:
            raise TypeError
        settings_keys = ("Guess-Types", "Combination Length", "Guesses")
        if settings_keys not in settings.keys():
            raise ValueError

        self.settings = settings
        self.answer = self.build_answer()
        self.answer_map = {L: self.answer.count(L) for L in set(self.answer)}

    def build_answer(self):
        """Creates a randomized string of letters based off the settings."""

        answer = ""
        for i in xrange(self.settings["Combination Length"]):
            answer += self.settings["Guess Types"].choice()
        return answer

    def compare_guess(self, guess):
        """Assumes guess is a string as long as the combination length.

        Return a string that gives the user info about their guess."""
        if type(guess) != str:
            raise TypeError
        try:
            for letter in set(guess):
                assert letter in self.settings["Guess-Types"]
            assert len(guess) == self.settings["Guess Length"]
        except:
            raise ValueError

        total_similar_letters = sum(self.answer_map.itervalues())
        correct_letters, similar_letters = (
            self.differentiate_letters(total_similar_letters))
        return self.parse_into_answer_info(correct_letters, similar_letters)

    def differentiate_letters(self, guess, similar_letters):
        """Assumes similar_letters is a positive integer;
        Guess is a string as long as the combination length

        Return the amount of similar letters and the ammount of correct letters in the guess."""
        try:
            assert type(guess) == str
            assert type(similar_letters) == int
        except:
            raise TypeError
        try:
            for letter in set(guess):
                assert letter in self.settings["Guess-Types"]
            assert len(guess) == self.settings["Guess Length"]
            assert similar_letters >= 0
        except:
            raise ValueError

        correct_letters = 0
        for i in xrange(len(guess)):
            if guess[i] == self.answer[i]:
                similar_letters -= 1
                correct_letters += 1
        return correct_letters, similar_letters
