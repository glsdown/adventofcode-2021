import re
import sys
from collections import Counter
from copy import deepcopy

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def get_data():

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Convert the image to binary values
    # light pixels (# / 1)
    # dark pixels (. / 0)
    values = [i.replace("#", "1").replace(".", "0") for i in values]

    # Get the two sections
    algorithm = values[0]
    image = [list(i) for i in values[2:]]

    return algorithm, image


def enhance_image(image, algorithm, number_turns=2):

    # Get the extra 'edges' to add each time
    extra_edges = 2

    for turn in range(number_turns):

        # My algorithm flips grids of all 0s to grids of all 1s
        replacement = algorithm[(turn + 1) % 2]
        other = algorithm[turn % 2]

        # Create a new 'blank' grid, with the 'extra' dark values around
        # the edges
        new_grid = [
            list(other * (len(image[0]) + (2 * extra_edges)))
            for _ in range(len(image) + (2 * extra_edges))
        ]

        # Add the blank edges to the original grid
        image = (
            [
                list(replacement * (len(image[0]) + (2 * extra_edges)))
                for i in range(extra_edges)
            ]
            + [
                list(replacement * extra_edges)
                + i
                + list(replacement * extra_edges)
                for i in image
            ]
            + [
                list(replacement * (len(image[0]) + (2 * extra_edges)))
                for i in range(extra_edges)
            ]
        )

        # Loop through each pixel in the grid
        for row in range(1, len(image) - 1):
            for col in range(1, len(image[0]) - 1):

                # Get the grid
                grid = "".join(
                    [
                        image[row + i][col - 1]
                        + image[row + i][col]
                        + image[row + i][col + 1]
                        for i in [-1, 0, 1]
                    ]
                )

                # Get the pixel value
                pixel_value = int(grid, 2)

                # Create the new grid
                new_grid[row][col] = algorithm[pixel_value]

        # Copy the new grid to the image
        image = deepcopy(new_grid)

    # Get the number of 'light' pixels
    return sum([Counter(i)["1"] for i in image])


def part_1(path):
    """Part 1/Star 1"""

    # Load the data
    algorithm, image = get_data()

    # Get th enumber of light pixels
    answer = enhance_image(image, algorithm, 2)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Load the data
    algorithm, image = get_data()

    # Get th enumber of light pixels
    answer = enhance_image(image, algorithm, 50)

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
