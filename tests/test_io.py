import json
import tempfile
import unittest
from pathlib import Path

from stable_matching.io import load_preferences


class InputTests(unittest.TestCase):
    def write_json(self, data):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        with handle:
            json.dump(data, handle)
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_loads_valid_preferences(self):
        path = self.write_json({"proposers": {"A": ["X"]}, "receivers": {"X": ["A"]}})
        proposers, receivers = load_preferences(path)
        self.assertEqual({"A": ["X"]}, proposers)
        self.assertEqual({"X": ["A"]}, receivers)

    def test_missing_side_is_invalid(self):
        path = self.write_json({"proposers": {"A": ["X"]}})
        with self.assertRaisesRegex(ValueError, "receivers"):
            load_preferences(path)

    def test_ranking_must_be_list_of_strings(self):
        path = self.write_json({"proposers": {"A": "X"}, "receivers": {"X": ["A"]}})
        with self.assertRaisesRegex(ValueError, "array of strings"):
            load_preferences(path)


if __name__ == "__main__":
    unittest.main()
