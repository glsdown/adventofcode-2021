import re
import sys
from collections import defaultdict
from itertools import combinations

import networkx as nx

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split("-") for line in f.readlines()]

    # Create a graph
    G = nx.Graph()

    # Identify the nodes and edges
    nodes = set()
    edges = set()
    big_caverns = defaultdict(set)
    for start, end in values:
        # Add the caverns
        nodes.add(start)
        nodes.add(end)
        # Add the connections with the small caverns
        if (not start.isupper()) and (not end.isupper()):
            edges.add((start, end))
        else:
            # If there is a 'big' cavern, want to instead create multiple
            # ones later - simply record the matches here
            if start.isupper():
                big_caverns[start].add(end)
            if end.isupper():
                big_caverns[end].add(start)

    # Create all the possible 'entrances' and 'exits'
    for node, caverns in big_caverns.items():
        for x, y in combinations(caverns, 2):
            new_node = f"{x}{node}{y}"
            nodes.add(new_node)
            edges.add((x, new_node))
            edges.add((y, new_node))

    # Add the nodes and edges
    G.add_nodes_from(list(nodes))
    G.add_edges_from(list(edges))

    # Get the number of paths
    # for path in nx.all_simple_paths(G, source="start", target="end"):
    #     print(path)
    answer = len(
        [path for path in nx.all_simple_paths(G, source="start", target="end")]
    )

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split("-") for line in f.readlines()]

    def get_new_graph(cavern_values, c):

        # Create a graph
        G = nx.Graph()
        # Identify the nodes and edges
        nodes = set()
        edges = set()
        big_caverns = defaultdict(set)
        small_caverns = set()
        for start, end in cavern_values:
            # Add the caverns
            nodes.add(start)
            nodes.add(end)
            # Add the connections with the small caverns
            if (not start.isupper()) and (not end.isupper()):
                edges.add((start, end))
                if start not in ["start", "end"]:
                    small_caverns.add(start)
                if end not in ["start", "end"]:
                    small_caverns.add(end)
            else:
                # If there is a 'big' cavern, want to instead create multiple
                # ones later - simply record the matches here
                if start.isupper():
                    big_caverns[start].add(end)
                    if end not in ["start", "end"]:
                        small_caverns.add(end)
                if end.isupper():
                    big_caverns[end].add(start)
                    if start not in ["start", "end"]:
                        small_caverns.add(start)

        # Create all the possible 'entrances' and 'exits'
        for node, caverns in big_caverns.items():
            for x, y in combinations(sorted(caverns), 2):
                new_node = f"{x}{node}{y}"
                nodes.add(new_node)
                edges.add((x, new_node))
                edges.add((y, new_node))

        # Add the nodes and edges
        G.add_nodes_from(list(nodes))
        G.add_edges_from(list(edges))

        # Return the paths
        return [
            ",".join(
                loc
                if loc.islower()
                else "".join([i for i in loc if i.isupper()])
                for loc in path
            ).replace("temp", c)
            for path in nx.all_simple_paths(G, source="start", target="end")
        ]

    # Identify the small caverns
    answer = []
    caverns = set(
        [
            i
            for line in values
            for i in line
            if i.islower() and i not in ["start", "end"]
        ]
    )

    # Loop through each small cavern and duplicate it
    for c in caverns:
        cavern_values = (
            values
            + [["temp", y] for x, y in values if x == c]
            + [[x, "temp"] for x, y in values if y == c]
        )
        answer += get_new_graph(cavern_values, c)

    answer = len(set(answer))

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
