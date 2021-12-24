import re
import sys
from collections import defaultdict
from itertools import combinations
from math import comb, sqrt

import numpy as np

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def read_data():

    with open(f"{path}/day-{DAY}.txt", "r") as f:
        # Split on the empty line
        values = [i.split("\n") for i in f.read().split("\n\n")]
        # Create a dictionary of the scanners to the co-ordinates
        values = {
            re.match(r"\-\-\- scanner (\d+) \-\-\-", i[0]).groups()[0]: [
                tuple(int(j) for j in x.split(",")) for x in i[1:]
            ]
            for i in values
        }
    return values


def distance(point1, point2):
    """Get the distance between 2 3D points"""
    return sqrt(
        pow(point2[0] - point1[0], 2)
        + pow(point2[1] - point1[1], 2)
        + pow(point2[2] - point1[2], 2)
    )


def manhattan_distance(point1, point2):
    """Get the manhattan distance between two points"""

    return sum(abs(point1[i] - point2[i]) for i in range(3))


def get_all_distances(values):
    """Get all pairs of distances"""

    scanner_distances = {}

    # Get the distances between all points for each scanner, for each beacon
    for scanner, beacons in values.items():
        # Create empty list of the distances
        distances = defaultdict(list)

        # Calculate distance between all pairs of points
        for b1, b2 in combinations(beacons, 2):
            dist = distance(b1, b2)
            distances[b1].append(dist)
            distances[b2].append(dist)

        # Record all possible distances between points
        scanner_distances[scanner] = dict(distances)

    return scanner_distances


def get_common_locations(scanner_distances, number_scanners):
    """Create a dictionary showing the scanners with common points"""

    # Find how many distances there are in common between beacons in each
    # scanner to work out the beacons in common
    common = {}

    # Add the first 'known' scanner
    locations = {
        "0": {
            "start": (0, 0, 0),
            "axis_order": ["x", "y", "z"],
            "flip": [1, 1, 1],
        }
    }
    seen_scanners = set(["0"])
    s1 = "0"

    # Keep going until all scanners have been found
    while len(seen_scanners) < number_scanners:

        for s2 in scanner_distances.keys():

            # Don't end up in a loop
            if s2 in seen_scanners:
                continue

            # Create empty list of the distances
            common_beacons = []

            # Flag to stop it checking the pairs once it's found the 12
            found = False
            for b1, d1 in scanner_distances[s1].items():
                for b2, d2 in scanner_distances[s2].items():
                    # If there are at least 11 distances in common
                    if len(set(d1).intersection(set(d2))) >= 11:
                        # Then the beacon is common between the two scanners
                        common_beacons.append((b1, b2))
                        # If there are at least 12 common beacons, then we say
                        # the scanners overlap, and we stop checking this pair
                        if len(common_beacons) >= 12:
                            common[(s1, s2)] = common_beacons
                            found = True
                            break
                # Stop checking this pair
                if found:
                    break

            # If they don't have common beacons, look at the next sensor
            if not found:
                continue

            # Now find out the relative position of s2 from s1

            # Firstly, need to work out which co-ordinates are the 'same'
            # common_beacons is of the form:
            # [
            #   ((404, -588, -901), (-336, 658, 858)),
            #   ((528, -643, 409), (-460, 603, -452)),
            #   ((390, -675, -793), (-322, 571, 750)),
            # ]
            # Want to find the pattern and work out which are 'flipped' and
            # translated

            # Look at the differences in the pattern to identify which
            # co-ordinate is which relative to the start sensor
            b1 = [i[0] for i in common_beacons]
            b2 = [i[1] for i in common_beacons]

            # Get the differences
            d1 = [np.diff([i[j] for i in b1]) for j in range(3)]
            d2 = [np.diff([i[j] for i in b2]) for j in range(3)]

            # Identify which is which
            axis_order = [None, None, None]
            flip = [1, 1, 1]

            known_start = locations[s1]["start"]
            known_axis_order = locations[s1]["axis_order"]
            known_flip = locations[s1]["flip"]

            # Loop through each 'known' option
            for option, axis in enumerate(d1):
                # Work out the 'arrangement' for the 'known' scanner
                this_axis = known_axis_order[option]
                this_flip = known_flip[option]

                # Look at each possible option to determine the layout of the
                # 'unknown' scanner
                for i in range(3):
                    # If this axis is identical, then it's clearly the same
                    if list(axis) == list(d2[i]):
                        axis_order[i] = this_axis
                        flip[i] = this_flip
                        break
                    # If it's the same value, but negative, it's flipped
                    elif list(axis) == [-x for x in d2[i]]:
                        axis_order[i] = this_axis
                        flip[i] = this_flip * -1
                        break

            # Now we know the order and 'flip' can compare the values to get the
            # start position
            point1 = [i * b for i, b in zip(known_flip, b1[0])]
            # Rearrange the axes
            point1 = (
                point1[known_axis_order.index("x")],
                point1[known_axis_order.index("y")],
                point1[known_axis_order.index("z")],
            )
            # Flip as required
            point2 = [i * b for i, b in zip(flip, b2[0])]
            # Rearrange the axes
            point2 = (
                point2[axis_order.index("x")],
                point2[axis_order.index("y")],
                point2[axis_order.index("z")],
            )

            # Use rules of vectors
            start = tuple(
                known_start[i] + point1[i] - point2[i] for i in range(3)
            )

            # Add to the known list
            locations[s2] = {
                "start": start,
                "axis_order": axis_order,
                "flip": flip,
            }

            # Look at the pair for this one
            s1 = s2
            seen_scanners.add(s2)

        # Couldn't find a pair, so try and find a different pair that we already know
        s1 = str((int(s1) + 1) % number_scanners)
        while s1 not in seen_scanners:
            s1 = str((int(s1) + 1) % number_scanners)

    return locations


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    values = read_data()
    # Get the number of scanners
    number_scanners = len(values.keys())

    # Get the distances between the beacons
    scanner_distances = get_all_distances(values)

    # Get the details about each scanner
    locations = get_common_locations(scanner_distances, number_scanners)

    # Now need to get a full list of the beacons
    all_beacons = set()
    for scanner, beacons in values.items():
        known_start = locations[scanner]["start"]
        known_axis_order = locations[scanner]["axis_order"]
        known_flip = locations[scanner]["flip"]

        for beacon in beacons:
            # Now we know the order, 'flip' and start, can get the actual
            # position

            # Flip as required
            point = [i * b for i, b in zip(known_flip, beacon)]
            # Rearrange the axes
            point = [
                point[known_axis_order.index("x")],
                point[known_axis_order.index("y")],
                point[known_axis_order.index("z")],
            ]

            # Add to the start
            all_beacons.add(tuple(point[i] + known_start[i] for i in range(3)))

    # Print out the response
    print(f"Task 1 Answer: {len(all_beacons)}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    values = read_data()
    # Get the number of scanners
    number_scanners = len(values.keys())

    # Get the distances between the beacons
    scanner_distances = get_all_distances(values)

    # Get the details about each scanner
    locations = get_common_locations(scanner_distances, number_scanners)

    # Get all the start points
    start_points = [locations[i]["start"] for i in locations.keys()]

    answer = 0
    for p1, p2 in combinations(start_points, 2):
        answer = max([manhattan_distance(p1, p2), answer])

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
