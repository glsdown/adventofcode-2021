import re
import sys

import pandas as pd

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [list(line.strip()) for line in f.readlines()]

    # Complete the task
    gamma = "".join(
        str(i) for i in pd.DataFrame(values).mode().iloc[0].to_list()
    )  # Most common bit in each position
    epsilon = "".join(
        "1" if x == "0" else "0" for x in gamma
    )  # Least common bit in each position i.e. the opposite of gamma

    answer = int(gamma, 2) * int(epsilon, 2)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [list(line.strip()) for line in f.readlines()]

    # Complete the task
    df = pd.DataFrame(values)

    def get_value(default):
        df_tmp = df
        for col in df.columns:
            common = df_tmp[col].mode().to_list()
            if len(common) == 2:
                common = default
            else:
                if default == "1":
                    common = common[0]
                else:
                    common = "0" if common[0] == "1" else "1"

            df_tmp = df_tmp.loc[df_tmp[col] == common]
            if df_tmp.shape[0] == 1:
                return "".join(str(i) for i in df_tmp.iloc[0].to_list())

    oxygen = get_value("1")
    co2 = get_value("0")

    answer = int(oxygen, 2) * int(co2, 2)

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
