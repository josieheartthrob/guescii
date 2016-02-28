import Guess

def __main():
    test_make_random_sequence()

def test_make_random_sequence():
    random_sequence_lengths = (4, 6, 3, 10)
    linear_sequences = (range(6), range(8), range(7), range(4))

    for i in xrange(len(random_sequence_lengths)):
        randomized_sequence = Guess.make_random_sequence(
            linear_sequences[i], random_sequence_lengths[i])
        assert len(randomized_sequence) == random_sequence_lengths[i]
        for num in randomized_sequence:
            assert type(num) == int
            assert num in linear_sequences[i]

if __name__ == '__main__':
    __main()
