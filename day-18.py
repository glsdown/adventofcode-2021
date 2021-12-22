import re
import sys
from copy import deepcopy
from itertools import permutations

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


class SnailfishNumber:
    def __init__(self, side=None, value=None, parent=None):

        self.side = side  # "left" or "right"
        self.parent = parent
        self.value = value  # Could be a number or 2 children

    def __repr__(self):

        if isinstance(self.value, int):
            return f"{self.value}"
        else:
            return f"[{self.value['left']},{self.value['right']}]"

    def __add__(self, other):
        """Add two SnailfishNumbers together"""

        # Copy the two values to add
        left = deepcopy(self)
        right = deepcopy(other)

        # Create the new number
        addition = SnailfishNumber(value={"left": left, "right": right})

        # Add the 'side's to each side
        left.side = "left"
        right.side = "right"

        # Add the new parent
        left.parent = addition
        right.parent = addition

        # Return the addition value
        return addition

    def get_level(self):
        """Find out how many parents it has (i.e. the 'level')"""
        counter = 1
        parent = self.parent
        while parent.parent is not None:
            counter += 1
            parent = parent.parent
        return counter

    def magnitude(self):
        """
        The magnitude of a pair is 3 times the magnitude of its left element
        plus 2 times the magnitude of its right element. The magnitude of a
        regular number is just that number.
        """
        if isinstance(self.value, int):
            return self.value

        return (
            3 * self.value["left"].magnitude()
            + 2 * self.value["right"].magnitude()
        )


def add_left_or_right_most(snailfish_number, value_to_add, side):
    # Get the current value
    current = snailfish_number

    # Find the parent
    ancestor = snailfish_number.parent

    # Loop through all the parents
    while ancestor is not None:
        # If the value to be added is the left/right-most already...
        if current.side == side:
            # Check the parent level instead
            ancestor = ancestor.parent
            current = current.parent
        else:
            # Get the opposite side
            if side == "left":
                opposite = "right"
            else:
                opposite = "left"

            # Otherwise, travel down the required hand side
            node = ancestor.value[side]
            # Keep travelling down the opposite hand branch until we get
            # a number
            while not isinstance(node.value, int):
                node = node.value[opposite]
            # Add the addition number to the number
            node.value += value_to_add
            # Stop looping as reached the 'left/right-most' number
            break


def explode_number(snailfish_number):
    """
    To explode a pair, the pair's left value is added to the first regular
    number to the left of the exploding pair (if any), and the pair's right
    value is added to the first regular number to the right of the exploding
    pair (if any). Exploding pairs will always consist of two regular numbers.
    Then, the entire exploding pair is replaced with the regular number 0.
    """

    # If it's nothing, then flag it
    if isinstance(snailfish_number.value, int):
        return False
    # Check if it's a terminal pair
    elif (
        isinstance(snailfish_number.value, dict)
        and isinstance(snailfish_number.value["left"].value, int)
    ) and (
        isinstance(snailfish_number.value, dict)
        and isinstance(snailfish_number.value["right"].value, int)
    ):
        # Check that the depth is greater than 4
        if snailfish_number.get_level() >= 4:
            # Get the left and right children
            left, right = (
                snailfish_number.value["left"].value,
                snailfish_number.value["right"].value,
            )
            # Explode the number
            add_left_or_right_most(
                snailfish_number, value_to_add=left, side="left"
            )
            add_left_or_right_most(
                snailfish_number, value_to_add=right, side="right"
            )

            # Set the value to 0
            snailfish_number.value = 0

            # Mark that it has exploded
            return True
        # Mark that it hasn't exploded
        return False

    # Explode the children
    return explode_number(snailfish_number.value["left"]) or explode_number(
        snailfish_number.value["right"]
    )


def split_number(snailfish_number):
    """
    To split a regular number, replace it with a pair; the left element
    of the pair should be the regular number divided by two and rounded
    down, while the right element of the pair should be the regular number
    divided by two and rounded up. For example, 10 becomes [5,5], 11
    becomes [5,6], 12 becomes [6,6], and so on.
    """

    # If it's the bottom of the chain
    if isinstance(snailfish_number.value, int):
        # If the value is greater than 10
        if snailfish_number.value >= 10:
            # Split the value
            half = snailfish_number.value // 2
            snailfish_number.value = {
                "left": SnailfishNumber(
                    side="left",
                    value=half,
                    parent=snailfish_number,
                ),
                "right": SnailfishNumber(
                    side="right",
                    value=snailfish_number.value - half,
                    parent=snailfish_number,
                ),
            }
            return True
        # Number not split
        return False

    return split_number(snailfish_number.value["left"]) or split_number(
        snailfish_number.value["right"]
    )


def parse_snailfish_number(value, parent=None, side=None):
    """Parse a nested list of snailfish numbers"""

    # Base case
    if isinstance(value, int):
        return SnailfishNumber(side=side, value=value, parent=parent)

    # Nested case - create an 'empty' value to be the parent
    current = SnailfishNumber(side=side, parent=parent)

    # Identify the 'left' and 'right' sides
    left, right = value

    # Add the 'children' to the 'current' value
    current.value = {
        "left": parse_snailfish_number(
            value=left, side="left", parent=current
        ),
        "right": parse_snailfish_number(
            value=right, side="right", parent=current
        ),
    }

    # Return the newly created value
    return current


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [eval(line.strip()) for line in f.readlines()]

    # Get the first number
    answer = parse_snailfish_number(values[0])

    # Add each value to the answer
    for i in range(1, len(values)):

        # Create the new number
        new = parse_snailfish_number(values[i])

        # 'add' the two numbers
        answer += new

        # reduce the number
        while True:
            # Keep exploding/splitting as required
            if explode_number(answer) or split_number(answer):
                continue
            break

    # Print out the response
    print(f"Task 1 Answer: {answer.magnitude()}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            parse_snailfish_number(eval(line.strip()))
            for line in f.readlines()
        ]

    answer = 0

    # Loop through all possibilities
    for first, second in permutations(values, 2):

        # 'add' the two numbers
        sum_total = first + second

        # reduce the number
        while True:
            # Keep exploding/splitting as required
            if explode_number(sum_total) or split_number(sum_total):
                continue
            break

        # Get the max magnitude
        answer = max([answer, sum_total.magnitude()])

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


"""
[[[[[9,8],1],2],3],4]


                    |
                --------|
                |       4
            --------|
            |       3
        --------|
        |       2
    --------|
    |       1
|-------|
9       8

Explodes to:


                    |
                --------|
                |       4
            --------|
            |       3
        --------|
        |       2
    --------|
    0       9


[[6,[5,[4,[3,2]]]],1]

                    |
                --------|
                |       1
            |--------
            6       |
                |--------
                5       |
                    |--------
                    4       |
                        |-------|
                        3       2

explodes to

                    |
                --------|
                |       3
            |--------
            6       |
                |--------
                5       |
                    |--------
                    7       0



[[[[0,  [4,5]], [0,0]], 0], 1]
         ---
[[[[0+4, 0   ], [5,0]], 0], 1]

"""
