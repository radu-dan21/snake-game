from domain import GameOverError, InvalidDirection


class UI:

    def __init__(self, service):
        self.__service = service

    def welcome_message(self):
        print("\nWelcome to Snake! Eat apples and do not bite yourself or the wall!\nBy eating an apple, the snake will"
              " grow by one cell!")
        print("\n\t- apples = '.'\n\t- snake's head = '*'\n\t- snake's body = '+'\n")
        print("\nThe list of available commands is:\n\t- move <n>\n\t* moves the snake n squares in the direction it is"
              " currently facing\n\t* move with no parameter moves the snake 1 square\n")
        print("\n\t- up | down | left | right\n\t* changes the direction the snake is currently facing\n"
              "\t* the direction cannot be changed by 180 degrees (ex. command down when the snake is facing up)\n")
        print("\n\t- exit\n\t* exits the program\n")
        not_added_apples = self.__service.apples_not_added()
        apples_added = self.__service.number_of_apples()
        if not_added_apples:
            print("\nCould not add " + str(apples_added + not_added_apples) + " apples")
            print("Only " + str(apples_added) + " apples were added\n")
        else:
            print("\nAll " + str(apples_added) + " apples were added successfully\n")

    @staticmethod
    def bye_message():
        print("Game Over! Bye!")

    def initialize_command_dict(self):
        command_dict = {"left": self.direction_ui, "right": self.direction_ui, "up": self.direction_ui,
                        "down": self.direction_ui, "move": self.move_ui, "exit": self.exit_ui}
        return command_dict

    @staticmethod
    def read_line():
        line = input("Please enter a command > ")
        return line.strip().lower()

    @staticmethod
    def break_line(line, command_dict):
        tokens = line.split()
        for i in range(len(tokens)):
            if tokens[i] == "":
                tokens.pop(i)
        if tokens[0] not in command_dict:  # if the line is empty, raises IndexError that we catch.
            raise ValueError
        return tokens

    @staticmethod
    def invalid_command_ui():
        print("The command does not exist\n")
        print("The only available commands are: left | right | up | down | move <int> | exit\n")

    def print_board(self):
        print("Snake is currently facing:", str(self.__service.direction))
        print(self.__service.printable_board())

    def start(self):

        self.welcome_message()
        command_dict = self.initialize_command_dict()

        done = False
        while not done:
            self.print_board()
            line = self.read_line()
            try:
                arguments = self.break_line(line, command_dict)
            except ValueError:
                self.invalid_command_ui()
            except IndexError:  # This means that we inputted an empty line (see function break_line)
                pass  # We use pass here so when we input \n, we go to a new line with nothing happening
            else:
                try:
                    command_dict[arguments[0]](arguments)
                except GameOverError:
                    done = True
        self.bye_message()

    def direction_ui(self, arguments):
        if len(arguments) != 1:
            self.invalid_command_ui()
        else:
            # arguments[0] represents the command, arguments[0][0] represents the first character of the command
            #   u - up
            #   d -down
            #   l - left
            #   r - right
            try:
                self.__service.change_direction(arguments[0][0])
            except InvalidDirection as i_dir:
                print(i_dir)

    def move_ui(self, arguments):
        if len(arguments) == 1:
            self.__service.move()
        else:
            if len(arguments) > 2:
                self.invalid_command_ui()
            else:
                try:
                    times = int(arguments[1])
                    if times <= 0:
                        raise ValueError
                    self.__service.move(times)
                except ValueError:
                    self.invalid_command_ui()

    def exit_ui(self, arguments):
        if len(arguments) != 1:
            self.invalid_command_ui()
        else:
            raise GameOverError
