def main():
    for i in get_combo_list("abcdef"):
        print i,

def get_combo_list(guess_types):
    combo_list = []
    for i in guess_types:
        first_letter = []
        for j in guess_types:
            for k in guess_types:
                for L in guess_types:
                    first_letter.append(j+k+L)
        combo_list.append(first_letter)
    return combo_list

if __name__ == '__main__':
    main()
