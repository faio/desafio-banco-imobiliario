from src.board import Board


def start():

    for i in range(0, 300):
        board = Board()
        board.play()


if __name__ == '__main__':
    start()
