import random
import numpy as np
import matplotlib.pyplot as plt
from menace import SimpleMENACE

# reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Tic-Tac-Toe helper functions
def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in wins:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "draw"
    return None

def random_opponent_move(board):
    legal = [i for i,v in enumerate(board) if v == " "]
    return random.choice(legal)

# play_game must accept choose_move returning stage
def play_game(agent, estimated_length=9):
    board = [" "] * 9
    game_history = []
    move_no = 0

    while True:
        # MENACE plays X
        move_no += 1
        move, canonical, stage = agent.choose_move(board, move_no, estimated_length)
        game_history.append((canonical, move, stage))
        board[move] = "X"

        result = check_winner(board)
        if result is not None:
            if result == "X":
                agent.update_beads(game_history, "win")
                return "win"
            elif result == "draw":
                agent.update_beads(game_history, "draw")
                return "draw"

        # Opponent plays O (random)
        opp = random_opponent_move(board)
        board[opp] = "O"

        result = check_winner(board)
        if result is not None:
            if result == "O":
                agent.update_beads(game_history, "loss")
                return "loss"
            else:
                agent.update_beads(game_history, "draw")
                return "draw"

def train_menace(games=2000, log_every=200, save_plot=True):
    agent = SimpleMENACE()
    results = {"win":0, "loss":0, "draw":0}
    wins_history = []
    draws_history = []
    losses_history = []

    for g in range(games):
        r = play_game(agent)
        results[r] += 1

        if (g+1) % log_every == 0:
            wins_history.append(results['win'])
            draws_history.append(results['draw'])
            losses_history.append(results['loss'])
            print(f"After {g+1} games → Wins: {results['win']}, Draws: {results['draw']}, Losses: {results['loss']}")

    print("\nFinal Results:")
    print(results)

    # save model and plots
    agent.save("matchboxes_final.json")
    if save_plot:
        x = np.arange(log_every, games+1, log_every)
        plt.figure()
        plt.plot(x, wins_history, label="Wins")
        plt.plot(x, draws_history, label="Draws")
        plt.plot(x, losses_history, label="Losses")
        plt.xlabel("Games")
        plt.ylabel("Cumulative count")
        plt.title("MENACE training progress")
        plt.legend()
        plt.savefig("menace_training.png")
        plt.close()

    return agent, results

if __name__ == "__main__":
    agent, stats = train_menace(games=2000, log_every=200)
