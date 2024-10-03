import math
from dataclasses import dataclass
from typing import List


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
        return Solution([DriverAssignment(self.loads[:3])])


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
