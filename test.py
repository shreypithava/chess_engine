from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    board.make_move('Qxd7')
    # board.make_move('d5')
    board.print_board()
