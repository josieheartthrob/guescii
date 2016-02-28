import string, subprocess

def main():
    num_letters = 3
    guess_len = 3

    combos = exhaust_combos(string.ascii_lowercase[:num_letters],
                          guess_len, "")

    t1 = CheatTable("aab", combos)
    print t1

class CheatTable(dict):
    """A hash table that organizes the different possible out-comes of a specified guess checked with specified answers."""

    def __init__(self, guess, answers):
        """Assumes guess is a combo string;
        answers is a combos string"""
        self.guess = guess
        self.answers = answers
        dict.__init__(self, self.__hash_guesses())

    def __hash_guesses(self):
        cheat_table = {}
        for answer in self.answers.split():
            check = check_guess(answer, self.guess)
            if check not in cheat_table:
                cheat_table[check] = [answer]
            else:
                cheat_table[check].append(answer)
        return cheat_table

    def __str__(self):
        s = self.guess + "\n"
        for check in self:
            s += "\n" + check + ": " + self[check][0]
            for combo in self[check][1:]:
                s += ", " + combo
        return s

def exhaust_combos(letters, length, combos="", combo=""):
    for c in letters:
        if length == 1:
            combos += (combo + c + " ")
        else:
            combos = exhaust_combos(letters, length-1,
                                    combos, combo + c)
            combos += "\n"
    return combos

def check_guess(guess, answer):
    check = ""
    answer = list(answer)
    for i in xrange(len(guess)):
        if guess[i] == answer[i]:
            check = "x"+check
            answer[i] = ""
        elif guess[i] in answer:
            check += "o"
            answer[answer.index(guess[i])] = ""
    return check

if __name__ == '__main__':
    main()
