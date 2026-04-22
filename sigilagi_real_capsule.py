#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import zlib
from typing import Dict, Any


class SigilGlyphCapsule:
    VISIBLE = 'SIGILAGI_COLLAPSE_TO_TEXTUAL_GLYPH_IMAGE'
    BRAILLE = '⠎⠊⠛⠊⠇⠁⠛⠊⠉⠕⠇⠇⠁⠏⠎⠑'
    HANZI = '一二十'

    IDENTITY_SHA256 = '44209342fff30aa5af57ad97b6ceab96db7a0bc12a2fcc0d97e2e41c53e0deae'
    PAYLOAD_SHA256 = '6914cd9cdac48d0c3cc2bfa857b80fb833358c0e208b4a2efd136224d0455f12'
    ENTRY_MODULE = 'sigil_stack.py'
    ENTRY_CLASS = 'SigilAGIStack'
    ENTRY_METHOD = 'demo'
    METADATA = {'name': 'sigilagi-real', 'version': 'v4', 'slice': 'core-control-retrieval-pricing-discovery'}
    MANIFEST = {'proxy_pointer_rag.py': {'sha256': 'bc2957347fc33c852c716e0470e2c54382c0479ae8a73da0849695f7b15c4351', 'size': 1196}, 'system_refiner.py': {'sha256': '276f899f3361837e8e1a887ec3d08ac2b608405df19b4abd9c2d78f916c24f35', 'size': 1024}, 'discount_combiner.py': {'sha256': 'c8acbd07442bc95e74f596b08a61a73a0ca95fbbb58d6f5b5d7b69cffff24fb3', 'size': 1409}, 'sigil_stack.py': {'sha256': 'eaca1f0f86e7841c31453e7290e894b047e6d070ef271e451687f146cef000d0', 'size': 2202}, 'enhancement_discovery.py': {'sha256': '23eaf9ffa500d13027607278358ddc0be5546379074cb749e26b9de032a2ada9', 'size': 1349}}

    ENCODED_PAYLOAD = 'c-pmDU60$i75yuO`yv$@uRYuBgIfn1?54p2>2{G6eHjk~S)x5`BuXKr)W*R7z4u;{GAYTPal4(x#ujyXzj=5_KhFxG^SYC5n%C7<NUrA1akiT6R9&$&-F0oJc$zX%HMMG4CS~1bt*E8mNRlbCHp|OQYp$J8KV(JPV<Y6=z5OV3o3Nin4*$NB$Bo4Qe(dK&wJNw;|3h^=-bfk(VdLYcuH>tYWboH0Q7h3NS4_y(49TqGE2djz9=`}#c#q$*vV+&Vvd&s#Gt~W)4d3c7_zuDsQnYCrX<qJPcK4S3T1)2u{^9ssfm3=#VLkYcKC(4?ctk@^Use<;N|U~X;n!6V+jSfBtZBF`B7BG^1vKP0ihYx|sMezHwk?#ev}qu7ScnJ65*6doGYr;B!3!IO8_heVxNKpRR76f?Zx#P`wW8>tHhzxI0{FM(AjUzFRT;h&JJK-6Dzf#OZDtKuIf~5&dMH$zM9`+-vxuznKQhYJoQluBW6Q;2zK9ccABQ@4IkvYG2VT5ntr9Xa7SDE2ePY8K+0lGLp~{5j?4LOKy;8M`cAHrzb=Tm6ffDovO;11fo}M<dAn{>^f>hk~TE^kqQo9Cw9(%Z%;p&2Hm@MH#G9`sh^-}mSDMe}O#Z1zs<c#YmXueGfxv)^I4{=H`+qGPwl+DmU=oDm9aR5Ha2C3N0T)&g|lwUVOWgm*~gv`pcpD}HDGb4f2k0jI$)pJv)tl0YDJp0uXIc?-DnQ{4)$(&c9!r1x7)$vBC4{^Ll@Px3>$JF;{V?R4v9<Dn34wb+P0ih2>giRJx{c#_mAh`uNbOzr*Fo0hRDP(HC=WVo^<>2F<r#9mWTg2?`nteZ5p3cVAwc$1+EC4{vWcRhAEvc0^vtMh-VZ{pp&M>bq&~#rrp|FsXDiqIjEsc(!>?)^-n1(v(oq#R4ec}j8qJpL=I5a#y=vL&gW7azX%Wb6m<e|X?K;4{yA6`trFEYni_`pMIifqqc5&qw|nyYUBjeZpYCCd8Wtj!cu_|J?Vnhe0aR{0Z$wxCu<8XyY#I-Q7%?NZcv&?|po_y236-n^Ko_a+1YBPBSv4k=Pir(cnvkB|s(xud=^*@4FDa%hpWwn9L{HF$GtE*xh>{QkYO@~79g4@}Duk%(*D&^;eTC2(K$=WClE*3_lQkJvqmYYiEa@bOZD`Y4Hlec{J-nN`~&V}})s?hX%rh>r=w0UOX`9FKM#r;U&s*6rb#HZ|~Eu2P8b|4q;*f&E8sjwQ}@?l2vehVZ#|%MY#hSn)Q)=|hb7w~XH~%HK?opWc1AnT3N7{XS6V)7;yw2fOchZYO7#lZ)<Nwe8v)j7LVX(Ro%E2gF?S3~<SM^0mVa(mGN%=@&ZHKn&l%W*hvPB8X}Xxh3k|BJU=hbHGE`XXCjBRscr>T*$4*=3yDDp5ll69fIiTJ0&-4|DrbvFXtHP&{imqi?hrckk?%mEj>T2BJ>QOt>VFSa<r$kPT6;?$_`P<Wn{Gg?_R?HKg6TMgi-L8Ehgx<$-)(YvP6^0N;DHfwne@qOgd4PzFZcQ0<5-9DdzEEwOlSAFV1l7<fgdiixUF;z*%s(cs@sP`om)NjK>&Eqw@jtxLn4kNh}SK&nE98?%70G&~rJQLOrADVMQz8k+4sTy(m-Idh##74_DntJMu5w45SqvL9ClMKqV`#kGkbms`w5s44mv|8vSGj9rg|{SI!QFw+=~g4`63ca(1U-ievkL`WaLA?!zyiF?qLNYCsOw!|<cgt%J?LIt+d!*GIn|1wN8J2fCh&F}&X>>kM$6S9MDK<i()o!9FlNNA1gF^K@q#c67-4fG__BO_pm$V6p=>xTylG40)_RR$C+yz#(|v5$%L9o(O6c--D1ss&1Ga^d8U-u>}SL993!n#%h9YJa1-Yb~FnZ&MxHQ$&-n1jg^+x9f(bYN_A&;Jus*|qd+0W=;oO}VnG123y8Dm*`^B&*R+PE#dEyeFbQA^*}5k5Cwi_YiFg=nZ|{1<{rzQs&E_wu$nmfBa*@zg;Tnx};MQ`1<P|R~*4`~sVr~pUe7=bPTU+;MTi-<U#<OE@mz<S1#)x-DhMqom^TkU#@@BXQd}z(~>62)2pYGejQV#&*pli=%wYAD?xf9qPhLf!C1IWgeUi50s!ndE%sG3z>SnjU53ENg!<LI+%=oQ0j-^AQ#(5t^@a3DRMk}Dd`F>g|<(}G%0_;y>@t$hcrD|YtMgx+81Eq6v(4=V3&R+sl!J3lk<2G)T&WcG<a-?{X+AH$gBH09{8gm8oIi-?pgzIq=P9L~JieFSvsnbr~BjjUX`ABJy+H03mz!b^8)t~tqq{XW7XYufW-Bw|a1BKGTqmY^y|TQC&fm~A93!YTt^L<<m*(5^Z-6m}(Y^I(Go+Dj`o?th&C$VHAZFS@GHk(recSjrZbQtY%*Y8Gfw;O2~I0lbE8pwko`NYnlj+T0VHz4rY9NVah>He4xSB{$Ngyl#4CQE=Yi^R2gj0SE9HhXn<5)Y-zheR!~fqZltQoVP9_pFt-)e^_@TRPA-0>D1R=4pO<f+ViN;?bt!B^6_AUksavV#;{(S*%b9~2Pz=P7VYU=rSiFebm=IbIFU42`-DHS08=+cPV;A&4}2WYGG>VG>QL)=I>-nuB<u#jo+A6BL;>E%v^RV2AXvK70X4A|Sxp}#`s6%-?4yk&Ay4D+j0-<>Sm!_k9rbj3LB^}!`B*lq8%GG5GRwIEd~|?TK71y@Zw6;yy}N&M`xH-`z2fzCkAMbDd(;2Yan-K#6iRL;c#UcDZo1trlqqPPx!rojoU8+DLOc64nE-d(8SLvAe=Iot2gEH+Q~'

    @classmethod
    def identity_hash(cls) -> str:
        raw = f"{cls.VISIBLE}{cls.BRAILLE}{cls.HANZI}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @classmethod
    def decode_payload(cls) -> Dict[str, str]:
        compressed = base64.b85decode(cls.ENCODED_PAYLOAD.encode("ascii"))
        raw = zlib.decompress(compressed)
        actual = hashlib.sha256(raw).hexdigest()
        if actual != cls.PAYLOAD_SHA256:
            raise RuntimeError(f"payload hash mismatch: {actual} != {cls.PAYLOAD_SHA256}")
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise TypeError("decoded payload must be a mapping of filename -> source")
        return data

    @classmethod
    def textual_glyph_image(cls) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SIGILAGI REHYDRATING GLYPH CAPSULE                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  α-layer: {cls.VISIBLE:<64}║
║  β-layer: {cls.BRAILLE:<64}║
║  γ-layer: {cls.HANZI:<64}║
║  Identity SHA256: {cls.IDENTITY_SHA256[:64]}║
║  Payload  SHA256: {cls.PAYLOAD_SHA256[:64]}║
║                                                                              ║
║  MODE: Embedded source archive → verify → write → import → execute          ║
║  FILES: {len(cls.MANIFEST):<3} modules                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""".strip()

    @classmethod
    def verify(cls) -> Dict[str, Any]:
        payload = cls.decode_payload()
        payload_canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        identity_ok = cls.identity_hash() == cls.IDENTITY_SHA256
        payload_ok = hashlib.sha256(payload_canonical).hexdigest() == cls.PAYLOAD_SHA256

        files = {}
        for name, src in payload.items():
            digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
            expected = cls.MANIFEST[name]["sha256"]
            files[name] = {
                "ok": digest == expected,
                "sha256": digest,
                "expected": expected,
                "size": len(src.encode("utf-8")),
            }

        all_files_ok = all(v["ok"] for v in files.values())
        return {
            "identity_ok": identity_ok,
            "payload_ok": payload_ok,
            "all_files_ok": all_files_ok,
            "file_count": len(files),
            "files": files,
        }

    @classmethod
    def rehydrate(cls, output_dir: str | os.PathLike[str]) -> Dict[str, Any]:
        out = Path(output_dir).expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)

        payload = cls.decode_payload()
        written = []

        for name, src in payload.items():
            file_path = out / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(src, encoding="utf-8")
            actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
            expected = cls.MANIFEST[name]["sha256"]
            if actual != expected:
                raise RuntimeError(f"file hash mismatch for {name}: {actual} != {expected}")
            written.append({
                "file": str(file_path),
                "sha256": actual,
                "size": file_path.stat().st_size,
            })

        return {
            "output_dir": str(out),
            "written": written,
            "count": len(written),
        }

    @classmethod
    def boot(cls, output_dir: str | os.PathLike[str]) -> Dict[str, Any]:
        out = Path(output_dir).expanduser().resolve()
        entry_path = out / cls.ENTRY_MODULE
        if not entry_path.exists():
            raise FileNotFoundError(f"missing rehydrated file: {entry_path}")

        if str(out) not in sys.path:
            sys.path.insert(0, str(out))

        mod_name = Path(cls.ENTRY_MODULE).stem
        spec = importlib.util.spec_from_file_location(mod_name, entry_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"unable to load entry module: {entry_path}")

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        target_cls = getattr(mod, cls.ENTRY_CLASS)
        target = target_cls()
        method = getattr(target, cls.ENTRY_METHOD)
        result = method()

        return {
            "boot_module": str(entry_path),
            "entry_class": cls.ENTRY_CLASS,
            "entry_method": cls.ENTRY_METHOD,
            "demo_result": result,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generated SigilAGI self-rehydrating glyph capsule")
    parser.add_argument("--out", default="./sigilagi_capsule_out", help="rehydration directory")
    parser.add_argument("--verify-only", action="store_true", help="verify capsule without writing files")
    parser.add_argument("--no-boot", action="store_true", help="rehydrate files but do not import/execute stack")
    args = parser.parse_args()

    print(SigilGlyphCapsule.textual_glyph_image())

    report = SigilGlyphCapsule.verify()
    print(json.dumps({
        "verify": {
            "identity_ok": report["identity_ok"],
            "payload_ok": report["payload_ok"],
            "all_files_ok": report["all_files_ok"],
            "file_count": report["file_count"],
        }
    }, indent=2))

    if not (report["identity_ok"] and report["payload_ok"] and report["all_files_ok"]):
        raise SystemExit(2)

    if args.verify_only:
        return 0

    rehydrated = SigilGlyphCapsule.rehydrate(args.out)
    print(json.dumps({"rehydrate": rehydrated}, indent=2))

    if args.no_boot:
        return 0

    booted = SigilGlyphCapsule.boot(args.out)
    print(json.dumps({"boot": booted}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
