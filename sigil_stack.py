from __future__ import annotations
from typing import Dict, Any
import json
from pathlib import Path

from system_refiner import SystemRefiner
from discount_combiner import DiscountCombiner, DiscountRule
from enhancement_discovery import EnhancementDiscovery
from registry_manifest import RegistryManifest
from corpus_loader import CorpusLoader
from index_builder import IndexBuilder
from retrieval_index import RetrievalIndex


class SigilAGIStack:
    def __init__(self) -> None:
        self.refiner = SystemRefiner()
        self.combiner = DiscountCombiner()
        self.discovery = EnhancementDiscovery()
        self.registry = RegistryManifest()
        self.base_dir = Path(__file__).resolve().parent
        self.retrieval = None

    def load_demo_state(self) -> None:
        corpus = CorpusLoader(self.base_dir / "corpus.json").load()
        index_snapshot = IndexBuilder().build(corpus)
        self.retrieval = RetrievalIndex(index_snapshot)

        self.combiner.add_rule(DiscountRule(priority=10, name="launch10", kind="percent", value=10.0))
        self.combiner.add_rule(DiscountRule(priority=20, name="vip5", kind="fixed", value=5.0))

        self.registry.register_modules([
            "system_refiner.py",
            "discount_combiner.py",
            "enhancement_discovery.py",
            "registry_manifest.py",
            "corpus_loader.py",
            "index_builder.py",
            "retrieval_index.py",
            "sigil_stack.py",
            "corpus.json",
        ])
        self.registry.apply_state(
            boot_verified=True,
            rehydrated=True,
            indexed=True,
        )

    def demo(self) -> Dict[str, Any]:
        self.load_demo_state()

        rag_hits = self.retrieval.search("deterministic retrieval anchor config", top_k=2)
        refined = self.refiner.refine(
            {"mode": "seed", "layers": {"core": True, "apps": False}},
            {"mode": "expanded", "layers": {"apps": True}, "boot": {"verified": True}},
        )
        pricing = self.combiner.combine(125.0)
        recommendations = self.discovery.discover(
            {
                "doc_count": len(self.retrieval.snapshot["docs"]),
                "discount_rule_count": len(self.combiner.rules),
                "change_count": refined["change_count"],
            }
        )
        registry = self.registry.snapshot()

        return {
            "rag_hits": rag_hits,
            "refined": refined,
            "pricing": pricing,
            "recommendations": recommendations,
            "registry": registry,
            "index": {
                "doc_count": self.retrieval.snapshot["doc_count"],
                "term_count": self.retrieval.snapshot["term_count"],
            },
        }


def main() -> int:
    result = SigilAGIStack().demo()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
