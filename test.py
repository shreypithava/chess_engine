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
        print()
        self.stalemate_test1()

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


test = Test()
test.run_all_tests()
