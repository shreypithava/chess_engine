from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    board.make_move('exd4')
    # board.make_move('Kd3')
    board.print_board()
