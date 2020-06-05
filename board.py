class Board(object):
    def __init__(self, fen):
        self.__fen: str = fen
        self.__board_list: list[list] = []
        self.__is_w_turn = self.__fen.split()[1] == 'w'
        self.__check_list = [False, False]
        self.__put_fen_in_board_list(self.__fen.split()[0])

    def __put_fen_in_board_list(self, fen):
        self.__board_list = []
        for idx, row in enumerate(fen.split('/')):
            self.__board_list.append([])
            for letter in row:
                if letter.isdigit():
                    for _ in range(int(letter)):
                        self.__board_list[idx].append('.')
                else:
                    self.__board_list[idx].append(letter)

    def __put_board_in_fen(self):
        fen = ''
        counter = 0
        for row in range(8):
            for col in range(8):
                if self.__board_list[row][col] != '.':
                    if counter > 0:
                        fen += str(counter)
                        counter = 0
                    fen += self.__board_list[row][col]
                else:
                    counter += 1
            if counter > 0:
                fen += str(counter)
                counter = 0
            if row != 7:
                fen += '/'
        full_fen = [fen] + self.__fen.split()[1:]
        self.__fen = ' '.join(full_fen)

    def print_fen(self):
        print(self.__fen.split()[0])

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
        if self.__is_w_turn:
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

    def make_move(self, move: str):
        move_legal = False
        if move[0].islower():  # is definitely pawn
            if self.__pawn_move(move, for_kill='x' in move):
                move_legal = True
            else:
                print("Can't play that P")
        elif move[0] == 'R':  # rook move
            p = 'R' if self.__is_w_turn else 'r'
            if self.__rook_move(move[2 if 'x' in move else 1:], p,
                                for_kill='x' in move):
                move_legal = True
            else:
                print("Can't play that R")
        elif move[0] == 'B':  # bishop move
            p = 'B' if self.__is_w_turn else 'b'
            if self.__bishop_move(move[2 if 'x' in move else 1:], p,
                                  for_kill='x' in move):
                move_legal = True
            else:
                print("Can't play that B")
        elif move[0] == 'N':  # knight move
            p = 'N' if self.__is_w_turn else 'n'
            if self.__knight_move(move[2 if 'x' in move else 1:], p,
                                  for_kill='x' in move):
                move_legal = True
            else:
                print("Can't play that N")
        else:  # king or queen move
            p = move[0].upper() if self.__is_w_turn else move[0].lower()
            if self.__king_queen_move(move[2 if 'x' in move else 1:], p,
                                      for_kill='x' in move):
                move_legal = True
            else:
                print("Can't play that {}".format(move[0]))
        if move_legal:
            if self.__if_getting_checked():
                self.__put_fen_in_board_list(self.__fen.split()[0])
                return False
            if self.__checked():
                if self.__checkmate():
                    print('Checkmate, Game over')
                else:
                    self.__check_list[1 if self.__is_w_turn else 0] = True
                    print('{} checked'.format('Black' if self.__is_w_turn
                                              else 'White'))
            self.__put_board_in_fen()
            self.__is_w_turn = not self.__is_w_turn
        return move_legal

    def __pawn_move(self, move, for_check=False, for_kill=False):
        al, nm = ord(move[2 if len(move) == 4 else 0]) - 97, \
                 8 - int(move[3 if len(move) == 4 else 1])
        if self.__is_w_turn:
            if for_kill:
                if self.__board_list[nm][al].islower() and \
                        self.__board_list[nm + 1][ord(move[0]) - 97] == 'P':
                    self.__board_list[nm][al] = 'P'
                    self.__board_list[nm + 1][ord(move[0]) - 97] = '.'
                    return True
                return False
            if for_check:
                if nm <= 5:
                    if al != 0 and nm != 7:
                        return self.__board_list[nm + 1][al - 1] == 'P' or \
                               self.__board_list[nm + 1][al + 1] == 'P'
                    if al == 0:
                        return self.__board_list[nm + 1][al + 1] == 'P'
                    if nm == 7:
                        return self.__board_list[nm + 1][al - 1] == 'P'
                return False
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
            if for_kill:
                if self.__board_list[nm][al].isupper() and \
                        self.__board_list[nm - 1][ord(move[0]) - 97] == 'p':
                    self.__board_list[nm][al] = 'p'
                    self.__board_list[nm - 1][ord(move[0]) - 97] = '.'
                    return True
                return False
            if for_check:
                if nm >= 2:
                    if al != 0 and nm != 7:
                        return self.__board_list[nm - 1][al - 1] == 'p' or \
                               self.__board_list[nm - 1][al + 1] == 'p'
                    if al == 0:
                        return self.__board_list[nm - 1][al + 1] == 'p'
                    if nm == 7:
                        return self.__board_list[nm - 1][al - 1] == 'p'
                return False
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

    def __rook_move(self, move, p, is_king=False,
                    for_check=False, for_kill=False):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])

        if (for_kill and
            not ((self.__is_w_turn and
                  self.__board_list[nm][al].islower()) or
                 ((not self.__is_w_turn) and
                  self.__board_list[nm][al].isupper())) or
            (not for_kill and
             self.__board_list[nm][al] != '.')) and not for_check:
            return False

        for idx in range(nm + 1, 8):  # find piece downwards
            if self.__board_list[idx][al] == p:
                if not for_check:
                    self.__board_list[idx][al] = '.'
                    self.__board_list[nm][al] = p
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(nm - 1, -1, -1):  # find piece upwards
            if self.__board_list[idx][al] == p:
                if not for_check:
                    self.__board_list[idx][al] = '.'
                    self.__board_list[nm][al] = p
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(al - 1, -1, -1):  # find piece leftwards
            if self.__board_list[nm][idx] == p:
                if not for_check:
                    self.__board_list[nm][idx] = '.'
                    self.__board_list[nm][al] = p
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break

        for idx in range(al + 1, 8):  # find piece rightwards
            if self.__board_list[nm][idx] == p:
                if not for_check:
                    self.__board_list[nm][idx] = '.'
                    self.__board_list[nm][al] = p
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break

        return False

    def __bishop_move(self, move, p, is_king=False,
                      for_check=False, for_kill=False):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])

        if (for_kill and
            not ((self.__is_w_turn and
                  self.__board_list[nm][al].islower()) or
                 ((not self.__is_w_turn) and
                  self.__board_list[nm][al].isupper())) or
            (not for_kill and
             self.__board_list[nm][al] != '.')) and not for_check:
            return False

        # find piece up left
        t_al, t_nm = al - 1, nm - 1
        while t_al >= 0 and t_nm >= 0:
            if self.__helper(al, nm, t_al, t_nm, p, for_check):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm -= 1

        # find piece up right
        t_al, t_nm = al + 1, nm - 1
        while t_al <= 7 and t_nm >= 0:
            if self.__helper(al, nm, t_al, t_nm, p, for_check):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm -= 1

        # find piece down right
        t_al, t_nm = al + 1, nm + 1
        while t_al <= 7 and t_nm <= 7:
            if self.__helper(al, nm, t_al, t_nm, p, for_check):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm += 1

        # find piece down left
        t_al, t_nm = al - 1, nm + 1
        while t_al >= 0 and t_nm <= 7:
            if self.__helper(al, nm, t_al, t_nm, p, for_check):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm += 1

        return False

    def __helper(self, al, nm, t_al, t_nm, p, for_check=False):
        if self.__board_list[t_nm][t_al] == p:
            if not for_check:
                self.__board_list[nm][al] = p
                self.__board_list[t_nm][t_al] = '.'
            return True
        return False

    def __knight_move(self, move, p, for_check=False, for_kill=False):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])

        if (for_kill and
            not ((self.__is_w_turn and
                  self.__board_list[nm][al].islower()) or
                 ((not self.__is_w_turn) and
                  self.__board_list[nm][al].isupper())) or
            (not for_kill and
             self.__board_list[nm][al] != '.')) and not for_check:
            return False

        # up
        if nm - 2 >= 0:
            if al - 1 >= 0 and self.__board_list[nm - 2][al - 1] == p:
                if not for_check:
                    self.__board_list[nm - 2][al - 1] = '.'
                    self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm - 2][al + 1] == p:
                if not for_check:
                    self.__board_list[nm - 2][al + 1] = '.'
                    self.__board_list[nm][al] = p
                return True
        # down
        if nm + 2 <= 7:
            if al - 1 >= 0 and self.__board_list[nm + 2][al - 1] == p:
                if not for_check:
                    self.__board_list[nm + 2][al - 1] = '.'
                    self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm + 2][al + 1] == p:
                if not for_check:
                    self.__board_list[nm + 2][al + 1] = '.'
                    self.__board_list[nm][al] = p
                return True
        # left
        if al - 2 >= 0:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al - 2] == p:
                if not for_check:
                    self.__board_list[nm - 1][al - 2] = '.'
                    self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al - 2] == p:
                if not for_check:
                    self.__board_list[nm + 1][al - 2] = '.'
                    self.__board_list[nm][al] = p
                return True
        # right
        if al + 2 <= 7:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al + 2] == p:
                if not for_check:
                    self.__board_list[nm - 1][al + 2] = '.'
                    self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al + 2] == p:
                if not for_check:
                    self.__board_list[nm + 1][al + 2] = '.'
                    self.__board_list[nm][al] = p
                return True
        return False

    def __king_queen_move(self, move, p, for_check=False, for_kill=False):
        if self.__bishop_move(move, p, p.upper() == 'K', for_check, for_kill):
            return True
        return self.__rook_move(move, p, p.upper() == 'K', for_check, for_kill)

    def __checked(self):
        position = self.__find_king()
        if self.__rook_move(position, 'R' if self.__is_w_turn else 'r',
                            for_check=True):
            return True
        if self.__bishop_move(position, 'B' if self.__is_w_turn else 'b',
                              for_check=True):
            return True
        if self.__knight_move(position, 'N' if self.__is_w_turn else 'n',
                              True):
            return True
        if self.__king_queen_move(position, 'Q' if self.__is_w_turn else 'q',
                                  True):
            return True
        return self.__pawn_move(position, True)

    def __find_king(self):
        k = 'k' if self.__is_w_turn else 'K'

        for num in range(8):
            for al in range(8):
                if k == self.__board_list[num][al]:
                    return '{}{}'.format(chr(al + 97), 8 - num)
        return ''

    def __if_getting_checked(self):
        self.__is_w_turn = not self.__is_w_turn
        is_still_checked = self.__checked()
        self.__is_w_turn = not self.__is_w_turn
        return is_still_checked

    def __checkmate(self):
        self.__is_w_turn = not self.__is_w_turn
        # is_checkmate = len(self.find_all_moves()) == 0  # TODO: fix this
        self.__is_w_turn = not self.__is_w_turn
        return False

    def find_all_moves(self):
        all_moves = []
        for num in range(8):
            for al in range(8):
                if self.__is_w_turn and self.__board_list[num][al].isupper():
                    pass
                elif (not self.__is_w_turn) and \
                        self.__board_list[num][al].islower():
                    pass
        return all_moves
