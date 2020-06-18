class Board(object):
    def __init__(self, fen):
        self.__fen: str = fen
        self.__board_list: list[list] = []
        self.__is_w_turn = self.__fen.split()[1] == 'w'
        self.__can_w_castle = [True, True]
        self.__can_b_castle = [True, True]  # Kingside, Queenside
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
        print()  # don't remove this

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

    def make_move(self, move: str, for_all_moves_checker=False) -> bool:
        if 'O' in move:
            p = 'C'
        else:
            p = move[0] if self.__is_w_turn else move[0].lower()

        if p == 'C':
            move_legal = self.__can_castle(move)
        elif move[0] == 'R':
            move_legal = self.__rook_move(move[2 if 'x' in move else 1:],
                                          p, 'x' in move)
        elif move[0] == 'B':
            move_legal = self.__bishop_move(move[2 if 'x' in move else 1:],
                                            p, 'x' in move)
        elif move[0] == 'N':
            move_legal = self.__knight_move(move[2 if 'x' in move else 1:],
                                            p, 'x' in move)
        elif move[0] == 'Q':
            move_legal = self.__king_queen_move(move[2 if 'x' in move else 1:],
                                                p, 'x' in move)
        elif move[0] == 'K':
            move_legal = self.__king_queen_move(move[2 if 'x' in move else 1:],
                                                p, 'x' in move)
        else:
            move_legal = self.__pawn_move(move[2 if 'x' in move else 0:],
                                          'P' if self.__is_w_turn else 'p',
                                          'x' in move,
                                          block=ord(move[0]) - 97)
        if move_legal:
            if self.__is_getting_checked():
                self.__put_fen_in_board_list(self.__fen.split()[0])
                return False
            if for_all_moves_checker:
                self.__put_fen_in_board_list(self.__fen.split()[0])
                return True

            if move[0] == 'K':
                if self.__is_w_turn:
                    self.__can_w_castle = [False, False]
                else:
                    self.__can_b_castle = [False, False]

            checked = self.__is_check_given()

            self.__put_board_in_fen()
            self.__is_w_turn = not self.__is_w_turn

            if not checked:
                if self.stalemate():
                    # print("Stalemate!! It's a Draw")
                    pass
            else:
                if self.checkmate():
                    # checkmate
                    pass
                else:
                    # only check
                    pass

        return move_legal

    def __can_castle(self, move, to_move=True):
        def __no_pieces(al, nm) -> bool:
            for idx in range(al, al + (3 if al == 1 else 2)):
                if self.__board_list[nm][idx] != '.':
                    return False
            return True

        def __check_in_castle_moves(queenside: bool) -> bool:
            nm = 7 if self.__is_w_turn else 0
            al = 4
            for idx in range(al, (al - 3) if queenside else (al + 3),
                             -1 if queenside else 1):
                self.__board_list[nm][idx + 1] = self.__board_list[nm][idx]
                self.__board_list[nm][idx] = '.'

                if self.__is_getting_checked():
                    self.__board_list[nm][al] = 'K' if self.__is_w_turn \
                        else 'k'
                    self.__board_list[nm][idx + 1] = '.'
                    return True

            self.__board_list[nm][al] = 'K' if self.__is_w_turn else 'k'
            self.__board_list[nm][(al - 2) if queenside else (al + 2)] = '.'
            return False

        if move == 'O-O':
            if self.__is_w_turn:
                if not self.__can_w_castle[0] or not __no_pieces(5, 7) or \
                        self.__board_list[7][4] != 'K' or \
                        self.__board_list[7][7] != 'R':
                    return False
            else:
                if not self.__can_b_castle[0] or not __no_pieces(5, 0) or \
                        self.__board_list[0][4] != 'k' or \
                        self.__board_list[0][7] != 'r':
                    return False

        elif move == 'O-O-O':
            if self.__is_w_turn:
                if not self.__can_w_castle[1] or not __no_pieces(1, 7) or \
                        self.__board_list[7][4] != 'K' or \
                        self.__board_list[7][0] != 'R':
                    return False
            else:
                if not self.__can_b_castle[1] or not __no_pieces(1, 0) or \
                        self.__board_list[0][4] != 'k' or \
                        self.__board_list[0][0] != 'r':
                    return False

        else:
            return False

        if __check_in_castle_moves(move.count('O') == 3):
            return False
        if to_move:
            self.__castle(move.count('O') == 3)

        return True

    def __castle(self, queenside: bool):
        if self.__is_w_turn:
            self.__can_w_castle = [False, False]
            nm = 7
        else:
            self.__can_b_castle = [False, False]
            nm = 0

        if queenside:
            self.__board_list[nm][2] = 'K' if self.__is_w_turn else 'k'
            self.__board_list[nm][3] = 'R' if self.__is_w_turn else 'r'
            self.__board_list[nm][0] = '.'
        else:
            self.__board_list[nm][6] = 'K' if self.__is_w_turn else 'k'
            self.__board_list[nm][5] = 'R' if self.__is_w_turn else 'r'
            self.__board_list[nm][7] = '.'

        self.__board_list[nm][4] = '.'

    def __pawn_move(self, move, p, for_kill, block=-1, to_move=True):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])
        if not for_kill:
            if self.__is_w_turn:
                if not nm <= 5:
                    return False
                if nm == 4 and \
                        self.__board_list[4][al] == '.' and \
                        self.__board_list[5][al] == '.' and \
                        self.__board_list[6][al] == p:
                    self.__board_list[4][al] = p
                    self.__board_list[6][al] = '.'
                    return True
                if self.__board_list[nm][al] == '.' and \
                        self.__board_list[nm + 1][al] == p:
                    self.__board_list[nm][al] = p
                    self.__board_list[nm + 1][al] = '.'
                    return True
            else:
                if nm <= 1:
                    return False
                if nm == 3 and \
                        self.__board_list[2][al] == '.' and \
                        self.__board_list[3][al] == '.' and \
                        self.__board_list[1][al] == p:
                    self.__board_list[3][al] = p
                    self.__board_list[1][al] = '.'
                    return True
                if self.__board_list[nm][al] == '.' and \
                        self.__board_list[nm - 1][al] == p:
                    self.__board_list[nm][al] = p
                    self.__board_list[nm - 1][al] = '.'
                    return True
        elif block != -1:
            if self.__is_w_turn:
                if self.__board_list[nm][al].islower() and \
                        self.__board_list[nm + 1][block] == p and \
                        abs(block - al) == 1:
                    if to_move:
                        self.__board_list[nm + 1][block] = '.'
                        self.__board_list[nm][al] = p
                    return True
            else:
                if self.__board_list[nm][al].isupper() and \
                        self.__board_list[nm - 1][block] == p and \
                        abs(block - al) == 1:
                    if to_move:
                        self.__board_list[nm - 1][block] = '.'
                        self.__board_list[nm][al] = p
                    return True

        return False

    def __rook_move(self, move, p, for_kill, is_king=False, to_move=True):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])

        if (for_kill and not ((self.__is_w_turn and
                               self.__board_list[nm][al].islower())
                              or
                              (not self.__is_w_turn and
                               self.__board_list[nm][al].isupper()))) \
                or \
                (not for_kill and self.__board_list[nm][al] != '.'):
            return False

        for idx in range(nm + 1, 8):  # find piece downwards
            if self.__helper(idx, al, nm, al, p, to_move):
                if to_move and al == 0 and nm == 7:
                    self.__can_w_castle[0] = False
                if to_move and al == 7 and nm == 7:
                    self.__can_w_castle[1] = False
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(nm - 1, -1, -1):  # find piece upwards
            if self.__helper(idx, al, nm, al, p, to_move):
                if to_move and al == 0 and nm == 0:
                    self.__can_b_castle[1] = False
                if to_move and al == 7 and nm == 0:
                    self.__can_b_castle[0] = False
                return True
            if self.__board_list[idx][al] != '.' or is_king:
                break

        for idx in range(al - 1, -1, -1):  # find piece leftwards
            if self.__helper(nm, idx, nm, al, p, to_move):
                if to_move and al == 0 and nm == 7:
                    self.__can_w_castle[1] = False
                if to_move and al == 0 and nm == 0:
                    self.__can_b_castle[1] = False
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break

        for idx in range(al + 1, 8):  # find piece rightwards
            if self.__helper(nm, idx, nm, al, p, to_move):
                if to_move and al == 7 and nm == 7:
                    self.__can_w_castle[0] = False
                if to_move and al == 7 and nm == 0:
                    self.__can_b_castle[0] = False
                return True
            if self.__board_list[nm][idx] != '.' or is_king:
                break
        return False

    def __bishop_move(self, move, p, for_kill, is_king=False, to_move=True):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])

        if (for_kill and not ((self.__is_w_turn and
                               self.__board_list[nm][al].islower())
                              or
                              (not self.__is_w_turn and
                               self.__board_list[nm][al].isupper()))) \
                or \
                (not for_kill and self.__board_list[nm][al] != '.'):
            return False

        # find piece up left
        t_al, t_nm = al - 1, nm - 1
        while t_al >= 0 and t_nm >= 0:
            if self.__helper(t_nm, t_al, nm, al, p, to_move):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm -= 1

        # find piece up right
        t_al, t_nm = al + 1, nm - 1
        while t_al <= 7 and t_nm >= 0:
            if self.__helper(t_nm, t_al, nm, al, p, to_move):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm -= 1

        # find piece down right
        t_al, t_nm = al + 1, nm + 1
        while t_al <= 7 and t_nm <= 7:
            if self.__helper(t_nm, t_al, nm, al, p, to_move):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al += 1
            t_nm += 1

        # find piece down left
        t_al, t_nm = al - 1, nm + 1
        while t_al >= 0 and t_nm <= 7:
            if self.__helper(t_nm, t_al, nm, al, p, to_move):
                return True
            if self.__board_list[t_nm][t_al] != '.' or is_king:
                break
            t_al -= 1
            t_nm += 1
        return False

    def __helper(self, from_nm, from_al, to_nm, to_al, p, to_move=True):
        if self.__board_list[from_nm][from_al] == p:
            if to_move:
                self.__board_list[from_nm][from_al] = '.'
                self.__board_list[to_nm][to_al] = p
            return True
        return False

    def __knight_move(self, move, p, for_kill, to_move=True):
        al, nm = ord(move[0]) - 97, 8 - int(move[1])
        if (for_kill and not ((self.__is_w_turn and
                               self.__board_list[nm][al].islower())
                              or
                              (not self.__is_w_turn and
                               self.__board_list[nm][al].isupper()))) \
                or \
                (not for_kill and self.__board_list[nm][al] != '.'):
            return False

        # up
        if nm - 2 >= 0:
            if al - 1 >= 0 and self.__board_list[nm - 2][al - 1] == p:
                if to_move:
                    self.__board_list[nm - 2][al - 1] = '.'
                    self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm - 2][al + 1] == p:
                if to_move:
                    self.__board_list[nm - 2][al + 1] = '.'
                    self.__board_list[nm][al] = p
                return True
        # down
        if nm + 2 <= 7:
            if al - 1 >= 0 and self.__board_list[nm + 2][al - 1] == p:
                if to_move:
                    self.__board_list[nm + 2][al - 1] = '.'
                    self.__board_list[nm][al] = p
                return True
            if al + 1 <= 7 and self.__board_list[nm + 2][al + 1] == p:
                if to_move:
                    self.__board_list[nm + 2][al + 1] = '.'
                    self.__board_list[nm][al] = p
                return True
        # left
        if al - 2 >= 0:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al - 2] == p:
                if to_move:
                    self.__board_list[nm - 1][al - 2] = '.'
                    self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al - 2] == p:
                if to_move:
                    self.__board_list[nm + 1][al - 2] = '.'
                    self.__board_list[nm][al] = p
                return True
        # right
        if al + 2 <= 7:
            if nm - 1 >= 0 and self.__board_list[nm - 1][al + 2] == p:
                if to_move:
                    self.__board_list[nm - 1][al + 2] = '.'
                    self.__board_list[nm][al] = p
                return True
            if nm + 1 <= 7 and self.__board_list[nm + 1][al + 2] == p:
                if to_move:
                    self.__board_list[nm + 1][al + 2] = '.'
                    self.__board_list[nm][al] = p
                return True
        return False

    def __king_queen_move(self, move, p, for_kill, to_move=True):
        if self.__bishop_move(move, p, for_kill, p.upper() == 'K', to_move):
            return True
        return self.__rook_move(move, p, for_kill, p.upper() == 'K', to_move)

    def __is_check_given(self):
        position = ''
        k = 'k' if self.__is_w_turn else 'K'

        for num in range(8):
            for al in range(8):
                if k == self.__board_list[num][al]:
                    position = '{}{}'.format(chr(al + 97), 8 - num)

        # finds white's king if blacks move
        if self.__rook_move(position, 'R' if self.__is_w_turn else 'r',
                            for_kill=True, is_king=False, to_move=False):
            return True
        if self.__bishop_move(position, 'B' if self.__is_w_turn else 'b',
                              for_kill=True, is_king=False, to_move=False):
            return True
        if self.__knight_move(position, 'N' if self.__is_w_turn else 'n',
                              for_kill=True, to_move=False):
            return True
        if self.__king_queen_move(position, 'Q' if self.__is_w_turn else 'q',
                                  for_kill=True, to_move=False):
            return True
        if self.__king_queen_move(position, 'K' if self.__is_w_turn else 'k',
                                  for_kill=True, to_move=False):
            return True
        if 'a' not in position and 'h' not in position:
            return self.__pawn_move(position, 'P' if self.__is_w_turn else 'p',
                                    for_kill=True, block=ord(position[0]) - 98,
                                    to_move=False) \
                   or \
                   self.__pawn_move(position, 'P' if self.__is_w_turn else 'p',
                                    for_kill=True, block=ord(position[0]) - 96,
                                    to_move=False)
        if 'a' not in position:
            return self.__pawn_move(position, 'P' if self.__is_w_turn else 'p',
                                    for_kill=True, block=6,
                                    to_move=False)
        if 'h' not in position:
            return self.__pawn_move(position, 'P' if self.__is_w_turn else 'p',
                                    for_kill=True, block=1,
                                    to_move=False)

        return False

    def __is_getting_checked(self):
        self.__is_w_turn = not self.__is_w_turn
        got_checked = self.__is_check_given()
        self.__is_w_turn = not self.__is_w_turn
        return got_checked

    def checkmate(self):
        return len(self.find_all_moves()) == 0

    def stalemate(self):
        return not self.__is_getting_checked() and \
               len(self.find_all_moves()) == 0

    def find_all_moves(self):
        pieces = 'RBNQK'
        all_moves = []
        for num in range(8):
            for al in range(8):
                if self.__is_w_turn:
                    if num == 7 and al == 4:
                        if self.make_move('O-O', True):
                            all_moves.append('O-O')
                        if self.make_move('O-O-O', True):
                            all_moves.append('O-O-O')
                    if self.__board_list[num][al].islower() or \
                            self.__board_list[num][al] == '.':
                        for letter in pieces:
                            move = '{}{}{}{}'.format(letter,
                                                     'x' if self.__board_list[num][al].islower() else '',  # noqa
                                                     chr(97 + al),
                                                     8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        if num >= 6:
                            continue
                        if 0 < al < 7 and self.__board_list[num][al].islower():
                            moves = '{}x{}{}'.format(chr(97 + al - 1),
                                                     chr(97 + al), 8 - num), \
                                    '{}x{}{}'.format(chr(97 + al + 1),
                                                     chr(97 + al), 8 - num)
                            if self.make_move(moves[0], True):
                                all_moves.append(moves[0])
                            if self.make_move(moves[1], True):
                                all_moves.append(moves[1])
                        elif al == 7 and self.__board_list[num][al].islower():
                            move = 'gxh{}'.format(8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        elif al == 0 and self.__board_list[num][al].islower():
                            move = 'bxa{}'.format(8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        else:
                            move = '{}{}'.format(chr(al + 97), 8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                else:
                    if num == 0 and al == 4:
                        if self.make_move('O-O', True):
                            all_moves.append('O-O')
                        if self.make_move('O-O-O', True):
                            all_moves.append('O-O-O')
                    if self.__board_list[num][al].isupper() or \
                            self.__board_list[num][al] == '.':
                        for letter in pieces:
                            move = '{}{}{}{}'.format(letter,
                                                     'x' if self.__board_list[num][al].isupper() else '',  # noqa
                                                     chr(97 + al),
                                                     8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        if num <= 1:
                            continue
                        if 0 < al < 7 and self.__board_list[num][al].isupper():
                            moves = '{}x{}{}'.format(chr(97 + al - 1),
                                                     chr(97 + al), 8 - num), \
                                    '{}x{}{}'.format(chr(97 + al + 1),
                                                     chr(97 + al), 8 - num)
                            if self.make_move(moves[0], True):
                                all_moves.append(moves[0])
                            if self.make_move(moves[1], True):
                                all_moves.append(moves[1])
                        elif al == 7 and self.__board_list[num][al].isupper():
                            move = 'gxh{}'.format(8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        elif al == 0 and self.__board_list[num][al].isupper():
                            move = 'bxa{}'.format(8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)
                        else:
                            move = '{}{}'.format(chr(al + 97), 8 - num)
                            if self.make_move(move, True):
                                all_moves.append(move)

        return all_moves
