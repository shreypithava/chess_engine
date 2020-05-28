class Board(object):
    def __init__(self, fen):
        self.__fen: str = fen
        self.__board_list: list[list] = []
        self.__is_whites_turn: bool = self.__fen.split()[1] == 'w'
        self.__put_fen_in_board_list()

    def print_fen(self):
        for row in self.__board_list:
            for block in row:
                print(block, end=' ')
            print()

    def whose_turn(self):
        if self.__is_whites_turn:
            print("White's Turn")
        else:
            print("Black's Turn")

    def return_color_pieces(self, color: str):
        counter = 0
        fen = self.__fen.split()[0]
        if color == 'w':
            for letter in fen:
                if letter.isupper():  # uppercase for white
                    counter += 1
        else:
            for letter in fen:
                if letter.islower():  # lowercase for black
                    counter += 1
        return counter

    def __put_fen_in_board_list(self):
        fen = self.__fen.split()[0]
        for idx, row in enumerate(fen.split('/')):
            self.__board_list.append([])
            for letter in row:
                if letter.isdigit():
                    for _ in range(int(letter)):
                        self.__board_list[idx].append('.')
                else:
                    self.__board_list[idx].append(letter)

    def make_move(self):
        pass


if __name__ == '__main__':
    with open('fen.txt', 'r') as f:
        board_fen = f.readline()
    board = Board(board_fen)
    board.print_fen()
