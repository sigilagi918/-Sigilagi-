#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from sigil_stack import SigilAGIStack


def render_text(result: Dict[str, Any], show_registry: bool, show_pricing: bool, show_refined: bool) -> str:
    lines = []

    retrieval = result["retrieval"]
    lines.append(f'Query: {retrieval["query"]}')
    lines.append(f'Top K: {retrieval["top_k"]}')
    lines.append(f'Hits: {retrieval["hit_count"]}')
    lines.append("")

    for i, hit in enumerate(retrieval["hits"], 1):
        lines.append(f'[{i}] {hit["doc_id"]}  score={hit["score"]}')
        lines.append(f'    layer: {hit["metadata"].get("layer", "")}')
        lines.append(f'    ptr  : {hit["proxy_pointer"]}')
        lines.append(f'    text : {hit["snippet"]}')
        lines.append("")

    if show_pricing and "pricing" in result:
        pricing = result["pricing"]
        lines.append("Pricing")
        lines.append(f'  subtotal      : {pricing["subtotal"]}')
        lines.append(f'  final_total   : {pricing["final_total"]}')
        lines.append(f'  total_discount: {pricing["total_discount"]}')
        lines.append("")

    if show_refined and "refined" in result:
        refined = result["refined"]
        lines.append("Refined")
        lines.append(f'  change_count: {refined["change_count"]}')
        lines.append("")

    if show_registry and "registry" in retrieval:
        registry = retrieval["registry"]
        lines.append("Registry")
        lines.append(f'  system : {registry["system"]}')
        lines.append(f'  version: {registry["version"]}')
        lines.append(f'  slice  : {registry["slice"]}')
        lines.append(f'  modules: {len(registry["modules"])}')
        lines.append("")

    if "index" in result:
        index = result["index"]
        lines.append("Index")
        lines.append(f'  doc_count : {index["doc_count"]}')
        lines.append(f'  term_count: {index["term_count"]}')

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="SigilAGI query CLI")
    parser.add_argument("query", help="Query string")
    parser.add_argument("--top-k", type=int, default=3, help="Number of hits to return")
    parser.add_argument("--json", action="store_true", help="Emit full JSON")
    parser.add_argument("--show-registry", action="store_true", help="Show registry summary in text mode")
    parser.add_argument("--show-pricing", action="store_true", help="Show pricing summary in text mode")
    parser.add_argument("--show-refined", action="store_true", help="Show refinement summary in text mode")
    args = parser.parse_args()

    result = SigilAGIStack().run_query(args.query, top_k=args.top_k)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_text(
            result,
            show_registry=args.show_registry,
            show_pricing=args.show_pricing,
            show_refined=args.show_refined,
        ), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
