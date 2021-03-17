import texttable
from random import randint


class Board:
    def __init__(self, dimension, apple_count):
        self.__apple_count = apple_count
        self.__dimension = dimension
        self.__board = [[' ' for i in range(dimension + 2)] for j in range(dimension + 2)]
        self.border_matrix()
        center = self.initialize_snake()
        self.__snake = [[center - 1, center], [center, center], [center + 1, center]]
        self.__added_all_apples = True
        self.__apples = []
        apples_added = self.initialize_apples()
        if apples_added != self.__apple_count:
            self.__added_all_apples = False
        self.__apple_count = apples_added

    @property
    def board(self):
        return self.__board

    def pop_tail(self):
        return self.__snake.pop(-1)

    def push_head(self, new_head):
        self.__snake.insert(0, new_head)

    def push_tail(self, new_tail):
        self.__snake.append(new_tail)

    def pop_apple(self, apple_to_pop):
        for i in range(len(self.__apples)):
            if self.__apples[i] == apple_to_pop:
                self.__apples.pop(i)
                break

    def __getitem__(self, item):
        return self.__board[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.__board[key[0]][key[1]] = value

    @property
    def added_all_apples(self):
        return self.__added_all_apples

    @property
    def head(self):
        return self.__snake[0]

    @property
    def tail(self):
        return self.__snake[-1]

    @property
    def apples(self):
        return self.__apples

    def border_matrix(self):
        for i in range(self.__dimension + 2):
            self.__board[i][0] = '+'
            self.__board[i][self.__dimension + 1] = '+'
            self.__board[0][i] = '+'
            self.__board[self.__dimension + 1][i] = '+'

    def initialize_snake(self):
        center = self.__dimension // 2 + 1
        self.__board[center - 1][center] = '*'
        self.__board[center][center] = '+'
        self.__board[center + 1][center] = '+'
        return center

    def neighbors_not_apples(self, i, j):
        if self.__board[i + 1][j] == '.':
            return 0
        if self.__board[i - 1][j] == '.':
            return 0
        if self.__board[i][j + 1] == '.':
            return 0
        if self.__board[i][j - 1] == '.':
            return 0
        return 1

    def possible_apple_spots(self):
        spots = []
        for i in range(1, self.__dimension + 1):
            for j in range(1, self.__dimension + 1):
                if self.__board[i][j] == ' ' and self.neighbors_not_apples(i, j):
                    spots.append([i, j])
        return spots

    def place_apple(self, i, j):
        self.__board[i][j] = '.'
        self.__apples.append([i, j])

    def initialize_apples(self):
        apples_to_add = self.__apple_count
        spots = self.possible_apple_spots()
        while spots != [] and apples_to_add != 0:
            coords = spots[randint(0, len(spots) - 1)]
            self.place_apple(coords[0], coords[1])
            apples_to_add -= 1
            spots = self.possible_apple_spots()
        return self.__apple_count - apples_to_add

    def __str__(self):
        table = texttable.Texttable()
        for i in range(1, self.__dimension + 1):
            table.add_row(self.__board[i][1:self.__dimension + 1])
        return table.draw()


class GameOverError(Exception):
    def __init__(self, msg):
        self.__msg = msg


class InvalidMove(Exception):
    def __init__(self, msg):
        self.__msg = msg
