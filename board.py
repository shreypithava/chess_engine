class Board(object):
    def __init__(self, fen):
        self.__fen: str = fen
        self.__board_list: list[list] = []
        self.__is_whites_turn = self.__fen.split()[1] == 'w'
        self.__put_fen_in_board_list()

    def print_board(self):
        for idx, row in enumerate(self.__board_list):
            print(8 - idx, end=' ')
            for block in row:
                print(block, end=' ')
            if idx == 7:
                print('\n ', end=' ')
                for i in range(97, 105):
                    print(chr(i), end=' ')
            else:
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

    def make_move(self, move: str):
        move_legal = False
        if len(move) == 2:  # is definitely pawn
            if self.__pawn_move(move):
                move_legal = True
            else:
                print("Can't play that")
        if move_legal:
            self.__is_whites_turn = not self.__is_whites_turn

    def __pawn_move(self, move):
        al, nm = move
        if self.__is_whites_turn:
            if '4' == nm and \
                    self.__board_list[6][ord(al) - 97] == 'P' and \
                    self.__board_list[5][ord(al) - 97] == '.' and \
                    self.__board_list[4][ord(al) - 97] == '.':  # double step
                self.__board_list[6][ord(al) - 97] = '.'
                self.__board_list[4][ord(al) - 97] = 'P'
                return True
            if self.__board_list[9 - int(nm)][ord(al) - 97] == 'P' and \
                    self.__board_list[8 - int(nm)][ord(al) - 97] == '.':
                self.__board_list[9 - int(nm)][ord(al) - 97] = '.'
                self.__board_list[8 - int(nm)][ord(al) - 97] = 'P'
                return True
            return False
        else:
            if '5' == nm and \
                    self.__board_list[1][ord(al) - 97] == 'p' and \
                    self.__board_list[2][ord(al) - 97] == '.' and \
                    self.__board_list[3][ord(al) - 97] == '.':  # double step
                self.__board_list[1][ord(al) - 97] = '.'
                self.__board_list[3][ord(al) - 97] = 'p'
                return True
            if self.__board_list[7 - int(nm)][ord(al) - 97] == 'p' and \
                    self.__board_list[8 - int(nm)][ord(al) - 97] == '.':
                self.__board_list[7 - int(nm)][ord(al) - 97] = '.'
                self.__board_list[8 - int(nm)][ord(al) - 97] = 'p'
                return True
            return False
