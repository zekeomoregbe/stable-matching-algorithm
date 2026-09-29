# Algorithm Notes

## Gale-Shapley

The implementation uses the deferred-acceptance algorithm described by Gale and Shapley.

Each free proposer starts with the highest-ranked receiver they have not proposed to yet. A receiver tentatively accepts a proposal when unmatched. If already matched, the receiver keeps whichever proposer is ranked higher and rejects the other. Rejected proposers continue down their preference lists.

The process stops when every proposer is either matched or has exhausted their preference list.

## Data structures

The implementation uses:

- a `deque` for the set of free proposers
- a dictionary that stores each proposer's next preference index
- a dictionary that stores the current partner of each receiver
- precomputed receiver ranking dictionaries for constant-time preference comparisons

Precomputing receiver ranks avoids scanning an entire preference list every time two proposers are compared.

## Complexity

For complete preference lists with `n` proposers and `n` receivers, each proposer can propose to each receiver at most once. That gives at most `n²` proposals and an `O(n²)` running time.

With incomplete preference lists, the number of proposals is bounded by `E`, the total number of acceptable proposer-to-receiver edges, so the matching loop runs in `O(E)` time after preference ranks are built.

The stability checker examines acceptable pairs and uses the same precomputed receiver ranks for constant-time comparisons.

## Stability

A blocking pair is a proposer and receiver who are not matched to each other but would both prefer each other over their current situation. A matching is stable when no blocking pair exists.

The package exposes both `is_stable(...)` and `find_blocking_pairs(...)` so a matching can be verified independently of the Gale-Shapley run.

## Proposer optimality

When proposers initiate the deferred-acceptance process, the result is proposer-optimal among all stable matchings. The command-line interface can also run the algorithm with the receiver side proposing, which produces the receiver-optimal stable matching.
