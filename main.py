"""
Vorto Challenge Problem: https://drive.google.com/drive/folders/1Jb7FmR5Ftrg0jwgIJ-n_oKwOjyJ4gDHI
Given a list of <200 loads with a start and stop coordinate, find the shortest collection of paths from (0,0)
That visits all loads.
 total_cost = 500*number_of_drivers + total_number_of_driven_minutes

 Drivers are assumed a constant rate of 1 mile per minute, as the crow flies.

Line of Reasoning:
- Multiple constraint satisfaction
- Start by trying to fill the largest available space first
- Add one more driver each time no possible slots are available
- Start by allocating the longest distance first
- Wait to iterate over possible choices until after a basic solution has been accomplished
- Would adding a driver affect our proposed solution from the start? If we're always picking the objectively largest
    route then the answer is no.
- Next generation will be to pick and positions that are close to pick up locations.
- Construct all possible pairs of loads as a distance
- Start by finding the shortest pair for each possible load, then check time remaining
- Each load can have three perspective pairs and then we iterate over a decision tree of triple branches for selecting
    subsequent loads
- 30 second run time means that we can't exhaustively search all loads. Test this hypothesis. How long would it take?
- Fewer than 200 loads is still a massive combinatorial space, but best for search might be able to prune branching
    dimension down to three or less.
"""

import csv
import os
from collections import namedtuple

# from pathlib import
from pathlib import Path
from typing import List, Tuple
import math


class Point:
    """Classic 2D points. Meant to make distances easier to work with."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> float:
        """Cartesian distance.  Here to avoid using external libraries."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Load:
    def __init__(self, load_number: int, pickup: Point, dropoff: Point):
        self.load_number = load_number
        self.pickup = pickup
        self.dropoff = dropoff


def parse_point(point_str: str) -> Point:
    """CSV contains "columns" wrapped in parens which need their own Point objects.
    Ex: "(-116.78442279683607,76.80147820713637)" """
    sx, sy = point_str.strip("()").split(",")
    x, y = float(sx), float(sy)
    return Point(x, y)


def load_csv_files(folder: Path) -> List[Load]:
    loads = []
    for filename in folder.glob("*.txt"):
        with open(filename, "r") as file:
            csv_reader = csv.reader(file, delimiter=" ")
            next(csv_reader)  # Skip header
            for row in csv_reader:
                load_number = int(row[0])
                pickup = parse_point(row[1])
                dropoff = parse_point(row[2])
                loads.append(Load(load_number, pickup, dropoff))
    return loads


def main(folder: Path):
    print(folder)

    loads = load_csv_files(folder)

    # Testing: Print the distance between pickup and dropoff for each load
    for load in loads:
        distance = load.pickup.distance(load.dropoff)
        print(f"Load {load.load_number}: Distance = {distance:.1f}")


if __name__ == "__main__":
    # Usage
    folder_path = Path("./problems/")
    main(folder_path)
