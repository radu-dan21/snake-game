from domain import Board
from controller import Service
from UI import UI
from settings import Settings


class Program:
    def __init__(self):
        self.__settings = Settings()
        tokens = self.__settings.read_file()
        self.__board = Board(tokens[0], tokens[1])
        self.__service = Service(self.__board)
        self.__UI = UI(self.__service)

    def start_program(self):
        self.__UI.start()


if __name__ == "__main__":
    program = Program()
    program.start_program()
