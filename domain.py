import texttable
from random import randint


class Board:
    """
        Class that implements the game board and the snake.
        The game board is implemented as an 2D character array and the snake is implemented as an array of lists.

             - one apple is represented by a '.'
             - the head of the snake is represented with a '*'
             - the body and tail of the snake are represented with '+'
             - empty spaces are represented with a ' '

        In order to lose, the snake must bite itself or a "wall" (basically getting out of the 2D array), so the game
    board is bordered with '+', which are not visible on the console.
    """

    def __init__(self, dimension, apple_count):
        """
            Method that initializes a game board based on the parameters read from the settings.properties file.
            If the number of apples from the file is greater than the number of apples we can add, the maximum number of
        apples will be added and an attribute of the class will be set to False (as opposed to True, the maximum number
        of apples can be added).

        :param dimension: odd natural number >= 3
        :type dimension: integer
        :param apple_count: natural number >= 1
        :type apple_count: integer
        """
        self.__apple_count = apple_count
        self.__dimension = dimension

        self.__board = [[' ' for i in range(dimension + 2)] for j in range(dimension + 2)]
        self.border_matrix()

        center = self.initialize_snake()
        self.__snake = [[center - 1, center], [center, center], [center + 1, center]]  # Snake initialized at the center

        self.__apples = []
        apples_added = self.initialize_apples()

        # if apple_difference is equal to 0 => all apples were added. Else, there were apple_difference apples not added
        self.__apple_difference = self.__apple_count - apples_added

        self.__apple_count = apples_added

    @property
    def board(self):
        """
            Getter for the matrix that represents the game board.
        :return: the game board
        :rtype: 2D array
        """
        return self.__board

    @property
    def head(self):
        """
            Getter for the snake's head.
        :return: pair of integers, representing a position in the 2D array
        :rtype: list
        """
        return self.__snake[0]

    @property
    def tail(self):
        """
            Getter for the snake's tail.
        :return: pair of integers, representing a position in the 2D array
        :rtype: list
        """
        return self.__snake[-1]

    @property
    def number_of_apples(self):
        """
        TODO
        :return:
        :rtype:
        """
        return self.__apple_count

    @property
    def apples(self):
        """
            Getter for the list of apples.
        :return: 1D array, that contains the list of the indices of the apples that are on the board
        :rtype: list
        """
        return self.__apples

    @property
    def get_apple_difference(self):
        """
            Getter for the apple difference (see __init__)
        :return: (number of apples that the user wanted to add) - (the number of apples that were added)
        :rtype: integer
        """
        return self.__apple_difference

    def pop_tail(self):
        """
            Removes the tail of the snake (last element from an array) and returns it.
        :return: list, 2 elements, representing 2 indices that give us the position of the snake's tail in the 2D array
        :rtype: list
        """
        return self.__snake.pop(-1)

    def push_head(self, new_head):
        """
            Inserts on the first position of the snake array, a new head.
        :param new_head: list, 2 elements, representing 2 indices that give us the position of the snake's new head
        :type new_head: list
        """
        self.__snake.insert(0, new_head)

    def push_tail(self, new_tail):
        """
            Inserts a new tail for the snake at the end of the 2D array.
        :param new_tail: list, 2 elements, representing 2 indices that give us the position of the snake's new tail
        :type new_tail: list
        """
        self.__snake.append(new_tail)

    def pop_apple(self, apple_to_pop):
        """
            Removes an apple from the apple list.
        :param apple_to_pop: list, 2 elements, representing 2 indices that give us the position of the apple
        :type apple_to_pop: list
        """
        for i in range(len(self.__apples)):
            if self.__apples[i] == apple_to_pop:
                print(self.__apples[i])
                self.__apples.pop(i)
                break

    def __getitem__(self, item):
        """
            Getter for an element from the 2D array.
        :param item: list, 2 elements, representing 2 indices that give us the position of an element from the 2D array
        :type item: list
        :return: Returns the element found with the 2 given indices
        :rtype: character
        """
        return self.__board[item[0]][item[1]]

    def __setitem__(self, key, value):
        """
            Setter for an element of the 2D array.
        :param key: a pair of integers, representing 2 indices that give us the position of the element we want to set
        :type key: list
        :param value: new value for the position specified as a parameter
        :type value: character
        """
        self.__board[key[0]][key[1]] = value

    def border_matrix(self):
        """
            Borders the game board with the character '+', reasoning explained in this class's specification.
        """
        for i in range(self.__dimension + 2):
            self.__board[i][0] = '+'
            self.__board[i][self.__dimension + 1] = '+'
            self.__board[0][i] = '+'
            self.__board[self.__dimension + 1][i] = '+'

    def initialize_snake(self):
        """
            "Initializes" a snake by modifying characters from the 2D array, such that there will be a '+' in the center
        of the board, a '+' under it, and a '*' over it.
        :return: one coordinate of the center of the board
        :rtype: integer
        """
        center = self.__dimension // 2 + 1
        self.__board[center - 1][center] = '*'
        self.__board[center][center] = '+'
        self.__board[center + 1][center] = '+'
        return center

    def neighbors_not_apples(self, i, j):
        """
            For a given position in the 2D array (given by i and j), checks if the neighbors of that element are apples.
        :param i: line coordinate
        :type i: integer
        :param j: column coordinate
        :type j: integer
        :return: True if the neighbors are not apples, False if at least one is
        :rtype:
        """
        if self.__board[i + 1][j] == '.':
            return False
        if self.__board[i - 1][j] == '.':
            return False
        if self.__board[i][j + 1] == '.':
            return False
        if self.__board[i][j - 1] == '.':
            return False
        return True

    def possible_apple_spots(self):
        """
            Computes the possible spots where apples can be place in the 2D array.
        :return: all places where apples can be put on the board, each given by a list [i, j]
        :rtype: list
        """
        spots = []
        for i in range(1, self.__dimension + 1):
            for j in range(1, self.__dimension + 1):
                if self.__board[i][j] == ' ' and self.neighbors_not_apples(i, j):
                    spots.append([i, j])
        return spots

    def place_apple(self, i, j):
        """
            Places an apple at a specified position, then adds the list of coordinates to the apples list.
        :param i: line coordinate
        :type i: integer
        :param j: column coordinate
        :type j: integer
        """
        self.__board[i][j] = '.'
        self.__apples.append([i, j])

    def initialize_apples(self):
        """
            Adds apples to the board, until the number of apples inputted by the user is reached or until there are no
        more places left for adding apples.
        :return: The difference between the user input and the number of apples added (ideally, this would be 0)
        :rtype: integer
        """
        apples_to_add = self.__apple_count
        spots = self.possible_apple_spots()
        while spots != [] and apples_to_add != 0:
            coords = spots[randint(0, len(spots) - 1)]
            self.place_apple(coords[0], coords[1])
            apples_to_add -= 1
            spots = self.possible_apple_spots()
        return self.__apple_count - apples_to_add

    def __str__(self):
        """
            Returns the string format of a board for printing, with the help of the texttable module.
        :return: string representation of the board
        :rtype: string
        """
        table = texttable.Texttable()
        for i in range(1, self.__dimension + 1):
            table.add_row(self.__board[i][1:self.__dimension + 1])
        return table.draw()


class GameOverError(Exception):
    """
        Custom exception class.
    """
    def __init__(self, msg=""):
        self.__msg = msg


class InvalidDirection(Exception):
    """
        Custom exception class.
    """
    def __init__(self, msg=""):
        self.__msg = msg
