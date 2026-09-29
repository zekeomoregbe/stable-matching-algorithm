# Stable Matching Algorithm

A Python implementation of the Gale-Shapley deferred-acceptance algorithm. The project computes stable pairings from ranked preferences, verifies stability, supports incomplete preference lists, and can run with either side making proposals.

## Features

- Gale-Shapley stable matching
- proposer-optimal or receiver-optimal matching
- incomplete preference lists and unmatched participants
- blocking-pair detection
- independent stability verification
- JSON input
- command-line interface
- automated tests and GitHub Actions CI

## How the algorithm works

A free proposer repeatedly proposes to the highest-ranked receiver they have not tried yet. Each receiver keeps the most preferred proposal seen so far and rejects the other proposer. Rejected proposers continue down their lists.

The process ends when each proposer is either matched or has no preferences left to try. For complete preference lists with the same number of participants on both sides, Gale-Shapley finishes after at most `n²` proposals.

## Data structures

The implementation uses a few simple structures to keep the algorithm efficient:

- `deque` for free proposers
- dictionaries for current matches
- a next-choice index for each proposer
- precomputed receiver rank maps for `O(1)` preference comparisons

More detail is available in [`docs/ALGORITHM.md`](docs/ALGORITHM.md).

## Example input

```json
{
  "proposers": {
    "Avery": ["Jordan", "Riley", "Morgan", "Casey"],
    "Blake": ["Riley", "Jordan", "Casey", "Morgan"]
  },
  "receivers": {
    "Jordan": ["Blake", "Avery"],
    "Riley": ["Avery", "Blake"],
    "Morgan": ["Avery", "Blake"],
    "Casey": ["Blake", "Avery"]
  }
}
```

Preference lists do not have to be complete. If one side does not rank a participant, that pairing is treated as unacceptable.

## Run the project

Python 3.10+ is required.

```bash
python -m pip install -e .
stable-match examples/preferences.json
```

Example output:

```text
Stable matching (proposers proposing)
------------------------------------------
       Avery  ->  Riley
       Blake  ->  Jordan
     Cameron  ->  Casey
        Drew  ->  Morgan

Proposals made: 8
Stable: yes
```

JSON output is also available:

```bash
stable-match examples/preferences.json --json
```

Run with the receiver side proposing:

```bash
stable-match examples/preferences.json --proposing-side receivers
```

You can also run the package without installing the command:

```bash
PYTHONPATH=src python -m stable_matching examples/preferences.json
```

## Verify a matching in Python

```python
from stable_matching import find_blocking_pairs, is_stable

proposers = {
    "A": ["X", "Y"],
    "B": ["Y", "X"],
}
receivers = {
    "X": ["A", "B"],
    "Y": ["B", "A"],
}
matching = {"A": "X", "B": "Y"}

print(is_stable(proposers, receivers, matching))
print(find_blocking_pairs(proposers, receivers, matching))
```

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers normal matchings, incomplete lists, unacceptable partners, blocking-pair detection, validation, JSON loading, and CLI output.

## Project structure

```text
src/stable_matching/
  matcher.py        Gale-Shapley and stability checking
  io.py             JSON preference loading
  cli.py            command-line interface
examples/           sample preference files
tests/              unit and CLI tests
docs/               algorithm notes
```

## Complexity

For complete preference lists with `n` participants on each side:

- time: `O(n²)`
- matching state: `O(n)`
- stored preference/rank data: `O(n²)`

For incomplete lists, the proposal loop is bounded by the number of acceptable pairs.
