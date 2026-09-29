from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Mapping, Sequence

Preferences = Mapping[str, Sequence[str]]


@dataclass(frozen=True)
class StableMatchingResult:
    """Result produced by Gale-Shapley."""

    matches: dict[str, str]
    unmatched_proposers: tuple[str, ...]
    unmatched_receivers: tuple[str, ...]
    proposals: int
    stable: bool


def gale_shapley(proposer_preferences: Preferences, receiver_preferences: Preferences) -> StableMatchingResult:
    """Compute a proposer-optimal stable matching.

    Preference lists may be incomplete. A receiver treats a proposer as
    unacceptable when that proposer is not present in the receiver's list.
    """
    _validate_preferences(proposer_preferences, receiver_preferences)

    proposer_lists = {person: list(ranking) for person, ranking in proposer_preferences.items()}
    receiver_rank = {
        receiver: {proposer: rank for rank, proposer in enumerate(ranking)}
        for receiver, ranking in receiver_preferences.items()
    }

    free = deque(proposer_lists)
    next_choice = {proposer: 0 for proposer in proposer_lists}
    receiver_partner: dict[str, str] = {}
    proposals = 0

    while free:
        proposer = free.popleft()
        preferences = proposer_lists[proposer]

        while next_choice[proposer] < len(preferences):
            receiver = preferences[next_choice[proposer]]
            next_choice[proposer] += 1
            proposals += 1

            ranks = receiver_rank[receiver]
            if proposer not in ranks:
                continue

            current = receiver_partner.get(receiver)
            if current is None:
                receiver_partner[receiver] = proposer
                break

            if ranks[proposer] < ranks[current]:
                receiver_partner[receiver] = proposer
                free.append(current)
                break

    matches = {proposer: receiver for receiver, proposer in receiver_partner.items()}
    unmatched_proposers = tuple(person for person in proposer_lists if person not in matches)
    unmatched_receivers = tuple(person for person in receiver_preferences if person not in receiver_partner)

    return StableMatchingResult(
        matches=matches,
        unmatched_proposers=unmatched_proposers,
        unmatched_receivers=unmatched_receivers,
        proposals=proposals,
        stable=is_stable(proposer_preferences, receiver_preferences, matches),
    )


def find_blocking_pairs(
    proposer_preferences: Preferences,
    receiver_preferences: Preferences,
    matches: Mapping[str, str],
) -> list[tuple[str, str]]:
    """Return every blocking pair in a proposed matching."""
    _validate_preferences(proposer_preferences, receiver_preferences)

    receiver_to_proposer = {receiver: proposer for proposer, receiver in matches.items()}
    receiver_rank = {
        receiver: {proposer: rank for rank, proposer in enumerate(ranking)}
        for receiver, ranking in receiver_preferences.items()
    }

    blocking: list[tuple[str, str]] = []

    for proposer, ranking in proposer_preferences.items():
        current_receiver = matches.get(proposer)

        for receiver in ranking:
            ranks = receiver_rank[receiver]
            if proposer not in ranks:
                continue

            if receiver == current_receiver:
                break

            current_proposer = receiver_to_proposer.get(receiver)
            if current_proposer is None or ranks[proposer] < ranks[current_proposer]:
                blocking.append((proposer, receiver))

    return blocking


def is_stable(
    proposer_preferences: Preferences,
    receiver_preferences: Preferences,
    matches: Mapping[str, str],
) -> bool:
    """Return True when a matching contains no blocking pair."""
    return not find_blocking_pairs(proposer_preferences, receiver_preferences, matches)


def _validate_preferences(proposer_preferences: Preferences, receiver_preferences: Preferences) -> None:
    if not proposer_preferences:
        raise ValueError("proposer preferences cannot be empty")
    if not receiver_preferences:
        raise ValueError("receiver preferences cannot be empty")

    proposer_names = set(proposer_preferences)
    receiver_names = set(receiver_preferences)

    for proposer, ranking in proposer_preferences.items():
        if len(set(ranking)) != len(ranking):
            raise ValueError(f"duplicate receiver in preference list for {proposer}")
        unknown = set(ranking) - receiver_names
        if unknown:
            raise ValueError(f"unknown receiver(s) for {proposer}: {', '.join(sorted(unknown))}")

    for receiver, ranking in receiver_preferences.items():
        if len(set(ranking)) != len(ranking):
            raise ValueError(f"duplicate proposer in preference list for {receiver}")
        unknown = set(ranking) - proposer_names
        if unknown:
            raise ValueError(f"unknown proposer(s) for {receiver}: {', '.join(sorted(unknown))}")
