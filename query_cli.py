#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from sigil_stack import SigilAGIStack


def main() -> int:
    parser = argparse.ArgumentParser(description="SigilAGI query CLI")
    parser.add_argument("query", help="Query string")
    parser.add_argument("--top-k", type=int, default=3, help="Number of hits to return")
    args = parser.parse_args()

    result = SigilAGIStack().run_query(args.query, top_k=args.top_k)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
