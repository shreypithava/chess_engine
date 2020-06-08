from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    # board.make_move('c3')
    # board.make_move('Ka7')
    board.make_move('d4')
    board.make_move('d5')
    print(board.find_all_moves())
    board.print_board()
