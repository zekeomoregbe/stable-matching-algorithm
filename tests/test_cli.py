import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from stable_matching.cli import main


class CliTests(unittest.TestCase):
    def write_input(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        with handle:
            json.dump(
                {
                    "proposers": {"A": ["X", "Y"], "B": ["Y", "X"]},
                    "receivers": {"X": ["A", "B"], "Y": ["B", "A"]},
                },
                handle,
            )
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_json_output(self):
        path = self.write_input()
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main([path, "--json"])
        self.assertEqual(0, code)
        data = json.loads(stream.getvalue())
        self.assertTrue(data["stable"])
        self.assertEqual({"A": "X", "B": "Y"}, data["matches"])

    def test_receivers_can_be_proposing_side(self):
        path = self.write_input()
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main([path, "--proposing-side", "receivers", "--json"])
        self.assertEqual(0, code)
        data = json.loads(stream.getvalue())
        self.assertEqual("receivers", data["proposing_side"])
        self.assertEqual({"A": "X", "B": "Y"}, data["matches"])
        self.assertTrue(data["stable"])


if __name__ == "__main__":
    unittest.main()
