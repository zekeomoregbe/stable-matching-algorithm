"""Stable matching package."""

from .matcher import StableMatchingResult, find_blocking_pairs, gale_shapley, is_stable

__all__ = [
    "StableMatchingResult",
    "gale_shapley",
    "find_blocking_pairs",
    "is_stable",
]
