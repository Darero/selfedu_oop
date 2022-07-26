import copy
from random import randint, randrange, shuffle, choice


def getrandom(num):
    a = randrange(num)
    return a


class Ceil:

    def __init__(self, around_mines=0, mine=False, fl_open=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = fl_open
        self.id = randrange(10000)


class GamePole:
    def __init__(self, N, M):
        self.N = N
        self.M = M

    def init(self):
        self.pole = [[Ceil() for i in range(self.N)] for i in range(self.N)]
        while self.M != 0:
            self.pole[getrandom(self.N)][getrandom(self.N)].mine = True
            self.M -= 1
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                self.pole[i][j].around_mines = self.get_quantity(i, j)

    def show(self):
        for i in self.pole:
            prnt_lst = [j.around_mines if j.mine == False else '#' for j in i]
            print(*prnt_lst)

    def quantity(self, lst):
        return lst.count(True)

    def get_quantity(self, i, j):
        if self.pole[i][j].mine != True:
            if i != 0 and i != self.N - 1 and j != 0 and j != self.N - 1:
                check_lst = [self.pole[y][x].mine for x in range(j - 1, j + 2) for y in range(i - 1, i + 2)]
                return self.quantity(check_lst)
            if i == 0:
                rng_i = (i, i + 2)
                rng_j = ((j - 1, j + 2) if j < self.N - 1 else (j - 1, j + 1)) if j != 0 else (j, j + 2)
                check_lst = [self.pole[y][x].mine for x in range(*rng_j) for y in range(*rng_i)]
                return self.quantity(check_lst)
            if i == self.N - 1:
                rng_i = (i - 1, i + 1)
                rng_j = ((j - 1, j + 2) if j < self.N - 1 else (j - 1, j + 1)) if j != 0 else (j, j + 2)
                check_lst = [self.pole[y][x].mine for x in range(*rng_j) for y in range(*rng_i)]
                return self.quantity(check_lst)
            if j == 0:
                rng_j = (j, j + 2)
                rng_i = ((i - 1, i + 2) if i < self.N - 1 else (i - 1, i + 1)) if i != 0 else (i, i + 2)
                check_lst = [self.pole[y][x].mine for x in range(*rng_j) for y in range(*rng_i)]
                return self.quantity(check_lst)
            if j == self.N - 1:
                rng_j = (j - 1, j + 1)
                rng_i = ((i - 1, i + 2) if i < self.N - 1 else (i - 1, i + 1)) if i != 0 else (i, i + 2)
                check_lst = [self.pole[y][x].mine for x in range(*rng_j) for y in range(*rng_i)]
                return self.quantity(check_lst)



pole_game = GamePole(10, 10)
pole_game.init()
pole_game.show()