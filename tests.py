import unittest

from pathlib import Path
from main import DriverAssignment, Solution, load_csv_files


class EvaluationTestCase(unittest.TestCase):
    def test_test_framework(self):
        self.assertEqual(True, True)  # this should always load and pass

    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        folder_path = Path("./problems/")
        cls.loads = load_csv_files(folder_path)[0].loads  # replaces cmd invocation

    def test_single_load_distances(self):
        """Test the distances between pickup and dropoff points for the first three loads, doesn't include arrival."""
        # Define expected distances
        expected_distances = [165.5, 174.7, 250.0]

        for i, load in enumerate(self.loads[:3]):
            distance = load.pickup.distance(load.dropoff)
            self.assertAlmostEqual(
                distance,
                expected_distances[i],
                places=1,
                msg=f"Load {load.load_number} distance incorrect.",
            )

    def test_single_assignment_total_distance(self):
        """Test the total distance driven for a single driver assignment."""
        test_assignment = DriverAssignment(self.loads[:3])
        expected_total_distance = 1165.6829  # rounded
        self.assertAlmostEqual(
            test_assignment.total_distance(),
            expected_total_distance,
            places=1,
            msg="Single assignment total distance incorrect.",
        )

    def test_solution_score(self):
        """Test the evaluation of the overall solution score."""
        test_assignment = DriverAssignment(self.loads[:3])
        collective = Solution([test_assignment])
        expected_score = 1665.682  # added 500
        self.assertAlmostEqual(
            collective.evaluate(),
            expected_score,
            places=1,
            msg="Calculated Solution score incorrect.",
        )


if __name__ == "__main__":
    unittest.main()
