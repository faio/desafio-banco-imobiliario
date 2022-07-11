from src.board import Board
from collections import Counter

QT_SIMULATION = 300


def start():
    boards = list()
    for i in range(0, QT_SIMULATION):
        board = Board()
        board.play()
        boards.append(board)

    timeouts = 0
    rounds = 0
    winners = list()
    for board in boards:
        # Quantas partidas terminam por time out (1000 rodadas);
        if board.current_round == board.MAX_ROUND:
            timeouts += 1

        # Quantos turnos em média demora uma partida;
        rounds += board.current_round

        # Qual a porcentagem de vitórias por comportamento dos jogadores;
        winners.append(board.winner)

    # ------------ Gerando as estatisticas do jogo -------------------
    counter_winners = Counter([w._strategy for w in winners])
    more_winners = counter_winners.most_common(1)[0]

    print(f"Quantidade de simulações: {QT_SIMULATION}")
    print(f"Partidas encerradas com timeout: {timeouts}")
    print(f"Quantidade de turnos em media: {round(rounds / board.MAX_ROUND)}")
    print(f"Quem mais venceu foi o: {more_winners[0].title()} com {more_winners[1]} vitórias")
    print("Porcentagem de vitórias por comportamento dos jogadores:")

    for key, value in counter_winners.most_common():
        print(f"\t{key.title()}: { (value / QT_SIMULATION) * 100 : .2f} %")
