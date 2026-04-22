from __future__ import annotations
from typing import Dict, Any
import json

from proxy_pointer_rag import ProxyPointerRAG
from system_refiner import SystemRefiner
from discount_combiner import DiscountCombiner, DiscountRule
from enhancement_discovery import EnhancementDiscovery
from registry_manifest import RegistryManifest


class SigilAGIStack:
    def __init__(self) -> None:
        self.rag = ProxyPointerRAG()
        self.refiner = SystemRefiner()
        self.combiner = DiscountCombiner()
        self.discovery = EnhancementDiscovery()
        self.registry = RegistryManifest()

    def load_demo_state(self) -> None:
        self.rag.add_document(
            "glyph-core",
            "GlyphMatics core focuses on deterministic symbolic execution anchored registries and reproducible transforms.",
            {"layer": "core"},
        )
        self.rag.add_document(
            "sigil-rag",
            "Proxy pointer RAG uses stable retrieval over indexed documents and returns precise anchor ranges for expansion.",
            {"layer": "retrieval"},
        )
        self.combiner.add_rule(DiscountRule(priority=10, name="launch10", kind="percent", value=10.0))
        self.combiner.add_rule(DiscountRule(priority=20, name="vip5", kind="fixed", value=5.0))

        self.registry.register_modules([
            "proxy_pointer_rag.py",
            "system_refiner.py",
            "discount_combiner.py",
            "enhancement_discovery.py",
            "registry_manifest.py",
            "sigil_stack.py",
        ])
        self.registry.apply_state(boot_verified=True, rehydrated=True)

    def demo(self) -> Dict[str, Any]:
        self.load_demo_state()
        rag_hits = self.rag.search("deterministic retrieval anchor config", top_k=2)
        refined = self.refiner.refine(
            {"mode": "seed", "layers": {"core": True, "apps": False}},
            {"mode": "expanded", "layers": {"apps": True}, "boot": {"verified": True}},
        )
        pricing = self.combiner.combine(125.0)
        recommendations = self.discovery.discover(
            {
                "doc_count": len(self.rag.docs),
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
        }

def main() -> int:
    result = SigilAGIStack().demo()
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
