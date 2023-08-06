from unda import UndaClient, UndaObject, LOGGER


class Skateboard:

    def __init__(self, name):
        self.name = name
        self.moving = False

    def start_skating(self):
        self.moving = True
        print('Time to grind!')

board = Skateboard('Varial')  # Just a skateboard named Varial.
client = UndaClient(board)
client.update()
print(client.undo_stack)
board.start_skating()
client.undo(inplace=True)
print(board.moving)