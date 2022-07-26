from random import randint


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)
    win_combinations = [[(i, j) for i in range(3)] for j in range(3)], \
                       [[(j, i) for i in range(3)] for j in range(3)], \
                       [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    @property
    def is_human_win(self):
        return self._is_human_win

    @is_human_win.setter
    def is_human_win(self, value):
        self._is_human_win = value

    @property
    def is_computer_win(self):
        return self._is_computer_win

    @is_computer_win.setter
    def is_computer_win(self, value):
        self._is_computer_win = value

    @property
    def is_draw(self):
        return self._is_draw

    @is_draw.setter
    def is_draw(self, value):
        self._is_draw = value

    def __init__(self):
        self.pole = tuple([tuple([Cell() for i in range(3)]) for i in range(3)])
        self._is_human_win = False
        self._is_computer_win = False
        self._is_draw = False

    def check_human(self):
        for i in self.win_combinations:
            for j in i:
                self._is_human_win = len([self[x] for x in j if self[x] == self.HUMAN_X]) == 3
                if self._is_human_win:
                    return self.HUMAN_X
        return False

    def check_computer(self):
        for i in self.win_combinations:
            for j in i:
                self._is_computer_win = len([self[x] for x in j if self[x] == self.COMPUTER_O]) == 3
                if self._is_computer_win:
                    return self.COMPUTER_O
        return False

    def check_win(self):
        if self.check_computer() != False and self.check_human() != False:
            self._is_draw = True
        if self.check_human() != False and self.check_computer() == False:
            return self.HUMAN_X
        if self.check_computer() != False and self.check_human() == False:
            return self.COMPUTER_O
        if len([self[x, y] for x in range(0, 3) for y in range(0, 3) if self[x, y] == self.FREE_CELL]) == 0:
            self._is_draw = True
            return 1
        return False

    def human_go(self):
        x = tuple(map(int, input().split()))
        # print(x)
        if len(x) != 2 or x[0] not in [0, 1, 2] or x[1] not in [0, 1, 2]:
            # print('неверные координаты, попробуйте еще раз')                                   ###
            return self.human_go()
        else:
            if self.pole[x[0]][x[1]].value != 0:
                # print('клетка уже занята, укажите другие координаты')                          ###
                return self.human_go()
            self.pole[x[0]][x[1]].value = self.HUMAN_X

    def computer_go(self):
        x = (randint(0, 2), randint(0, 2))
        if len([self[x, y] for x in range(0, 3) for y in range(0, 3) if self[x, y] == self.FREE_CELL]) != 0:
            if self.pole[x[0]][x[1]].value != 0:
                return self.computer_go()

            self.pole[x[0]][x[1]].value = self.COMPUTER_O
            self.check_win()

    @staticmethod
    def check_indx(indxs_tuple):
        if type(indxs_tuple) != tuple:
            raise IndexError('некорректно указанные индексы')
        for i in indxs_tuple:
            if i not in (0, 1, 2):
                raise IndexError('некорректно указанные индексы')
        return True

    def __getitem__(self, item):
        if self.check_indx(item):
            return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, val):
        if self.check_indx(key) and val in (0, 1, 2):
            self.pole[key[0]][key[1]].value = val

    def init(self):
        self.pole = tuple([tuple([Cell() for i in range(3)]) for i in range(3)])
        self._is_human_win = False
        self._is_computer_win = False
        self._is_draw = False

    def show(self):
        for i in self.pole:
            print(*[j.value for j in i])

    def __bool__(self):
        return False if (any([self._is_human_win, self._is_computer_win, self._is_draw]) == True) else True


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0


game = TicTacToe()
game.init()
step_game = 0
game.HUMAN_X = 'X'
game.COMPUTER_O = 'Y'
while game:
    game.show()
    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()
    step_game += 1

game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
