from pathlib import Path
import re
import string

from scrabblesolver.board import Board
from scrabblesolver.letter_scores import letter_scores

_generation_point_re = re.compile(
    r"([ ])"
    r"(?=[^ ]+)|([^ ])"
    r"[^ ]*"
    r"([ ])"
)

_package_dir = Path(__file__).parent


def get_dictionary():
    with (_package_dir / "dictionary.txt").open() as dictionary_file:
        return set([
            line.strip().upper()
            for line in dictionary_file
            if line.strip()
        ])


def generation_points(s):
    for m in _generation_point_re.finditer(s):
        left_insertion_index = m.start(1)
        right_insertion_index = m.start(3)
        word_start_index = m.start(0)

        if left_insertion_index >= 0:
            yield left_insertion_index, left_insertion_index
        else:
            yield right_insertion_index, word_start_index


def generate_words_at_index(partial, tiles, index, word_start, **kwargs):
    parent_move = kwargs.pop("parent_move", [])

    seen = kwargs.pop("seen", set())

    while index < len(partial) and partial[index] != ' ':
        index += 1

    if not tiles or index >= len(partial):
        return

    for tile_index in range(len(tiles)):
        if tiles[tile_index] == '_':
            for letter in string.ascii_uppercase:
                new_tiles = tiles[:tile_index] + letter + tiles[tile_index+1:]

                for child_move in generate_words_at_index(
                    partial, new_tiles, index, word_start,
                    parent_move=parent_move, seen=seen
                ):
                    yield child_move
            continue

        new_partial = partial[:index] + tiles[tile_index] + partial[index+1:]
        if new_partial in seen:
            continue
        seen.add(new_partial)

        new_tiles = tiles[:tile_index] + tiles[tile_index+1:]
        move = parent_move + [(index, tiles[tile_index])]

        word_end = index
        while word_end < len(new_partial) and new_partial[word_end] != ' ':
            word_end += 1
        word = new_partial[word_start:word_end]

        yield move, word, word_start, word_end

        for child_move in generate_words_at_index(
            new_partial,
            new_tiles,
            index,
            word_start,
            parent_move=move,
            seen=seen
        ):
            yield child_move


def generate_words_in_partial_string(partial, tiles):
    for insertion_index, word_start in generation_points(partial):
        for move in generate_words_at_index(partial, tiles, insertion_index, word_start):
            yield move


def generate_moves(board, tiles, **kwargs):
    dictionary = kwargs.pop("dictionary", get_dictionary())

    rows = list(board.row_strs())
    for m in range(len(rows)):
        for move, word, n, word_end in generate_words_in_partial_string(rows[m], tiles):
            if word in dictionary:
                yield [(word[i], m, n+i) for i in range(len(word))]

    cols = list(board.column_strs())
    for n in range(len(cols)):
        for move, word, m, word_end in generate_words_in_partial_string(cols[n], tiles):
            if word in dictionary:
                yield [(word[i], m+i, n) for i in range(len(word))]


def score_move(board, move):
    score = 0
    score_multiplier = 1

    for letter, m, n in move:
        letter_score = letter_scores[letter]

        if board[m, n] == 'dl':
            letter_score *= 2
        elif board[m, n] == 'tl':
            letter_score *= 3
        elif board[m, n] == 'dw':
            score_multiplier *= 2
        elif board[m, n] == 'tw':
            score_multiplier *= 3

        score += letter_score

    score *= score_multiplier
    return score


def make_test_board_1():
    board = Board()
    board.add_word_v("spews", 3, 7)
    board.add_word_h("liars", 7, 3)
    board.add_word_v("raids", 7, 6)
    board.add_word_h("sober", 11, 6)
    board.add_word_v("qi", 6, 4)
    return board, "UAOSJIZ"


def make_test_board_2():
    board = Board()
    board.add_word_h("toward", 7, 3)
    board.add_word_v("pore", 5, 7)
    board.add_word_v("luna", 4, 6)
    board.add_word_v("eh", 4, 5)
    board.add_word_v("thunk", 7, 3)
    return board, "RYOATDE"


def main():
    board, tiles = make_test_board_2()
    print(str(board))
    print("Tiles: " + ", ".join(tiles))
    print("...")

    moves = []
    best_score = 0
    best_moves = []

    for move in generate_moves(board, tiles):
        score = score_move(board, move)
        word = "".join(symbol for symbol, m, n in move)
        moves.append((word, score, move))

        if best_score < score:
            best_score = score
            best_moves = []
        if best_score == score:
            best_moves.append((word, score, move))

    sorted_moves = sorted(moves, key=lambda m: m[1])

    for word, score, move in sorted_moves:
        print("\n---")
        print("WORD:  {0}".format(word))
        print("SCORE: {0}".format(score))

        new_board = Board(board)
        new_board.add_tiles(*move)
        print(new_board)


if __name__ == "__main__":
    main()
