import re
import sys
from copy import deepcopy
from cachetools import cached

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Get the starting positions
    players = [
        {"position": int(i.split(":")[1].strip()) - 1, "score": 0}
        for i in values
    ]

    # create the deterministic 100-sided die
    die = 1

    # Keep track of the number of die rolls
    number_rolls = 0

    # Start with the first player
    turn = 0

    while True:

        # Player plays
        move = 0
        for _ in range(3):
            move += die
            die += 1

        # Increase the number of die rolls
        number_rolls += 3

        # Add the move to the score
        players[turn]["position"] = (players[turn]["position"] + move) % 10
        players[turn]["score"] += players[turn]["position"] + 1

        # Check for win
        if players[turn]["score"] >= 1000:
            break

        # Swap the turn
        turn = int(not turn)

    # Get the losing player score
    losing = players[(turn + 1) % 2]["score"]

    # Calculate the final result
    answer = losing * number_rolls

    # Print out the response
    print(f"Task 1 Answer: {answer}")


@cached(cache={})
def play_game(current_player, positions, scores):

    # Check for win
    if scores[current_player] >= 21:
        if current_player == 0:
            return (1, 0)
        return (0, 1)

    # Swap the current_player
    current_player = int(not current_player)

    # Need to work out the 'multiplier'
    # i.e. there is 1 way of getting a 3 or a 9,
    # but there are 3 ways of getting a 4 or an 8
    # 6 ways of getting a 5 or a 7 and 7 ways of getting a 6
    options = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    wins = (0, 0)

    # Get the wins for each possible outcome
    for move, multiplier in options.items():

        # Change the current players' position
        new_position = (positions[current_player] + move) % 10
        if current_player == 0:
            tmp_positions = (new_position, positions[1])
        else:
            tmp_positions = (positions[0], new_position)

        # Add the move to the score
        new_score = scores[current_player] + tmp_positions[current_player] + 1
        if current_player == 0:
            tmp_scores = (new_score, scores[1])
        else:
            tmp_scores = (scores[0], new_score)

        # Keep going with this game to see how many wins there are
        tmp_wins = play_game(
            current_player=current_player,
            positions=tmp_positions,
            scores=tmp_scores,
        )

        # Add to the current tally
        wins = tuple(tmp_wins[i] * multiplier + wins[i] for i in [0, 1])

    return wins


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Get the starting positions
    positions = tuple(int(i.split(":")[1].strip()) - 1 for i in values)

    # Play the game
    # current_player starts with 1 to ensure that player 0 plays first
    wins = play_game(current_player=1, positions=positions, scores=(0, 0))

    # Get the max win
    answer = max(wins)

    # Print out the response
    print(f"Task 2 Answer: {answer}")


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-1.py -test`
        `python day-1.py`
        `python day-1.py -test -2`
        `python day-1.py -2`
        `python day-1.py -test -both`
        `python day-1.py -both`
    """

    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"

    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path)
    elif "-both" in sys.argv:
        part_1(path)
        part_2(path)
    else:
        part_1(path)
