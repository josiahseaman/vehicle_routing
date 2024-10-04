"""
- Define a clear context to think about solution neighbors and optimization.
- table of precalculated distances (sorted) for preferred directed graph pairings
- I can run simulated annealing or Tabu search on the table once I have it,
- But I can also just take the optimal greedy solution and see how it ranks.

"""

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


class DriverAssignment:

    def __init__(self, loads: List[Load]):
        self._loads = loads
        self._total_distance = self.calc_total_distance()  # expensive operation

    def calc_total_distance(self):
        """Return total amount driven by one driver.
        This includes the distances unladen in-between loads and the final return home (0,0).
        Avoided list comprehension for readability."""
        total_driven = 0.0
        stop_coord = Point(0, 0)
        for load in self._loads:
            arrival = stop_coord.distance(load.pickup)
            transport = load.pickup.distance(load.dropoff)
            total_driven += arrival + transport
            stop_coord = load.dropoff
        go_home = stop_coord.distance(Point(0, 0))  # stop_coord is no longer 0,0 here
        total_driven += go_home
        self._total_distance = total_driven
        return total_driven

    def total_distance(self):
        """This is a cache for a value that is expensive to compute."""
        if not self._total_distance:
            return self.calc_total_distance()
        return self._total_distance

    def filler_distance(self):
        """Returns only distances covered when the truck is empty:
        The distances from start (0,0), in-between loads and the final return home (0,0).
        Separated because this is something to optimize.
        Logic: internal_distance = dropoff -> pickup.
            extras = start of day and end of day
        """
        coord_pairs = [
            Load(1, self._loads[i].dropoff, self._loads[i + 1].pickup)
            for i in range(len(self._loads) - 1)
        ]
        internal_distance = sum(x.distance() for x in coord_pairs)
        extras = Point(0, 0).distance(self._loads[0].pickup) + Point(0, 0).distance(
            self._loads[-1].dropoff
        )
        return internal_distance + extras

    def arrival_cost(self, load: Load) -> float:
        """Calculates the amount of extra time required to add this load to this driver"""
        # TODO: can we add the proposed load to the schedule and diff?
        previous_cost = self.total_distance()
        if self._loads:
            # TODO: Jiggle schedule
            # distance from last dropoff to this pickup
            return self._loads[-1].dropoff.distance(load.pickup)
        return Point(0, 0).distance(load.pickup)  # start location

    def time_remaining(self):
        """Used to calculate if another trip can be fit in."""
        return 12 * 60.0 - self.total_distance()

    def add_load(self, load) -> float:
        self._loads.append(load)
        # TODO: jiggle optimize
        return self.calc_total_distance()


@dataclass
class Problem:
    loads: List[Load]

    def solve(self) -> "Solution":
        print("Solving Problem")
        return GreedyPacker().solve(self.loads)


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


class GreedyPacker(Solution):
    """Places the next largest trip in the smallest available slot."""

    def solve(self, loads: List[Load]):
        # Start with the longest haul
        haul_distances = sorted([(l.distance(), l) for l in loads], reverse=True)
        self.assignments = [DriverAssignment([])]
        for trip_time, load in haul_distances:
            assignment_made = False
            # Find the driver with the shortest arrival distance
            candidates = sorted(self.assignments, key=lambda d: d.arrival_cost(load))
            for driver in candidates:
                # Check if they can make it back home in time
                # TODO add transit time
                if driver.arrival_cost(load) < driver.time_remaining():
                    # Add route,
                    # TODO: jiggle schedule
                    driver.add_load(load)
                    assignment_made = True
                    break
                else:
                    # If not, move to next closest
                    continue
            if not assignment_made:
                # If no available slots, add a Driver and give it to them
                self.assignments.append(DriverAssignment([load]))

        return self


def parse_point(point_str: str) -> Point:
    """CSV contains "columns" wrapped in parens which need their own Point objects.
    Ex: "(-116.78442279683607,76.80147820713637)" """
    sx, sy = point_str.strip("()").split(",")
    x, y = float(sx), float(sy)
    return Point(x, y)
