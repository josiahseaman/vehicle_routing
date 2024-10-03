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
import sys

# from pathlib import
from pathlib import Path
from typing import List, Tuple
import math
from dataclasses import dataclass


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

    def distance(self):
        return self.pickup.distance(self.dropoff)


@dataclass
class DriverAssignment:
    loads: List[Load]

    def total_distance(self):
        """Return total amount driven by one driver.
        This includes the distances unladen in-between loads and the final return home (0,0).
        Avoided list comprehension for readability."""
        total_driven = 0.0
        stop_coord = Point(0, 0)
        for load in self.loads:
            arrival = stop_coord.distance(load.pickup)
            transport = load.pickup.distance(load.dropoff)
            total_driven += arrival + transport
            stop_coord = load.dropoff
        go_home = stop_coord.distance(Point(0, 0))  # stop_coord is no longer 0,0 here
        total_driven += go_home
        return total_driven

    def filler_distance(self):
        """Returns only distances covered when the truck is empty:
        The distances from start (0,0), in-between loads and the final return home (0,0).
        Separated because this is something to optimize.
        Logic: internal_distance = dropoff -> pickup.
            extras = start of day and end of day
        """
        coord_pairs = [
            Load(1, self.loads[i].dropoff, self.loads[i + 1].pickup)
            for i in range(len(self.loads) - 1)
        ]
        internal_distance = sum(x.distance() for x in coord_pairs)
        extras = Point(0, 0).distance(self.loads[0].pickup) + Point(0, 0).distance(
            self.loads[-1].dropoff
        )
        return internal_distance + extras


class Problem:
    loads: List[Load] = []

    def solve(self) -> "Solution":
        print("I got nothing")


class Solution:
    """We want to be able to evaluate multiple Solutions per Problem"""

    assignments: List[DriverAssignment]

    def __init__(self, starting_assignments=None):
        if starting_assignments is None:
            starting_assignments = []  # don't use mutable types in signature
        self.assignments = starting_assignments

    def evaluate(self):
        total_number_of_driven_minutes = sum(
            [driver.total_distance() for driver in self.assignments]
        )
        cost = 500 * len(self.assignments) + total_number_of_driven_minutes
        return cost


def parse_point(point_str: str) -> Point:
    """CSV contains "columns" wrapped in parens which need their own Point objects.
    Ex: "(-116.78442279683607,76.80147820713637)" """
    sx, sy = point_str.strip("()").split(",")
    x, y = float(sx), float(sy)
    return Point(x, y)


def load_csv_files(folder: Path) -> List[Problem]:
    """Returns Problem objects with no assignments for each Problem file.
    Every Problem is waiting for a Solution!"""
    problems = []
    for filename in folder.glob("*.txt"):
        current_set = Problem()
        with open(filename, "r") as file:
            csv_reader = csv.reader(file, delimiter=" ")
            next(csv_reader)  # Skip header
            for row in csv_reader:
                load_number = int(row[0])
                pickup = parse_point(row[1])
                dropoff = parse_point(row[2])
                current_set.loads.append(Load(load_number, pickup, dropoff))
        problems.append(current_set)
    return problems


def main(folder: Path):
    print("Loading all problems in ", folder.resolve())

    loads = load_csv_files(folder)
    # TODO: populate multiple problems


if __name__ == "__main__":
    folder_path = Path(sys.argv[1])
    # Check existance
    if folder_path.exists():
        main(folder_path)
    else:
        print(folder_path.resolve(), " does not exist")
