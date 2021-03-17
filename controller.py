from domain import GameOverError, InvalidMove
from random import randint


class Service:
    def __init__(self, board):
        self.__board = board
        self.__last_move = 'u'
        self.__added_all_apples = self.__board.added_all_apples

    @property
    def board(self):
        return self.__board

    @property
    def added_all_apples(self):
        return self.__added_all_apples

    def compute_destination(self, direction):
        tokens = self.__board.head
        destination = None
        if direction == 'r':
            destination = [tokens[0], tokens[1] + 1]
        if direction == 'l':
            destination = [tokens[0], tokens[1] - 1]
        if direction == 'u':
            destination = [tokens[0] - 1, tokens[1]]
        if direction == 'd':
            destination = [tokens[0] + 1, tokens[1]]
        return destination

    def invalid_move(self, direction):
        if self.__last_move == 'r' and direction == 'l':
            return 1
        if self.__last_move == 'l' and direction == 'r':
            return 1
        if self.__last_move == 'u' and direction == 'd':
            return 1
        if self.__last_move == 'd' and direction == 'u':
            return 1
        return 0

    def move(self, direction, times=1):
        if direction is None:
            direction = self.__last_move
        while times != 0:
            if self.invalid_move(direction):
                raise InvalidMove("Can't move in that direction")
            else:
                destination = self.compute_destination(direction)
                self.__last_move = direction
                if destination != self.__board.tail and self.__board[destination] == '+':
                    raise GameOverError("Game over!")
                else:
                    add_apple = False
                    if self.__board[destination] == '.':
                        add_apple = True
                    self.move_snake(destination, add_apple)
            times -= 1

    def move_snake(self, destination, apples_to_add):
        tail = self.__board.pop_tail()
        head = self.__board.head
        self.__board[tail] = ' '
        self.__board[head] = '+'
        self.__board.push_head(destination)
        self.__board[destination] = '*'
        if apples_to_add:
            self.__board.push_tail(tail)
            self.__board[tail] = '+'
            self.__board.pop_apple(destination)
            spots = self.__board.possible_apple_spots()
            if len(spots) != 0:
                coords = spots[randint(0, len(spots) - 1)]
                self.__board.place_apple(coords[0], coords[1])

    def printable_board(self):
        return str(self.__board)
