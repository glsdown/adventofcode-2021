import re
import sys

import networkx as nx

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Create a graph
    G = nx.DiGraph()

    # Add the nodes and weighted edges
    number_rows = len(values)
    number_cols = len(values[0])
    for row in range(number_rows):
        for col in range(number_cols):
            # Add this node
            start = (col, row)
            start_risk = int(values[row][col])
            G.add_node(start)
            # Check the new node is on the graph
            if row + 1 < number_rows:
                new = (col, row + 1)
                G.add_node(new)
                risk = int(values[row + 1][col])
                G.add_weighted_edges_from(
                    [(start, new, risk), (new, start, start_risk)]
                )
            # Check the new node is on the graph
            if col + 1 < number_cols:
                new = (col + 1, row)
                G.add_node(new)
                risk = int(values[row][col + 1])
                G.add_weighted_edges_from(
                    [(start, new, risk), (new, start, start_risk)]
                )

    # Get the shortest path
    answer, _ = nx.bidirectional_dijkstra(
        G, (0, 0), (number_cols - 1, number_rows - 1)
    )

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    original_rows = len(values)

    def add_one_grid(grid, count=1):
        return [
            "".join([str((int(i) + (count - 1)) % 9 + 1) for i in v])
            for v in grid
        ]

    # Generate the large grid
    new_grid = [[values], *[[add_one_grid(values, i)] for i in range(1, 5)]]
    for row in range(5):
        for _ in range(1, 5):
            new_grid[row].append(add_one_grid(new_grid[row][-1]))

    values = [
        "".join(i[j] for i in row)
        for row in new_grid
        for j in range(original_rows)
    ]

    # Create a graph
    G = nx.DiGraph()

    # Add the nodes and weighted edges
    number_rows = len(values)
    number_cols = len(values[0])
    for row in range(number_rows):
        for col in range(number_cols):
            # Add this node
            start = (col, row)
            start_risk = int(values[row][col])
            G.add_node(start)
            # Check the new node is on the graph
            if row + 1 < number_rows:
                new = (col, row + 1)
                G.add_node(new)
                risk = int(values[row + 1][col])
                G.add_weighted_edges_from(
                    [(start, new, risk), (new, start, start_risk)]
                )
            # Check the new node is on the graph
            if col + 1 < number_cols:
                new = (col + 1, row)
                G.add_node(new)
                risk = int(values[row][col + 1])
                G.add_weighted_edges_from(
                    [(start, new, risk), (new, start, start_risk)]
                )

    # Get the shortest path
    answer, _ = nx.bidirectional_dijkstra(
        G, (0, 0), (number_cols - 1, number_rows - 1)
    )

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
