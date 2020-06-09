from board import Board

if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    board.make_move('e3')
    board.make_move('Ke4')
    board.make_move('d3')
    # print(len(board.find_all_moves()))
    # board.make_move('d5')
    board.print_board()
    board.whose_turn()
    # print(board.find_all_moves())
