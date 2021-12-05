import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task
    numbers_called = [int(v) for v in values[0].split(",")]
    boards = [
        [[int(n) for n in v.split()] for v in values[i : i + 5]]
        for i in range(2, len(values), 6)
    ]

    # Identify the columns
    for board in boards:
        board += [[b[i] for b in board] for i in range(5)]

    # Loop through the play
    winner = -1
    for current_number in numbers_called:
        for i, board in enumerate(boards):
            boards[i] = [[j for j in b if j != current_number] for b in board]
            if any(len(b) == 0 for b in boards[i]):
                winner = i
                break
        if winner >= 0:
            break

    # Get the number on the unmarked board
    unmarked = sum(sum(b) for b in boards[winner]) / 2

    # Calculate the answer
    answer = int(unmarked * current_number)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task
    numbers_called = [int(v) for v in values[0].split(",")]
    boards = [
        [[int(n) for n in v.split()] for v in values[i : i + 5]]
        for i in range(2, len(values), 6)
    ]

    # Identify the columns
    for board in boards:
        board += [[b[i] for b in board] for i in range(5)]

    # Loop through the play
    boards_playing = [i for i in range(len(boards))]
    for current_number in numbers_called:
        # Loop through the boards
        for i, board in enumerate(boards):
            # If there is only 1 board left in play, that's the lose
            if len(boards_playing) == 1:
                loser = boards_playing[0]
            # Remove the 'called' number
            boards[i] = [[j for j in b if j != current_number] for b in board]
            # If that board has now lost, remove it from play
            if any(len(b) == 0 for b in boards[i]):
                boards_playing = [b for b in boards_playing if b != i]
                # If there are no boards left, stop playing
                if len(boards_playing) == 0:
                    break
        if len(boards_playing) == 0:
            break

    # Get the number on the unmarked board
    unmarked = sum(sum(b) for b in boards[loser]) / 2
    # Calculate the answer
    answer = int(unmarked * current_number)

    # Print out the response
    print(f"Task 2 Answer: {answer}")


if __name__ == "__main__":

    """Run using e.g.
    `python day-1.py -test`
    `python day-1.py`
    `python day-1.py -test -2`
    `python day-1.py -2`
    `python day-1.py -test -both`
    `python day-1.py -both`"""

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
