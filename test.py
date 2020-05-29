from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    # board.make_move('a4')
    # board.make_move('a5')
    board.make_move('Be7')
    # board.make_move('c5')
    # board.make_move('Ra1')
    board.print_board()
