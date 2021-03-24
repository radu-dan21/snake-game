from domain import GameOverError, InvalidDirection
from random import randint


class Service:
    """
        Class that implements more complex operations like moving the snake or changing directions.
    """

    def __init__(self, board):
        """
            Creates a field for a game board and sets the snake's direction to 'u' (meaning up).
        :param board: (new) game board
        :type board: Board
        """
        self.__board = board
        self.__direction = "u"

    def board(self):
        return self.__board

    @property
    def direction(self):
        return self.__direction

    def number_of_apples(self):
        return self.__board.number_of_apples

    def apples_not_added(self):
        return self.__board.get_apple_difference

    def change_direction(self, new_direction):
        """
            Checks if the direction can be changed to the one specified by the user. Changes it if possible, raises
        InvalidDirection if not.
        :param new_direction: 'u', 'd', 'l', or 'r'
        :type new_direction: character
        """
        if self.__direction == 'r' and new_direction == 'l':
            raise InvalidDirection("\nSnake cannot turn 180 degrees!\n")
        if self.__direction == 'l' and new_direction == 'r':
            raise InvalidDirection("\nSnake cannot turn 180 degrees!\n")
        if self.__direction == 'u' and new_direction == 'd':
            raise InvalidDirection("\nSnake cannot turn 180 degrees!\n")
        if self.__direction == 'd' and new_direction == 'u':
            raise InvalidDirection("\nSnake cannot turn 180 degrees!\n")
        self.__direction = new_direction

    def compute_destination(self):
        """
            Computes the coordinates where the snake's head will be after the move is executed, based on the current
        direction of the snake
        :return: Coordinates i, j (head will be placed at board[i][j]), None if there is an invalid direction
        :rtype: List with 2 elements or None
        """
        tokens = self.__board.head
        if self.__direction == 'r':
            return [tokens[0], tokens[1] + 1]
        if self.__direction == 'l':
            return [tokens[0], tokens[1] - 1]
        if self.__direction == 'u':
            return [tokens[0] - 1, tokens[1]]
        if self.__direction == 'd':
            return [tokens[0] + 1, tokens[1]]
        return None

    def move(self, times=1):
        """
            Computes the destination of the snake, checks if there is an apple that will be eaten, and calls a method
        to actually move the snake
        :param times: represents how many squares should the snake move in the current direction
        :type times: int >= 1
        """
        while times != 0:
            destination = self.compute_destination()
            # Snake cannot eat it's own tail because when it moves to eat it, the tail also moves 1 square
            if destination != self.__board.tail and self.__board[destination] == '+':
                raise GameOverError("Game over!")
            add_apple = False
            if self.__board[destination] == '.':
                add_apple = True
            self.move_snake(destination, add_apple)
            times -= 1

    def move_snake(self, destination, apples_to_add):
        """
            Moves the snake to the specified destination, makes the snake grow larger by 1 square if needed (if the
        destination square has an apple on it).

            Because every part of the snake moves 1 square accordingly and takes the place of the previous part that was
        there (the exceptions are the head and the tail), moving the snake can be implemented like this:
                -> Pop the snake's tail
                -> Push the new head in the snake array (The old head becomes the new 'neck')
                -> If an apple is eaten, put the tail back in its place, pop the apple from the board, and put a new one
            at a random position
                    *(neck of the snake - the square directly after the snake's head)

        :param destination: The coordinate i, j of the new head (board[i][j])
        :type destination: List of 2 elements
        :param apples_to_add: Flag that tells the method if an apple was eaten or not
        :type apples_to_add: Bool
        """
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
