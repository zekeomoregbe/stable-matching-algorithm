from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import load_preferences
from .matcher import gale_shapley


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stable-match",
        description="Compute a Gale-Shapley stable matching from a JSON preference file.",
    )
    parser.add_argument("input", type=Path, help="JSON file containing 'proposers' and 'receivers'")
    parser.add_argument(
        "--proposing-side",
        choices=("proposers", "receivers"),
        default="proposers",
        help="side that makes proposals; changes which side receives the optimal stable matching",
    )
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        proposers, receivers = load_preferences(args.input)

        if args.proposing_side == "proposers":
            result = gale_shapley(proposers, receivers)
            matches = result.matches
            unmatched_proposers = result.unmatched_proposers
            unmatched_receivers = result.unmatched_receivers
        else:
            reverse_result = gale_shapley(receivers, proposers)
            matches = {proposer: receiver for receiver, proposer in reverse_result.matches.items()}
            result = reverse_result
            unmatched_proposers = reverse_result.unmatched_receivers
            unmatched_receivers = reverse_result.unmatched_proposers

        if args.json:
            print(
                json.dumps(
                    {
                        "matches": matches,
                        "unmatched_proposers": list(unmatched_proposers),
                        "unmatched_receivers": list(unmatched_receivers),
                        "proposals": result.proposals,
                        "stable": result.stable,
                        "proposing_side": args.proposing_side,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(f"Stable matching ({args.proposing_side} proposing)")
            print("-" * 42)
            for proposer in proposers:
                partner = matches.get(proposer, "UNMATCHED")
                print(f"{proposer:>12}  ->  {partner}")
            print(f"\nProposals made: {result.proposals}")
            print(f"Stable: {'yes' if result.stable else 'no'}")
            if unmatched_proposers:
                print("Unmatched proposers: " + ", ".join(unmatched_proposers))
            if unmatched_receivers:
                print("Unmatched receivers: " + ", ".join(unmatched_receivers))

        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
