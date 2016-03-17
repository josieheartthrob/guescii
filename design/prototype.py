import string, subprocess, random, time

def main():
    guess = ""
    while guess != "/q":
        answer = build_answer()
        game_strings = ["\n[ a b c d e f ]\n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "    _ _ _ _   |   \n\n",
                        "_______________\n\n",
                        "    _ _ _ _\n\n",
                        "> /n - new game\n",
                        "> /q - quit game\n\n"]

        for attempt in xrange(10):
            guess = get_guess(game_strings)
            hint = get_hint(guess, answer)
            write_guess(game_strings, guess, hint)
            replace_placeholder(game_strings)
            if guess in (answer, "/q", "/n"):
                break
        reveal(game_strings, answer)
        raw_input("> ")

def reveal(game_strings, answer):
    subprocess.call("cls", shell=True)
    game_strings[-3] = "    "+answer+ "\n\n"
    print_strings(game_strings)

def build_answer():
    letters = [letter for letter in string.lowercase[:6]]
    answer = ""
    for i in xrange(4):
        answer += " " + random.choice(letters)
    return answer[1:]

def get_hint(guess, answer):
    am = {L: answer.count(L) for L in set(answer.split())}
    gm = {L: guess.count(L) for L in set(guess.split())}
    similar = sum([min(am[L], gm[L]) for L in am if L in gm])
    exact = sum(
        [1 for i in xrange(len(guess.split())) if guess[2*i] == answer[2*i]])
    similar -= exact
    return "x"*exact + "o"*similar

def get_guess(game_strings):
    subprocess.call("cls", shell=True)
    print_strings(game_strings)
    guess = raw_input("> ")
    return guess

def write_guess(game_strings, guess, hint):
    i = find_index(game_strings)
    game_strings[i] = "    " + guess + "   |   " + hint + "\n\n"

def replace_placeholder(game_strings):
    i = find_index(game_strings)
    game_strings[i] = ">" + game_strings[i][1:]

def find_index(game_strings):
    for i in xrange(len(game_strings)):
        if game_strings[i].find("_") > 0:
            return i

def print_strings(game_strings):
    for string in game_strings:
        print string,

if __name__ == '__main__':
    main()
