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
    PAYLOAD_SHA256 = 'baef127845614b3bc89f1374b0b270ead8b5aed82453d5e9c831b016d5074754'
    ENTRY_MODULE = 'sigil_stack.py'
    ENTRY_CLASS = 'SigilAGIStack'
    ENTRY_METHOD = 'demo'
    METADATA = {'name': 'sigilagi-real', 'version': 'v5', 'slice': 'core-control-retrieval-pricing-discovery-registry'}
    MANIFEST = {'proxy_pointer_rag.py': {'sha256': 'bc2957347fc33c852c716e0470e2c54382c0479ae8a73da0849695f7b15c4351', 'size': 1196}, 'system_refiner.py': {'sha256': '276f899f3361837e8e1a887ec3d08ac2b608405df19b4abd9c2d78f916c24f35', 'size': 1024}, 'discount_combiner.py': {'sha256': 'c8acbd07442bc95e74f596b08a61a73a0ca95fbbb58d6f5b5d7b69cffff24fb3', 'size': 1409}, 'enhancement_discovery.py': {'sha256': '23eaf9ffa500d13027607278358ddc0be5546379074cb749e26b9de032a2ada9', 'size': 1349}, 'registry_manifest.py': {'sha256': 'dc5886fc2360659e367e9a0a2712eee9e0e2c7c488b8418e0f78dd87597ebe3c', 'size': 1256}, 'sigil_stack.py': {'sha256': 'dab5977c7e035d9b812bd03eeba6ff80cdfc5e8c794a052749b1bad1c3282f6b', 'size': 2705}}

    ENCODED_PAYLOAD = 'c-plZ+iu%N_E!en7c!t#E8X-#t%3$^HYkvGi)67cl0eYp$euNCnITgPhW>renHy)wp=|HA3S#kc=G<>{Mvqa+M9~gSpA~I=!y3w0-6`5cN8Z*X%Z@`oaGGU=)m_Vbk~dA;=RIp1v2P?ynfG~7<w8(lfb1g;(w{ok+?ux^ndnpUGb`ZlyXLfS@ZXPiP2BR5^6kI)K$CqV9|5r9@zYSz&AuV<={RdS>rWfPnqEC>@|tdl=()PRXHDtce$A@^ULUJA?-flS_fJ}UjlZNv5T7-y&$3w1>X?wLx8%3BF$~}bpRYJDB{ov5oy+KfY{~9`gbcpCEHi|b_)>zG8&9^&G*)@n(WZ>?CJ6!v&~Kc$B(+gBMKRp;V7^MLL6Sp5>_AJ>7zc+iP^%a%wG`%QF>p?s9-c}Ru|a96;^)|MDIM6x)zJumpBoBb6cA~Y{#$mG7*=RSvfYw>)KOj_STw;SMb%0KY#hGJSR;Q$q_$Sl_~aY1zP?^vCn<TI_&8`ar*~uzw0w$M&6-$I9O)qXREsyGBWM62&zYd)-?;ca=Pi$q`)Fvy&|$!U2`oY7(~p+Z^FHzv?_0=I#g)Y}7hjv&IN0Ny!+nI&1=>(r!kaV%g-lr}ya_@{HCZsFv=E$P9Rbx<5XgvyU{=HsV1Dc=M<}hK3DDWoB&U%08ZuGEJ~I9;xtIDiPo&wW;78WvRc2R&Deof*khzlhxWRg6X^4upAFk7v4#;`mL}^5uySyoA4JZ_yuauu&nCksJZZmi)bDx`2-;cz8Hng0)YUrD+1XN@qbQ6)xO**H#&)p0K$}NGRG5LCcUi#H3MUq<G(mvit1@L%FGp+HITqor1mV7%2PebEkY?xw%27nY3^uC_;m2~BO^jix$tZB)B8R8fQobJoOI2tmDg40~Ijl%Jhj&dmx5nv~AWKe?pJBmq()!;NG1&7BQ(X#?7W_x51ZZqU(CmRG3)QdIn-IEIVr72JrI^j?{MSe@4A^tya1m#~LHM&-WEK#+8kUr;N;qM83=yFKrEidjUxP^3OYy(&+FT;vhbeFO%JYV^Ny#9X`_2x-My;mYYGUAK^>!2du4dNLJ`Ur{umIvuqN;}|KLjf)_Vk;RaTmUyO)rIL9F@OKrTKW6)-3OKxn2}_!@dEGp$ZCdl)m<;Nen{6=tT>_fa4H07sDZDi6lA58E!aIhZL7S#DRc6$A@SA2&K2>H5`3TqIwZ-g>KJS?b3@!doU*QkK9}+gB>bxz^k8ED(OIJ#=e9689YTY-y>?F@dgr#LeU8hgIo>T9zoV4DD<MC<`|#o}9C)yGpe@3^w}}T`cO16Uk>zxe-HWu1djs)UAyzm?bcxrP3z|b-(wux5us~`?+Ah17yBd(;+vk+QFBv9Lfg<;^_3p9nmN-|C524N`D*;^rYz;7wd#9U+Fy^+!_xpDc!nW^HxxV|CmMFYjp`=q<K0F3zm3IIyhB{t5d}>6<8QyEeljV|8+tM0j-;g?gh%4H}8VmH@Yxw_NGTTfj1aHZ8p#4@_xR9W9qbbcQ+e{Ey8+i#>;zU?^u?*HQpxPUxsK?!Ay<Q&{R~UCPOU(V^0xy5yD%e~+juM>zcD;GTZ49c>@PK+;uak2ym-?AcD{nFHX+`LyXLK0KdJ5BSBO~A-b04R-;QRcP)p^5?P{seMj`fo!^sA=x;{0PdoMsJh+W98pBzjt_TJ)LSvg+N3UuLR?Z4wq|Q?tIl2|x%aRk|pm@~(=u>3LgS*%E)HOWc+1`LB#l1L&&!1SApPW4MHBtO$VvnqZ;TJY0m)TwR2*9AAVQr3nI^XEN4piPawAcZaz`vCCOhz)jos8L-5TdbjnD9Qx%2zV1#X^qk9ZXMc}2I-C*-YQ1Jv7YTi*iyX*&c-k3vj=boJLe3Ln{md&!xN$sXQhrVF)vNnIpp^!S;K$FRrL}ih4PA+N)Ox?}HF+oQ+J20t#R1gf7TiY9oB{pna4D8%tL(eOa)8ZAsW*oUK~#cd@ob@ae@HI*W(7u$FBmgfcHJ;pW1D0)8W5O)(DKFopOaqqjehbU?6?~ZJnLi4x=HJ&!Idd9PLDX1HL#!M(@*N5X>g|#?2#dVw3~XvR=qkn7%><^gABcHR+`M3X(@5bj7j#NQQ0q_G=t8zQ+36&QLxt7)>qaH&T4BrQ`8K0RLnN0lK>M+2>?IUhd-dM+8i2lTDMN>xuk%V*T_#};I=w-cUP+8m<7lOeEBOla3P5729JOScSUV88AOOveS^C|*aXsIkaGhN`A+uAS~8rqsI58pHS8PN4QxSso;LzI+d8mceAJOYR_lG_mVo4?vdXZ%0<eIn(npAnH3D8jq@bW;WOEz<pz)yTE<w)Hjth)nn0*C=EiG_5trS2wj$4Fm-{pKo1ScuJuuk7_Nn(2dWzR|6aE;9ddb_?(<yp@bi44Hj`WmMXIBniK#{{W5@&WMGb@IQ`dOgzm%DOiW9eq4tsJu}`7Q$dPtLeL`$wJ%wP{-$`#V}0hNG|}kG!hPghWhXjb6zF!01itTV&yg-UV|mi08=t{Qsz+5nIuEvct$572~IPOy8+2>vpd$~Zq~-0-k^gvz0@$qjt&TDcaIEXQ0?5euf2^8TB)>Xwb9gfJPR4{4c*KOs(j0D$s@C;REm*ve_`9p^EthMQ4K?bSPd4$dQNqltKYfJu6(}`z-E%RorIS;e_X%D0C6<~Z@}}^DAp=|bVGYaFqNqZZ_Mq%32tMp5pi&lTs$@MMwrfOD}kI1hH>~O2pePW-So}0M?42r=#)%9Ky1sLJlz``PnPWH>p(P1J{^|Rc{Z{eG<_Ms;+ark^Bygx5e2KRr@J5w>pEvmEJGTyp^jrt#Zci)%<G}zWF>PzVt*9?l@i;|RXNn1h}Ei8*0`pJ;7klQslRKa$guyyBoD2wJo(KsWFX7z;jcQMRqfRK2iC`m!9=ys(~SI*4!USN+iaGUc6k5N*@f5UZQOn2aXk9J$;Ir9Ed{V@Va~ajOI5zZxu0e?M%0dLD&K$Zp`0`~<+n60=d+WP2wuz|b|~3{oR<=`*FFk$jAoE|Pfxl?%Xua*Rt(f7;v_H$?DGB&f7-B*9u<-E>JiqT_Yuwz)gyUEhFIsz0fq_IKz)I_8tWee;C3vLEtT^Qgq3G0fF{u(oA3b7DrX0<2Q5h|IZfs(7Jgu$nF9=R#A@eTp^vuTI1Y{4&h&9zmE)!tiv%(t(*t~`-dX*~t8?Zq**+&>vKP3%%n@{NVQ%a%3@*|&oPx>K0>?3x-j%oOKndmF$khK0F|a26%ao`u(?GevTBBblxD!AB7l~4ph5'

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
