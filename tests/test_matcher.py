import unittest

from stable_matching.matcher import find_blocking_pairs, gale_shapley, is_stable


class GaleShapleyTests(unittest.TestCase):
    def setUp(self):
        self.proposers = {
            "A": ["X", "Y", "Z"],
            "B": ["Y", "X", "Z"],
            "C": ["Y", "Z", "X"],
        }
        self.receivers = {
            "X": ["B", "A", "C"],
            "Y": ["A", "C", "B"],
            "Z": ["C", "B", "A"],
        }

    def test_returns_stable_matching(self):
        result = gale_shapley(self.proposers, self.receivers)
        self.assertTrue(result.stable)
        self.assertEqual(3, len(result.matches))
        self.assertEqual((), result.unmatched_proposers)
        self.assertEqual((), result.unmatched_receivers)

    def test_result_is_proposer_optimal_for_example(self):
        result = gale_shapley(self.proposers, self.receivers)
        self.assertEqual({"A": "Y", "B": "X", "C": "Z"}, result.matches)

    def test_counts_proposals(self):
        result = gale_shapley(self.proposers, self.receivers)
        self.assertEqual(6, result.proposals)

    def test_incomplete_preferences_can_leave_participant_unmatched(self):
        proposers = {"A": ["X"], "B": ["X"]}
        receivers = {"X": ["B", "A"], "Y": []}
        result = gale_shapley(proposers, receivers)
        self.assertEqual({"B": "X"}, result.matches)
        self.assertEqual(("A",), result.unmatched_proposers)
        self.assertEqual(("Y",), result.unmatched_receivers)
        self.assertTrue(result.stable)

    def test_receiver_can_mark_proposer_unacceptable(self):
        proposers = {"A": ["X"], "B": ["X"]}
        receivers = {"X": ["B"]}
        result = gale_shapley(proposers, receivers)
        self.assertEqual({"B": "X"}, result.matches)
        self.assertIn("A", result.unmatched_proposers)

    def test_detects_blocking_pair(self):
        unstable = {"A": "Z", "B": "X", "C": "Y"}
        pairs = find_blocking_pairs(self.proposers, self.receivers, unstable)
        self.assertIn(("A", "Y"), pairs)
        self.assertFalse(is_stable(self.proposers, self.receivers, unstable))

    def test_rejects_duplicate_preference(self):
        with self.assertRaisesRegex(ValueError, "duplicate receiver"):
            gale_shapley({"A": ["X", "X"]}, {"X": ["A"]})

    def test_rejects_unknown_participant(self):
        with self.assertRaisesRegex(ValueError, "unknown receiver"):
            gale_shapley({"A": ["X", "Y"]}, {"X": ["A"]})

    def test_empty_side_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            gale_shapley({}, {"X": []})


if __name__ == "__main__":
    unittest.main()
