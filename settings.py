class Settings:

    def __init__(self):
        self.__infile = open("setting.properties", "r")

    def read_file(self):
        line = self.__infile.readline()
        index = line.find('=') + 1
        try:
            dimension = int(line[index:].strip())
        except ValueError:
            raise DimensionError("Dimension must be a natural odd number >= 3")
        line = self.__infile.readline()
        index = line.find('=') + 1
        try:
            apple_count = int(line[index:].strip())
        except ValueError:
            raise AppleError("The number of apples must be a natural number >= 1")
        if dimension < 3 or dimension % 2 == 0:
            raise DimensionError("Dimension must be a natural odd number >= 3")
        if apple_count < 1:
            raise AppleError("The number of apples must be a natural number >= 1")
        return dimension, apple_count


class AppleError(Exception):
    def __init__(self, msg):
        self.__msg = msg


class DimensionError(Exception):
    def __init__(self, msg):
        self.__msg = msg
