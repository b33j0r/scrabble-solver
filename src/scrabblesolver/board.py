class Board(object):

    _default_layout_str = """
         .  .  . tw  .  . tl  . tl  .  . tw  .  .  .
         .  . dl  .  . dw  .  .  . dw  .  . dl  .  .
         . dl  .  . dl  .  .  .  .  . dl  .  . dl  .
        tw  .  . tl  .  .  . dw  .  .  . tl  .  . tw
         .  . dl  .  .  . dl  . dl  .  .  . dl  .  .
         . dw  .  .  . tl  .  .  . tl  .  .  . dw  .
        tl  .  .  . dl  .  .  .  .  . dl  .  .  . tl
         .  .  . dw  .  .  . st  .  .  . dw  .  .  .
        tl  .  .  . dl  .  .  .  .  . dl  .  .  . tl
         . dw  .  .  . tl  .  .  . tl  .  .  . dw  .
         .  . dl  .  .  . dl  . dl  .  .  . dl  .  .
        tw  .  . tl  .  .  . dw  .  .  . tl  .  . tw
         . dl  .  . dl  .  .  .  .  . dl  .  . dl  .
         .  . dl  .  . dw  .  .  . dw  .  . dl  .  .
         .  .  . tw  .  . tl  . tl  .  . tw  .  .  .
    """

    _alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _special_tiles = ['.', 'st', 'dl', 'dw', 'tl', 'tw']

    @classmethod
    def str_to_layout(cls, board_str):
        def validate_tile(tile):
            if tile.lower() in cls._special_tiles:
                return tile.lower()
            elif tile.upper() in cls._alphabet:
                return tile.upper()
            raise Exception()
        return [[validate_tile(tile) for tile in line.strip().split()]
                                     for line in board_str.strip().split('\n')]

    def __init__(self, *args):
        try:
            self._layout = Board.str_to_layout(str(args[0]))
        except Exception:
            self._layout = Board.str_to_layout(self._default_layout_str)
        self._tiles = []
        self._dimensions = (len(self._layout), len(self._layout[0]))

    def __getitem__(self, tile_mn):
        m0, n0 = tile_mn
        for symbol, m, n in self._tiles:
            if m == m0 and n == n0:
                return symbol
        return self._layout[m0][n0]

    def get_symbol(self, m0, n0):
        for symbol, m, n in self._tiles:
            if m == m0 and n == n0:
                return symbol
        return " "

    def __str__(self):
        M, N = self._dimensions
        fmt = "{:>3}"
        return "\n".join(
            "".join(fmt.format(self[m, n]) for n in range(N))
            for m in range(M)
        ).replace('dl', ' .').replace('dw', ' .').replace('tl', ' .').replace('tw', ' .')

    def add_tile(self, *args):
        def validate_tile(tile):
            if tile.upper() in self._alphabet:
                return tile.upper()
            raise Exception()
        symbol, m, n = args
        self._tiles.append((validate_tile(symbol), m, n))

    def add_tiles(self, *args):
        for tile in args:
            self.add_tile(*tile)

    def add_word_h(self, word, m, n):
        for i in range(len(word)):
            self.add_tile(word[i], m, n+i)

    def add_word_v(self, word, m, n):
        for i in range(len(word)):
            self.add_tile(word[i], m+i, n)

    def row_strs(self):
        M, N = self._dimensions
        for m in range(M):
            yield "".join(self.get_symbol(m, n) for n in range(N))

    def column_strs(self):
        M, N = self._dimensions
        for n in range(N):
            yield "".join(self.get_symbol(m, n) for m in range(M))
