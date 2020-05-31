from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    # board.make_move('c5')
    # board.make_move('Ne5')
    board.make_move('Kf5')
    # board.make_move('c5')
    # board.make_move('Ra1')
    board.print_board()
