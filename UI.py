from domain import GameOverError, InvalidMove


class UI:

    def __init__(self, service):
        self.__service = service

    @staticmethod
    def welcome_message():
        print("\nWelcome to Snake!")

    @staticmethod
    def bye_message():
        print("You've lost! Bye!")

    def initialize_command_dict(self):
        command_dict = {"left": self.left_ui, "right": self.right_ui, "up": self.up_ui, "down": self.down_ui,
                        "move": self.move_ui}
        return command_dict

    @staticmethod
    def read_line():
        line = input("> ")
        return line

    @staticmethod
    def format_line(line):
        line = line.strip().lower()
        return line

    @staticmethod
    def break_line(line, command_dict):
        tokens = line.split()
        for i in range(len(tokens)):
            if tokens[i] == "":
                tokens.pop(i)
        if tokens[0] not in command_dict:  # If the line is empty, raises IndexError that we catch.
            raise ValueError
        return tokens

    @staticmethod
    def invalid_command_ui():
        print("""The command does not exist, the only available commands are: left | right | up | down| move <int>""")

    def start(self):
        self.welcome_message()
        if not self.__service.added_all_apples:
            print("Could not add the whole amount of apples in the setting.properties file!")
        command_dict = self.initialize_command_dict()
        done = False
        while not done:
            print(self.__service.printable_board())
            line = self.read_line()
            line = self.format_line(line)
            try:
                words = self.break_line(line, command_dict)
            except ValueError:
                self.invalid_command_ui()
            except IndexError:  # This means that we inputted an empty line (see function break_line)
                pass  # We use pass here so when we input \n, we go to a new line with nothing happening
            else:
                command = words[0]
                arguments = []
                for i in range(1, len(words)):
                    arguments.append(words[i])
                try:
                    if command != "move":
                        command_dict[command]()
                    else:
                        command_dict[command](arguments)
                except GameOverError:
                    done = True
                except InvalidMove:
                    print("Invalid move, snake cannot go 180 degrees!")

        self.bye_message()

    def left_ui(self):
        self.__service.move('l')

    def right_ui(self):
        self.__service.move('r')

    def up_ui(self):
        self.__service.move('u')

    def down_ui(self):
        self.__service.move('d')

    def move_ui(self, times):
        if not times:
            times.append('1')
        self.__service.move(None, int(times[0]))
