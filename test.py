from board import Board


class Test(object):
    def __init__(self):
        self.__all_fens = []
        with open('fen.txt', 'r') as f:
            for fen in f.readlines():
                self.__all_fens.append(fen.rstrip())

    def run_all_tests(self):
        self.checkmate_test1()
        self.checkmate_test2()
        self.stalemate_test1()
        self.pawn_cross_test1()
        self.castling_test1()
        self.castling_test2()
        self.castling_test3()
        self.castling_test4()
        self.all_moves_checker_test1()
        self.all_moves_checker_test2()

    def checkmate_test1(self):
        results = []
        board = Board(self.__all_fens[0])
        results.append(board.make_move('Kf4'))
        results.append(board.make_move('Kh7'))
        results.append(board.make_move('Kf5'))
        results.append(board.make_move('Kh8'))
        results.append(board.make_move('Kf6'))
        results.append(board.make_move('Kh7'))
        results.append(board.make_move('Qg6'))
        results.append(board.make_move('Kh8'))
        results.append(board.make_move('Qg7'))
        results.append(not board.stalemate())
        results.append(board.checkmate())
        print("Checkmate Test1 = {}".format(all(results)))

    def checkmate_test2(self):
        results = []
        board = Board(self.__all_fens[1])
        results.append(board.make_move('c3'))
        results.append(board.make_move('Ke4'))
        results.append(board.make_move('d3'))
        results.append(not board.stalemate())
        results.append(board.checkmate())
        print("Checkmate Test2 = {}".format(all(results)))

    def stalemate_test1(self):
        results = []
        board = Board(self.__all_fens[2])
        results.append(board.make_move('Kh8'))
        results.append(board.make_move('Qg6'))
        results.append(board.stalemate())
        print("Stalemate Test1 = {}".format(all(results)))

    def pawn_cross_test1(self):
        results = []
        board = Board(self.__all_fens[3])
        results.append(board.make_move('d4'))
        results.append(board.make_move('e5'))
        results.append(not board.make_move('fxe5'))
        results.append(board.make_move('dxe5'))
        print("Pawn Crosskill Test1 = {}".format(all(results)))

    def castling_test1(self):
        results = []
        board = Board(self.__all_fens[4])
        results.append(board.make_move('O-O'))
        print("Castling Test1 = {}".format(all(results)))

    def castling_test2(self):
        results = []
        board = Board(self.__all_fens[4])
        results.append(not board.make_move('O-O-O'))
        print("Castling Test2 = {}".format(all(results)))

    def castling_test3(self):
        results = []
        board = Board(self.__all_fens[5])
        results.append(not board.make_move('O-O'))
        results.append(board.make_move('Qxf3'))
        print("Castling Test3 = {}".format(all(results)))

    def castling_test4(self):
        results = []
        board = Board(self.__all_fens[6])
        results.append(not board.make_move('O-O'))
        results.append(not board.make_move('Qxf3'))
        results.append(not board.make_move('Kf1'))
        results.append(board.make_move('hxg3'))
        print("Castling Test4 = {}".format(all(results)))

    def all_moves_checker_test1(self):
        results = []
        board = Board(self.__all_fens[7])
        results.append(len(board.find_all_moves()) == 20)
        print("All Moves Checker Test1 = {}".format(all(results)))

    def all_moves_checker_test2(self):
        results = []
        board = Board(self.__all_fens[8])
        results.append(len(board.find_all_moves()) == 24)
        print("All Moves Checker Test2 = {}".format(all(results)))


test = Test()
test.run_all_tests()
