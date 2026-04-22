#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from corpus_loader import CorpusLoader
from index_builder import IndexBuilder


def main() -> int:
    base = Path(__file__).resolve().parent
    corpus_path = base / "corpus.json"
    out_path = base / "index.json"

    docs = CorpusLoader(corpus_path).load()
    snapshot = IndexBuilder().build(docs)

    out_path.write_text(
        json.dumps(snapshot, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
