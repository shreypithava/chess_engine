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
        elif move[0] == 'N':  # knight move
            p = 'N' if self.__is_whites_turn else 'n'
            if self.__knight_move(move, p):
                move_legal = True
            else:
                print("Can't play that N")
        else:  # king or queen move
            p = move[0].upper() if self.__is_whites_turn else move[0].lower()
            if self.__king_queen_move(move, p):
                move_legal = True
            else:
                print("Can't play that K")
        if move_legal:
            self.__is_whites_turn = not self.__is_whites_turn

    def __pawn_move(self, move):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])
        if self.__is_whites_turn:
            if nm == 4 and \
                    self.__board_list[6][al] == 'P' and \
                    self.__board_list[5][al] == '.' and \
                    self.__board_list[4][al] == '.':  # double step
                self.__board_list[6][al] = '.'
                self.__board_list[4][al] = 'P'
                return True
            if self.__board_list[nm + 1][al] == 'P' and \
                    self.__board_list[nm][al] == '.':
                self.__board_list[nm + 1][al] = '.'
                self.__board_list[nm][al] = 'P'
                return True
        else:
            if nm == 3 and \
                    self.__board_list[1][al] == 'p' and \
                    self.__board_list[2][al] == '.' and \
                    self.__board_list[3][al] == '.':  # double step
                self.__board_list[1][al] = '.'
                self.__board_list[3][al] = 'p'
                return True
            if self.__board_list[nm - 1][al] == 'p' and \
                    self.__board_list[nm][al] == '.':
                self.__board_list[nm - 1][al] = '.'
                self.__board_list[nm][al] = 'p'
                return True
        return False

    def __rook_move(self, move, p, is_king=False):
        al, nm = ord(move[1]) - 97, 8 - int(move[2])

        for idx in range(nm + 1, 8):  # find piece downwards
            if self.__board_list[idx][al] == p:
                self.__board_list[idx][al] = '.'
                self.__board_list[nm][al] = p
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(nm - 1, -1, -1):  # find piece upwards
            if self.__board_list[idx][al] == p:
                self.__board_list[idx][al] = '.'
                self.__board_list[nm][al] = p
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(al - 1, -1, -1):  # find piece leftwards
            if self.__board_list[nm][idx] == p:
                self.__board_list[nm][idx] = '.'
                self.__board_list[nm][al] = p
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break

        for idx in range(al + 1, 8):  # find piece rightwards
            if self.__board_list[nm][idx] == p:
                self.__board_list[nm][idx] = '.'
                self.__board_list[nm][al] = p
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break

        return False

    def __bishop_move(self, move, p, is_king=False):
        al, nm = ord(move[1]) - 97, 8 - int(move[2])

        # find piece up left
        t_al, t_nm = al - 1, nm - 1
        while t_al >= 0 and t_nm >= 0:
            if self.__helper(al, nm, t_al, t_nm, p):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm -= 1

        # find piece up right
        t_al, t_nm = al + 1, nm - 1
        while t_al <= 7 and t_nm >= 0:
            if self.__helper(al, nm, t_al, t_nm, p):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm -= 1

        # find piece down right
        t_al, t_nm = al + 1, nm + 1
        while t_al <= 7 and t_nm <= 7:
            if self.__helper(al, nm, t_al, t_nm, p):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm += 1

        # find piece down left
        t_al, t_nm = al - 1, nm + 1
        while t_al >= 0 and t_nm <= 7:
            if self.__helper(al, nm, t_al, t_nm, p):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm += 1

        return False

    def __helper(self, al, nm, t_al, t_nm, p):
        if self.__board_list[t_nm][t_al] == p:
            self.__board_list[nm][al] = p
            self.__board_list[t_nm][t_al] = '.'
            return True
        return False

    def __knight_move(self, move, p):
        al, nm = ord(move[1]) - 97, 8 - int(move[2])
        # up
        if nm - 2 >= 0:
            if al - 1 >= 0 and self.__board_list[nm - 2][al - 1] == p:
                self.__board_list[nm - 2][al - 1] = '.'
                self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm - 2][al + 1] == p:
                self.__board_list[nm - 2][al + 1] = '.'
                self.__board_list[nm][al] = p
                return True
        # down
        if nm + 2 <= 7:
            if al - 1 >= 0 and self.__board_list[nm + 2][al - 1] == p:
                self.__board_list[nm + 2][al - 1] = '.'
                self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm + 2][al + 1] == p:
                self.__board_list[nm + 2][al + 1] = '.'
                self.__board_list[nm][al] = p
                return True
        # left
        if al - 2 >= 0:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al - 2] == p:
                self.__board_list[nm - 1][al - 2] = '.'
                self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al - 2] == p:
                self.__board_list[nm + 1][al - 2] = '.'
                self.__board_list[nm][al] = p
                return True
        # right
        if al + 2 <= 7:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al + 2] == p:
                self.__board_list[nm - 1][al + 2] = '.'
                self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al + 2] == p:
                self.__board_list[nm + 1][al + 2] = '.'
                self.__board_list[nm][al] = p
                return True
        return False

    def __king_queen_move(self, move, p):
        if self.__bishop_move(move, p, p.upper() == 'K'):
            return True
        return self.__rook_move(move, p, p.upper() == 'K')
