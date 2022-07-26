from random import randint, seed, choice
from time import time

seed(time())


class CoordDescriptor:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Ship:
    x = CoordDescriptor()
    y = CoordDescriptor()

    def __init__(self, length, tp=randint(1, 2), x=None, y=None):
        self.x = x
        self.y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [1 for i in range(self._length)]
        if self.x != None and self.y != None:
            self.set_start_coords(self.x, self.y)

    def set_start_coords(self, x, y):
        self.start_coord_x = x
        self.start_coord_y = y
        self.x = x
        self.y = y
        if self._tp == 1:
            self.end_coord_x = self.x + (self._length - 1)
            self.end_coord_y = self.y
            self.coords_list = [[self.x + n, self.y] for n in range(self._length)]
        elif self._tp == 2:
            self.end_coord_y = self.y + (self._length - 1)
            self.end_coord_x = self.x
            self.coords_list = [[self.x, self.y + n] for n in range(self._length)]

    def get_start_coords(self):
        return self.start_coord_x, self.start_coord_y

    def move(self, go):
        if self._is_move is True and go in (-1, 1):
            if self._tp == 1:
                self.set_start_coords(self.x + go, self.y)
            if self._tp == 2:
                self.set_start_coords(self.x, self.y + go)

    def is_collide(self, obj):
        if (obj.x - 1 <= self.x <= obj.end_coord_x + 1
                and obj.y - 1 <= self.y <= obj.end_coord_y + 1):
            return True
        if (obj.x - 1 <= self.end_coord_x <= obj.end_coord_x + 1
                and obj.y - 1 <= self.end_coord_y <= obj.end_coord_y + 1):
            return True
        else:
            return False

    def is_out_pole(self, size):
        lst = []
        for i in self.coords_list:
            lst.append(0 <= i[0] < size and 0 <= i[1] < size)
        if all(lst) == True:
            return False
        return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __iter__(self):
        return iter(self.coords_list)


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []

    def init(self):

        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]

        for i in self._ships:
            i.set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))

        for i in self._ships:
            collide_check_list = list(filter(lambda x: i.is_collide(x) if i is not x else None, self._ships))
            condition = i.is_out_pole(self._size) == True or len(collide_check_list) != 0
            # print(self._ships.index(i), 'entered')
            # print(self._ships.index(i), len(collide_check_list), i.is_out_pole(self._size))
            if condition:
                while condition == True:
                    i.tp = randint(1, 2)
                    i.set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
                    collide_check_list = list(filter(lambda x: i.is_collide(x) if i is not x else None, self._ships))
                    condition = i.is_out_pole(self._size) == True or len(collide_check_list) != 0
                    if not condition:
                        # print(self._ships.index(i), 'passed')
                        break

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for i in self._ships:
            a = choice([-1, 1])
            i.move(a)
            collide_check_list = list(filter(lambda x: i.is_collide(x) if i is not x else None, self._ships))
            condition = i.is_out_pole(self._size) == True or len(collide_check_list) != 0
            if condition:
                i.move(-a)
                i.move(-a)
            else:
                continue
            collide_check_list = list(filter(lambda x: i.is_collide(x) if i is not x else None, self._ships))
            condition = i.is_out_pole(self._size) == True or len(collide_check_list) != 0
            if condition:
                i.move(a)
            else:
                continue

    def show(self):
        pole = [[0 for i in range(self._size)] for j in range(self._size)]
        for j in self._ships:
            # print(j.coords_list)
            for n in range(j._length):
                if j._tp == 1:
                    # print(j.x, n)
                    pole[j.y][j.x + n] = j[n]
                if j._tp == 2:
                    pole[j.y + n][j.x] = j[n]
        for i in pole:
            print(i)
        print('--------------------------------------')


pole = Ship(4, tp=1)
# pole.init()
# print(pole.get_ships())
# for i in pole._ships:
#    print(i.y, i.x, i.end_coord_x, i.end_coord_y, '////', i._length, i)
# pole.show()
b = GamePole(10)
b.init()
b.show()
# for i in b.get_ships():  #_______HIT CHECK
#     for j in i:
#         if (j[0], j[1]) == (8, 8):
#             i[i.coords_list.index(j)] = 2
#             print(i._cells)
#             print('gotcha')
b.move_ships()
b.show()
b.move_ships()
b.show()
b.move_ships()
b.show()
b.move_ships()
b.show()
