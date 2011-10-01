import sys

class BoggleSolver:
    def __init__(self, letter_list):
        self.dictionary = Dictionary("C:\\My Dropbox\\Programming Projects\\Python\\PyBoggle\\dictionary.txt")
        self.board = Board(letter_list)
        self.min_length = 3
        self.found_words = set()

        # Find all words starting from each coordinate position
        for row in xrange(self.board.side_length):
            for column in xrange(self.board.side_length):
                self._find_words(Word.new(row, column), row, column)

    def _find_words(self, word, row, column):
        word.add_letter(self.board[row][column], row, column)

        if (self._can_add_word(word)):
            self.found_words.add(word.letter_sequence)

        for row, column in self._get_valid_coodinates_for_word(word, row, column):
            if(self.dictionary.contains_prefix(word.letter_sequence + self.board[row][column])):
                self._find_words(Word.new_from_word(word), row, column)

    def _can_add_word(self, word):
        return len(word) >= self.min_length and self.dictionary.contains_word(word.letter_sequence)

    def _get_valid_coodinates_for_word(self, word, row, column):
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if r >= 0 and r < self.board.side_length and c >= 0 and c < self.board.side_length:
                    if ((r, c) not in word.used_board_coordinates):
                        yield r, c

class Board:
    def __init__(self, letter_list):
        self.side_length = len(letter_list) ** .5
        if (self.side_length != int(self.side_length)):
            raise Exception("Board must have equal sides! (4x4, 5x5...)")
        else:
            self.side_length = int(self.side_length)

        self.board = []

        index = 0
        for row in xrange(self.side_length):
            self.board.append([])
            for column in xrange(self.side_length):
                self.board[row].append(letter_list[index])
                index += 1

    def __getitem__(self, row):
        return self.board[row]

class Word:
    def __init__(self):
        self.letter_sequence = ""
        self.used_board_coordinates = set()

    @classmethod
    def new(cls, row, column):
        word = cls()
        word.used_board_coordinates.add((row, column))
        return word

    @classmethod
    def new_from_word(cls, word):
        new_word = cls()
        new_word.letter_sequence += word.letter_sequence
        new_word.used_board_coordinates.update(word.used_board_coordinates)
        return new_word

    def add_letter(self, letter, row, column):
        self.letter_sequence += letter
        self.used_board_coordinates.add((row, column))

    def __str__(self):
        return self.letter_sequence

    def __len__(self):
        return len(self.letter_sequence)

class Dictionary:
    def __init__(self, dictionary_file):
        self.words = set()
        self.prefixes = set()
        word_file = open(dictionary_file, "r")

        for word in word_file.readlines():
            self.words.add(word.strip())
            for index in xrange(len(word.strip()) + 1):
                self.prefixes.add(word[:index])

    def contains_word(self, word):
        return word in self.words

    def contains_prefix(self, prefix):
        return prefix in self.prefixes

if __name__ == "__main__":
    boggleSolver = BoggleSolver(sys.argv[1:])
    words = boggleSolver.found_words 
    print words
