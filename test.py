from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    board.make_move('e3')
    # board.make_move('e5')
    # board.make_move('c4')
    # board.make_move('e4')
    board.print_board()
