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
        for letter in fen:
            if letter.isupper() if color == 'w' else letter.islower():
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
        if move[0].islower():  # is definitely pawn
            if self.__pawn_move(move):
                move_legal = True
            else:
                print("Can't play that P")
        elif move[0] == 'R':  # rook move
            p = 'R' if self.__is_whites_turn else 'r'
            if self.__rook_move(move, p):
                move_legal = True
            else:
                print("Can't play that R")
        elif move[0] == 'B':  # bishop move
            p = 'B' if self.__is_whites_turn else 'b'
            if self.__bishop_move(move, p):
                move_legal = True
            else:
                print("Can't play that B")
        elif move[0] == 'Q':  # queen move
            p = 'Q' if self.__is_whites_turn else 'q'
            if self.__queen_move(move, p):
                move_legal = True
            else:
                print("Can't play that Q")
        elif move[0] == 'N':  # knight move
            p = 'N' if self.__is_whites_turn else 'n'
            if self.__knight_move(move, p):
                move_legal = True
            else:
                print("Can't play that N")
        else:  # king move
            p = 'K' if self.__is_whites_turn else 'k'
            if self.__king_move(move, p):
                move_legal = True
            else:
                print("Can't play that K")
        if move_legal:
            self.__is_whites_turn = not self.__is_whites_turn

    def __pawn_move(self, move):
        al, nm = move[0], int(move[1])
        if self.__is_whites_turn:
            if nm == 4 and \
                    self.__board_list[6][ord(al) - 97] == 'P' and \
                    self.__board_list[5][ord(al) - 97] == '.' and \
                    self.__board_list[4][ord(al) - 97] == '.':  # double step
                self.__board_list[6][ord(al) - 97] = '.'
                self.__board_list[4][ord(al) - 97] = 'P'
                return True
            if self.__board_list[9 - nm][ord(al) - 97] == 'P' and \
                    self.__board_list[8 - nm][ord(al) - 97] == '.':
                self.__board_list[9 - nm][ord(al) - 97] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = 'P'
                return True
        else:
            if nm == 5 and \
                    self.__board_list[1][ord(al) - 97] == 'p' and \
                    self.__board_list[2][ord(al) - 97] == '.' and \
                    self.__board_list[3][ord(al) - 97] == '.':  # double step
                self.__board_list[1][ord(al) - 97] = '.'
                self.__board_list[3][ord(al) - 97] = 'p'
                return True
            if self.__board_list[7 - nm][ord(al) - 97] == 'p' and \
                    self.__board_list[8 - nm][ord(al) - 97] == '.':
                self.__board_list[7 - nm][ord(al) - 97] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = 'p'
                return True
        return False

    def __rook_move(self, move, p):
        al, nm = move[1], int(move[2])
        for idx in range(nm, 0, -1):  # find piece downwards
            if self.__board_list[8 - idx][ord(al) - 97] == p:
                self.__board_list[8 - idx][ord(al) - 97] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = p
                return True
            if self.__board_list[8 - idx][ord(al) - 97] != '.':
                break
        for idx in range(nm, 9):  # find piece upwards
            if self.__board_list[8 - idx][ord(al) - 97] == p:
                self.__board_list[8 - idx][ord(al) - 97] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = p
                return True
            if self.__board_list[8 - idx][ord(al) - 97] != '.':
                break
        for idx in range(ord(al) - 97, -1, -1):  # find piece leftwards
            if self.__board_list[8 - nm][idx] == p:
                self.__board_list[8 - nm][idx] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = p
                return True
            if self.__board_list[8 - nm][idx] != '.':
                break
        for idx in range(ord(al) - 97, 8):  # find piece rightwards
            if self.__board_list[8 - nm][idx] == p:
                self.__board_list[8 - nm][idx] = '.'
                self.__board_list[8 - nm][ord(al) - 97] = p
                return True
            if self.__board_list[8 - nm][idx] != '.':
                break
        return False

    def __bishop_move(self, move, p):
        al, nm = ord(move[1]) - 97, 8 - int(move[2])

        # find piece up left
        t_al, t_nm = al, nm
        while t_al >= 0 and t_nm >= 0:
            if self.__board_list[t_nm][t_al] == p:
                self.__board_list[nm][al] = p
                self.__board_list[t_nm][t_al] = '.'
                return True
            if self.__board_list[t_nm][t_al] != '.':
                break
            t_al -= 1
            t_nm -= 1

        # find piece up right
        t_al, t_nm = al, nm
        while t_al <= 7 and t_nm >= 0:
            if self.__board_list[t_nm][t_al] == p:
                self.__board_list[nm][al] = p
                self.__board_list[t_nm][t_al] = '.'
                return True
            if self.__board_list[t_nm][t_al] != '.':
                break
            t_al += 1
            t_nm -= 1

        # find piece down right
        t_al, t_nm = al, nm
        while t_al <= 7 and t_nm <= 7:
            if self.__board_list[t_nm][t_al] == p:
                self.__board_list[nm][al] = p
                self.__board_list[t_nm][t_al] = '.'
                return True
            if self.__board_list[t_nm][t_al] != '.':
                break
            t_al += 1
            t_nm += 1

        # find piece down left
        t_al, t_nm = al, nm
        while t_al >= 0 and t_nm <= 7:
            if self.__board_list[t_nm][t_al] == p:
                self.__board_list[nm][al] = p
                self.__board_list[t_nm][t_al] = '.'
                return True
            if self.__board_list[t_nm][t_al] != '.':
                break
            t_al -= 1
            t_nm += 1

        return False

    def __knight_move(self, move, p):
        print(self)
        return False

    def __queen_move(self, move, p):
        print(self)
        return False

    def __king_move(self, move, p):
        print(self)
        return False
