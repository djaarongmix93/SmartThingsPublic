import curses
import random
import time

# Tetris pieces: rotation states represented as lists of strings
TETROMINOS = {
    'I': [
        ['1111'],
        ['1','1','1','1']
    ],
    'O': [
        ['11',
         '11']
    ],
    'T': [
        ['010',
         '111'],
        ['10',
         '11',
         '10'],
        ['111',
         '010'],
        ['01',
         '11',
         '01']
    ],
    'S': [
        ['011',
         '110'],
        ['10',
         '11',
         '01']
    ],
    'Z': [
        ['110',
         '011'],
        ['01',
         '11',
         '10']
    ],
    'J': [
        ['100',
         '111'],
        ['11',
         '10',
         '10'],
        ['111',
         '001'],
        ['01',
         '01',
         '11']
    ],
    'L': [
        ['001',
         '111'],
        ['10',
         '10',
         '11'],
        ['111',
         '100'],
        ['11',
         '01',
         '01']
    ]
}

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - 2
        self.y = 0

    @property
    def matrix(self):
        return TETROMINOS[self.shape][self.rotation]

    def rotate(self, board):
        new_rot = (self.rotation + 1) % len(TETROMINOS[self.shape])
        mat = TETROMINOS[self.shape][new_rot]
        if not collides(board, mat, self.x, self.y):
            self.rotation = new_rot


def create_board():
    return [[0]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]


def collides(board, matrix, x, y):
    for j, row in enumerate(matrix):
        for i, cell in enumerate(row):
            if cell == '1':
                if i + x < 0 or i + x >= BOARD_WIDTH or j + y >= BOARD_HEIGHT:
                    return True
                if board[j + y][i + x]:
                    return True
    return False


def merge(board, matrix, x, y):
    for j, row in enumerate(matrix):
        for i, cell in enumerate(row):
            if cell == '1':
                board[j + y][i + x] = 1


def clear_lines(board):
    new_board = [row for row in board if any(v == 0 for v in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0]*BOARD_WIDTH)
    return new_board, lines_cleared


def draw_board(stdscr, board, piece):
    stdscr.clear()
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            if val:
                stdscr.addstr(y, x*2, '[]')
    matrix = piece.matrix
    for j, r in enumerate(matrix):
        for i, c in enumerate(r):
            if c == '1':
                stdscr.addstr(piece.y + j, (piece.x + i)*2, '[]')
    stdscr.refresh()


def game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    board = create_board()
    current = Piece(random.choice(list(TETROMINOS.keys())))
    last_drop = time.time()
    while True:
        draw_board(stdscr, board, current)
        # input
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None
        if key in ('a', 'KEY_LEFT') and not collides(board, current.matrix, current.x-1, current.y):
            current.x -= 1
        elif key in ('d', 'KEY_RIGHT') and not collides(board, current.matrix, current.x+1, current.y):
            current.x += 1
        elif key in ('s', 'KEY_DOWN') and not collides(board, current.matrix, current.x, current.y+1):
            current.y += 1
        elif key in ('w', 'KEY_UP'):
            current.rotate(board)
        elif key == 'q':
            break

        # gravity
        if time.time() - last_drop > 0.5:
            if not collides(board, current.matrix, current.x, current.y+1):
                current.y += 1
            else:
                merge(board, current.matrix, current.x, current.y)
                board, _ = clear_lines(board)
                current = Piece(random.choice(list(TETROMINOS.keys())))
                if collides(board, current.matrix, current.x, current.y):
                    break
            last_drop = time.time()
    stdscr.nodelay(False)
    stdscr.addstr(10, 0, "Game Over! Press any key to exit")
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(game)
