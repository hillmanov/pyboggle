import os
import sys

side_length = None

class BoggleSolver:
    def __init__(self, letter_list, min_word_length):
        self.board = Board(letter_list)
        global side_length
        side_length = self.board.side_length

        self.dictionary = Dictionary('dictionary.txt')
        self.min_length = int(min_word_length)
        self.found_words = set()

        # Find all words starting from each coordinate position
        for row in xrange(self.board.side_length):
            for column in xrange(self.board.side_length):
                self._find_words(Word.new(row, column), row, column)

    def _find_words(self, word, row, column):
        word.add_letter(self.board[row][column], row, column)
        if (self._can_add_word(word)):
            self.found_words.add(word)

        for row, column in self._get_valid_coodinates_for_word(word, row, column):
            if(self.dictionary.contains_prefix(word.letters + self.board[row][column])):
                self._find_words(Word.new_from_word(word), row, column)

    def _can_add_word(self, word):
        return len(word) >= self.min_length and self.dictionary.contains_word(word.letters)

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
        self.letters = ""
        self.used_board_coordinates = []

    @classmethod
    def new(cls, row, column):
        word = cls()
        word.used_board_coordinates.append((row, column))
        return word

    @classmethod
    def new_from_word(cls, word):
        new_word = cls()
        new_word.letters += word.letters
        new_word.used_board_coordinates.extend(word.used_board_coordinates)
        return new_word

    def add_letter(self, letter, row, column):
        self.letters += letter
        if (row, column) not in self.used_board_coordinates:
            self.used_board_coordinates.append((row, column))

    def get_used_coord_numbers(self):
        return map(lambda (x, y) : str(side_length * x + y), [coordinate for coordinate in self.used_board_coordinates])

    def __hash__(self):
        return self.letters.__hash__()

    def __cmp__(self, other):
        if self.letters > other.letters:
            return 1
        elif self.letters == other.letters:
            return 0
        else:
            return - 1

    def __eq__(self, other):
        return self.letters == other.letters

    def __len__(self):
        return len(self.letters)
        
    def __str__(self):
        return "Word: {} Path: {}".format(self.letters, self.get_used_coord_numbers())
    
class Dictionary:
    def __init__(self, dictionary_file):
        self.words = set()
        self.prefixes = set()
        word_file = open(dictionary_file, "r")

        for word in word_file.readlines():
            word = word.lower()
            self.words.add(word.strip())
            for index in xrange(len(word.strip()) + 1):
                self.prefixes.add(word[:index])

    def contains_word(self, word):
        return word in self.words

    def contains_prefix(self, prefix):
        return prefix in self.prefixes



if __name__ == "__main__":
    print sys.argv[1:-1]
    print sys.argv[-1]
    boggleSolver = BoggleSolver(sys.argv[1:-1], sys.argv[-1])
    words = list(boggleSolver.found_words)
    words.sort()
    for word in words:
        print word
    
