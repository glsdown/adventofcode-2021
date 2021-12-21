import re
import sys

from functools import reduce
from operator import mul

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        value = [line.strip() for line in f.readlines()][0]

    binary_instruction = "".join(["{0:04b}".format(int(v, 16)) for v in value])

    # Rules:
    # First 3 bits = packet version
    # Next 3 bits = type ID
    # - ID 4 = 'literal value' - single binary number
    #       Then keep going in groups of 4 until group of 4 starts with a 0
    # - Other IDs are operators
    #       First bit is length type id:
    #       - 0 = 15 bit sub-package length
    #       - 1 = 11 bit sub-package length
    #       once you have the sub-package length, that says how many
    #       sub-packages there are to find.

    def get_number_versions(packet):
        if len(packet) == 0 or all(i == "0" for i in packet):
            return 0, ""
        else:
            # Get the metadata
            version = int(packet[:3], 2)
            type_id = int(packet[3:6], 2)
            number_types = version

            # Literal value case
            if type_id == 4:
                for i in range(6, len(packet), 5):
                    if packet[i] == "0":
                        counter = i + 5
                        break

                return number_types, packet[counter:]

            # Sub-packet case

            # Identify the sub-packet lengths
            length_type_id = packet[6]
            if length_type_id == "0":
                sub_package_length = 15
            else:
                sub_package_length = 11

            # Get the start of the next section
            counter = 7 + sub_package_length
            sub_package_count = int("".join(packet[7:counter]), 2)

            # Get the counts in the sub-packages
            current = packet[counter:]
            for _ in range(sub_package_count):
                count, current = get_number_versions(current)
                number_types += count

            # Return the total
            return number_types, current

    # Run the process
    answer, _ = get_number_versions(binary_instruction)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        value = [line.strip() for line in f.readlines()][0]

    binary_instruction = "".join(["{0:04b}".format(int(v, 16)) for v in value])

    # Rules:
    # First 3 bits = packet version
    # Next 3 bits = type ID
    # - ID 4 = 'literal value' - single binary number
    #       Then keep going in groups of 4 until group of 4 starts with a 0
    # - Other IDs are operators
    #       First bit is length type id:
    #       - 0 = 15 bit sub-package length
    #       - 1 = 11 bit sub-package length
    #       once you have the sub-package length, that says how many
    #       sub-packages there are to find.
    #       Then:
    #       - Packets with type ID 0 are sum
    #       - Packets with type ID 1 are product
    #       - Packets with type ID 2 are minimum
    #       - Packets with type ID 3 are maximum
    #       - Packets with type ID 5 are greater than packets - their value is
    #       1 if the value of the first sub-packet is greater than the value
    #       of the second sub-packet; otherwise, their value is 0. These
    #       packets always have exactly two sub-packets.
    #       - Packets with type ID 6 are less than packets - their value is
    #       1 if the value of the first sub-packet is less than the value
    #       of the second sub-packet; otherwise, their value is 0. These
    #       packets always have exactly two sub-packets.
    #       - Packets with type ID 7 are equal to packets - their value is
    #       1 if the value of the first sub-packet is equal to the value of
    #       the second sub-packet; otherwise, their value is 0. These packets
    #       always have exactly two sub-packets.

    def get_packet_value(packet):
        if len(packet) == 0 or all(i == "0" for i in packet):
            return None, ""
        else:
            # Get the metadata
            type_id = int(packet[3:6], 2)

            # Literal value case
            counter = len(packet) - 5  # Backup
            if type_id == 4:
                for i in range(6, len(packet), 5):
                    if packet[i] == "0":
                        counter = i + 5
                        break
                # Remove the 'leading' bit in each group
                value = [
                    v for i, v in enumerate(packet[6:counter]) if i % 5 != 0
                ]
                value = int("".join(value), 2)
                print(f"Type 4 value {value}")
                return value, packet[counter:]

            # Sub-packet case

            # Identify the sub-packet lengths
            length_type_id = packet[6]
            if length_type_id == "0":
                sub_package_length = 15
            else:
                sub_package_length = 11

            # Get the start of the next section
            counter = 7 + sub_package_length
            sub_package_bits = int("".join(packet[7:counter]), 2)

            values = []
            current = packet[counter:]
            # Get the counts in the sub-packages
            if length_type_id == "0":
                # In this case, it's the number of bits
                tmp = current[:sub_package_bits]
                current = current[sub_package_bits:]

                print(
                    f"Type {type_id} with length type {length_type_id} "
                    f"showing {sub_package_bits} bits in sub-package"
                )

                # Parse the number of bits in sub-package count
                while len(tmp) > 0:
                    value, tmp = get_packet_value(tmp)
                    values.append(value)
            else:

                print(
                    f"Type {type_id} with length type {length_type_id} "
                    f"showing {sub_package_bits} sub-packages"
                )

                # In this case, it's the number of sub-packages
                for _ in range(sub_package_bits):
                    value, current = get_packet_value(current)
                    values.append(value)

            # Remove the None values
            values = [i for i in values if i is not None]

            # Sum
            if type_id == 0:
                return sum(values), current
            # Product
            if type_id == 1:
                return reduce(mul, values), current
            # Min
            if type_id == 2:
                return min(values), current
            # Max
            if type_id == 3:
                return max(values), current
            # Greater Than
            if type_id == 5:
                return int(values[0] > values[1]), current
            # Less Than
            if type_id == 6:
                return int(values[0] < values[1]), current
            # Equal To
            if type_id == 7:
                return int(values[0] == values[1]), current

    # Complete the task
    print(binary_instruction)
    answer, _ = get_packet_value(binary_instruction)

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
