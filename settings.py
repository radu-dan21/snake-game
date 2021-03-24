class Settings:
    """
        Class that reads and validates input from the setting.properties file.
    """

    @staticmethod
    def check_input(dimension_string, apple_count_string):
        """
            Checks if the settings file contains valid input. In case it does, it converts the input into the
        corresponding data type and returns it. In case it doesn't, raises exceptions.
        :param dimension_string: The dimension of the game board
        :type dimension_string: string
        :param apple_count_string: The number of apples at the start of the game
        :type apple_count_string: string
        :return: The parameters received (as strings), converted to appropriate data types
        :rtype: Tuple
        """
        try:
            dimension = int(dimension_string)
        except ValueError:
            raise DimensionError("Dimension must be a natural odd number >= 3")

        try:
            apple_count = int(apple_count_string)
        except ValueError:
            raise AppleError("The number of apples must be a natural number >= 1")

        if dimension < 3 or dimension % 2 == 0:
            raise DimensionError("Dimension must be a natural odd number >= 3")

        if apple_count < 1:
            raise AppleError("The number of apples must be a natural number >= 1")

        return dimension, apple_count

    def read_file(self):
        """
            Reads the settings file, passes data to another method for checking.
        :return: Returns the parameters read from the settings file, if they are valid (the method called in the return
        statement (check_input()) raises exceptions if the input is invalid
        :rtype: Tuple
        """

        infile = open("setting.properties", "r")

        line = infile.readline()
        index = line.find('=') + 1
        dimension_string = line[index:].strip()

        line = infile.readline()
        index = line.find('=') + 1
        apple_count_string = line[index:].strip()

        infile.close()

        return self.check_input(dimension_string, apple_count_string)


class AppleError(Exception):
    """
        Custom exception class.
    """
    def __init__(self, msg):
        self.__msg = msg


class DimensionError(Exception):
    """
        Custom exception class.
    """
    def __init__(self, msg):
        self.__msg = msg
