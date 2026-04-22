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
    PAYLOAD_SHA256 = '15cf9578173291496456227accdcb1d0b6ae9fcb34ee44cd02cda12701d76738'
    ENTRY_MODULE = 'sigil_stack.py'
    ENTRY_CLASS = 'SigilAGIStack'
    ENTRY_METHOD = 'demo'
    METADATA = {
    "name": "sigilagi-real",
    "slice": "query-interface-indexed-capsule",
    "version": "v8"
}
    MANIFEST = {
    "build_index.py": {
        "sha256": "0adcf1773d9b4afeb368bf1f5611790ce2d57fbadb9d77bb055f0978c08b6a32",
        "size": 605
    },
    "corpus.json": {
        "sha256": "656980e88297b4dc91b07352daea00435f55ed2e64e5c1a3bf57294fb136a330",
        "size": 604
    },
    "discount_combiner.py": {
        "sha256": "c8acbd07442bc95e74f596b08a61a73a0ca95fbbb58d6f5b5d7b69cffff24fb3",
        "size": 1409
    },
    "enhancement_discovery.py": {
        "sha256": "23eaf9ffa500d13027607278358ddc0be5546379074cb749e26b9de032a2ada9",
        "size": 1349
    },
    "index.json": {
        "sha256": "115994d52464043cce214a3956f4743c92b85b0b3a338e297cccd9754b854311",
        "size": 2387
    },
    "indexed_loader.py": {
        "sha256": "ebf70ef6e31568ff49bf88ea1b0f5b6b073d5a0c6d8d2aa0176010bbde0e40fc",
        "size": 806
    },
    "query_cli.py": {
        "sha256": "ce5e7dbc3c7b0044403c5a5004f9d9c3d67c259f62229fec33cdef0759954dc9",
        "size": 573
    },
    "query_engine.py": {
        "sha256": "be596a022d114010f52e0d4ccaffe4cab1514d23e61ce55243210dfe055292d0",
        "size": 748
    },
    "registry_manifest.py": {
        "sha256": "dc5886fc2360659e367e9a0a2712eee9e0e2c7c488b8418e0f78dd87597ebe3c",
        "size": 1256
    },
    "retrieval_index.py": {
        "sha256": "bf724666d3f645985857697de4b463e48bb9a2beb5721095cab053e86b72d991",
        "size": 1266
    },
    "sigil_stack.py": {
        "sha256": "5ad35efde16c822e12a1862ee03e618f856946cb59ab823332a6e55a8b5671bf",
        "size": 3158
    },
    "system_refiner.py": {
        "sha256": "276f899f3361837e8e1a887ec3d08ac2b608405df19b4abd9c2d78f916c24f35",
        "size": 1024
    }
}

    ENCODED_PAYLOAD = (
        'c-qAqYm?iy@vkt-hma|czO(C0Myb-cj+1f5aZ)?eFOr7CBOx7g6v^;$KJ}{q-rdE600`-*)M@;|CjpCnW3jt{9%k2lUSx4zX6!zy_p|xz(@&oCZS&+hFQ2gT&a3y`O;tWym7Av8d2zhyyS`y@?B%<<YC10|%c@JdyeivOxhlozuWeO|C3Vu>6#2D;{~5ln<Xl=cb>GHCm1L}u5HD%)4UGvnVlO6E2e{Wb_zymY7+3Ip<L#2X^aJnWYgp9HSEUF4u9KE|3nJ}<1bG4c2T{Y?s<>l*5Y<V;%8tVdmXK>$LMxwms~I1TNUj-&tom*Q#`P$nI9yhxEx_nv`5KiVLh=281Gi;Tw>MP>3v~H_Ns``2WP!viIfy<qdB@_8-FH5p!GFj_l=Zv1^(EGjG+B0wr=iz^4&z(4Zx_EbJqyBNAuH1=%ggOzHS4?0#h0s@m=rwL4XD<a#KmC4z%NSgl3OC*fUA_r4jpB&0L8>H8YYfcGhve^$w6oD_ie{^ukQ2C=Y|7pvryMIc;pgSJn&_!8E7ERGr$9%x5d7`xd3RUcwEg;4Sf20oc<A<6AXYr-lj_XmbG40dKv3jv&+l8g=w$d@2;x?KCpY1_UO&v*y#<d$w0C#05v(ROG^A&H&xcB`E|j(u1U&vQ#HFb(m2?$F3FNEK`tIvvm)7phZ0Ae)dK<^!lPmdihHL}@5Cf{I;feoT??{o@{)NwU<-K4%R4Y}1rT?vX;G9MZJu{~;=hI6%9NkApp(W@#&re$cb61-M*Di2WCPESN!RAvytrtRty8?8o9ce=)fKoHZ1s09zW2ytz%}X{ybKHhym{3fMgrU-U?M=@??6UrA#}wS{FJ5WWZaVAapjhAdD(ppb~{5hK~)O3D%a$vS>C2qUv_a??I2*XhKJB8p^{*bTv{Y8N+^KTkO1lSHEcyW`v!Czdf(<L{Qsid^Ud~+TH{v@1Pi{QS0xPrFz4|d_{Lmq;0hwfevUDc58+;&gO(fq^%gX%eFf2bnBG97>Nrgk_e&wZz>je_hBGDa;@EFlv7vbUwkjn96zO0*YJjPBPGT)}M%NJkmTMJ30bi13F+vl*(8G^&L$=d2qNJ`_nfdr7Z~|aF^aGuwFsh)~_SYSluMlb=a%hMpXo-xm)(8W&A_vFhQpnM?Z}6ajQ9|KMl!_|;L;q~}KGt<K0MLoXHW<$q5~Vo{(H9p*Xhj}=Yu2O)HnZ@Ms6vT=t%1LpFOYxkk+vc-KAdh>mzU9H5PDAo69+5C^fozc%g3le!0|c7fexY%g?J-6Eps5`2g$#1@vEk(8h-=FR@wG7ZWxRWk|6i#2gT`OH8T`%TF6kvg~BoxUzl1t*u$8^)eLtRh7zKUUqTlYGNqvKixY~}q`<h+TyUIq1mvHbKvFCOQzE(mlTF8?q0o>8bTBk2asf*f5c!3_6ZfQFIYMT)!QoI#ide01Q--qx0b*Se6E|2-E_G26_QQ4JqXu%IFwe>xI71koFq{sYJ^M35y&1<<1P>|p=`r=yK<rydON*<LzKlwEn$N93M6pT4RDE2JP@r7Q@rK}Q02<*}gcKqbZ5ia4v-AcJ(^zOc^ezMM>xK8s+Mbfe$-N;DBQyYn7^n9^@=`E<7Qd}PhdY+#n8j#@0jK+|&l@zP6Gg)k%E}SPOR>vEDg<_FH<;daHw=SPz5}N*QzA(DuxyA%$PZdHa0IBcHSoow3V2<nC=0VVB&SHWY=ZbdUAL^cgV3m35u!v<eek-Z0SkY{Go;L`n)C)z%!XXqnG?DrfaNZj{^`E*H}C2Hs;K9WD(V#%VMrNyRWU(9Z$J?;rS!OVz_I!iTx7tO<&<7``*U?6b4HBcA6qMbo$fxcEX9aKxyBjZ^CsWrc&_T}TcIDw+o6csqxV2{-GYWn`16>8l$4Z$K}otOlHGNdc=vP9zqnuOBCbOZ2ZTWDAQ+uG5*tPCp&o}=P1-Y@aqc|})nLmLe^CwSrR97$%Iq?s9F#OF^W@|q99I8n#VKdupsJmrUOQX5Vd-fJ|BOo27E>!We}|l^>^m*!|Gj1vQVxYScAfw^>`UItGhCVD!lC8By`~sGxDHKto)T#*^c^u?atc~g+Nibh2rp=13$yKh1F+n!6Pf1DI2pU)dgn?zLME+0-7ISNpCO`hn(1Uj7&?Q<X5?JwTA8r#C>EYUR|bp878F}=x-L|JnoL54y6Gz@7ET5~%lsH{rb{aV*cl6WusUY}1j^~)B5Y3u#!z_%ygE70P^f-tPBNE%AfH7?9X-?Kp%Y~K0(G!X7KR^aXHdWcd^&cK=A5CXA;URikt4dDkYUI!CJQ2xnaAMu(;H6~Eh+tSRUTya3P(D>A3L+*;JkM`)rzn#?}m=VYt9D0x;ob44aFrLlBLeE_aCBpv@JV;%d5FzB#3zZ38uoUFLhI=cW3F=Of{E}c4DFW0?pVY0Y4a{^#iNm;?2bGpwxd`b>CqdN%a(WITSRgHbmlKHvm#B3$5K!#0(RpqnkM7xAkp4pt8#N#ohSUO)qYQ7&)*2yQ)l?kGMmqLetJI#4r0=G(^S0=k59y%X}~Ket7@WTd%tQm8G4<vFxG%*AG_RZhC2`il)$!eI5pkQg4d^_XU`vBLO13fb=av#R{iXW}jEcB`6>+v<dZneK8swMiNq)NXb8zh`;r$*~e*-f5hwWq}kR<11F=sr3ec}n;6WP-bys@ap=YOuixX~>C0?F+<-bIk?2LUrCjo7n(;H%rcGWWPvA=uvqy4zFW<Z-eGHf)yje*E3h)(zL#y7fq6P&2q;+^wmfJ^`UR-oleQ}G6A;z#pjxAS^Bk7B7@l0WS+wZPHf@<U4<WT-}m9UAz4k+=)To9o@NTwYE07L}92{4A@FjVwqOcMCGAfk`JO;yLY3mT!1#znSvPtMT}x8%Veak<SMj+I*|K0ZzpS$UR98~8qyfbZlmMREnp&!bqTtOGQk_)(1OM*%s*D`NflL7=#pTa-gZbUvbT{Q6Fn&x--`2u5@o7K(y?RDe?m)=2ksJPD_uD^OVW42_-^ea7N}M<_m#DqW|ZJY>j^7Z$%!%aSI&@eLo;-A_E>u)FsZdaX+eu_@<V0LK*wV8v<rFq%g8a2Ef%CWp+UV5N^xfq4g_1?Q2LOne~EQqOhPgIf4dB-2iR+`5Csv_nR&`A6Ng*iLx%{k7t7iV<6i2fSq@<JPD(YNU_w<+%f*g)Es3okqxW%dV*)ft9XzA)2!n>bB~_QIZ=iuh!~>>CIoQ7QwyXY!M3{PQnPTPQoaTPeSQ+m;>lAl95;0JnvtR6)FoArvk7C6$4B8M%)vAmlW+WzHate1IUiT9n77j1t}7VHL+k-L@e=5T+@Nf>&KmOsmV(lP-H}W%*dkg%5xu+{DR=;pWlAKlX8xJJc*Xj-a6{*4Ds;w1{t;KA5YkiULLF6GiE?ctxxTx(JD2!KEA=mr1;GG#3sU&+#fBJ^XuT0Zx&!=|AaAv<F4x_D{T{uF14*(;g1WkdIoSjX^<Y`yvufZp!QNyezYLO!%I24lm*LrREhH9#e}s>8g(814eB&ccMK|nY>=m`ZdsZCoB3GHQHn8K!{fFcyZ928M3`9DkUK}={Hss??gz{D!(p{r%|3%{7;453SO8Q1AAs>m5Mqzox`3oI!1H*(5g6~KMDp=i+B4;;0G53!y-{KkPW>qr9!0HgK6>OtC*i?<;Dji-G=SQ^^u%i(dM~J+KuKHB6)LU?A&Li%$3UEkC0|aVj|ONR9}GQw#pM0PyNWJ#t|$>Z@f1Rp^sEH;UqESg?_;(^5(J@l6_^rAYEAMXCMHN2&P@){YTSE(6;jFQr&5Sfes%IPcz9?j7;pi#@}fk%zEUhc;o^nf7lC_WnFH-kpkK;6u=R3&b#=9NF3~UA_?ls4eI!e$?)S0QjD|x0flG7v^m6`y&&E*mi0w0E;IlRA|LO`${gW5XsJx?h%t9&Rf?4X(b;FD~?wqy}e+8=5^B=38JMS4iKmQ;l$NMbxKAxAK@A#m6aB4qT9cY^`IYZ-ZrC9BJ2PHAM-YuP9Y7Wo+Ro~Ni?=RbszoX#Q>uw3C)wBAcWpowJf7B}MurN*F+wV@54HhHyk6;INFPxelEznA0TgxL@{P_YHw3+%F31@ANny{t~jY|l#gBxdTS84gDOR2nFYX34qdV+6?VE+ok{CS0wbJJUVlbjJi46{Y*NwU6GeEC*oadjEev+4yVe|?$WTwP*k3?Ftbv=_M{e_ajWa4rSElh)IL)?Hpd*XW3sxRT0qPUMKQM57{P=}yCCtbusvC@5Xe;vHbeo>e+PT^#`j*yzH<iOSA<9Y9u(&Q*gOLEiyj{9?$>>3DK|Y#T><p=P}W*UQs|qZ%HHQrE1|nQN-X3aM2&unUAM3U4v?_Vn1ztazXWU*Fu6p(%V|HS<J=cT#S9w9X_7b_g;Ldlex@++&}aXTXbbdvDxIl)uQ(vE%;9hVB^OPW-QB;0LMzMZ>3Md^?+M8};;sY`|YNx2gqku=^nfMt;@i#452M)<dX0$9bUgSv5px{$Sc(IgxlLxUeFc{B_0EQ;bQvW?%+l0>5-sb;l4O)C*`^rX%UF(cH9Kw4>TEIQdTAc(kcuR8rAvNH-4i&GcNlz|x+vv*N>%Ep@C>V)W~VEj0!s@){>25UpP)K02@%*5cTVA$RCI+H5l{cG6nM^d(>C={M@f5$SO2sl7Uk7}Hx>;#WK}Y*{bKv_K;s{iRj8$+vWiMnUCiaQa5@=w%qO`KR7>jk1Mvs-v{3RdtauR^#_`+fPOYKG(ago8hNjm^|8jC%m{Uy2ROzI%;rkIk1Fe*GJS^aN|3D>W?nS;H=p)KO5gLz!}-3<G~swyXP-3&|Z)MJ5p-drGP?MWQNq9XwoCS34Z5GPc^U_=R^+C1FVOl8~advh<*csSjWrp?r3<uAb#vc&ll(ctp2hA(mQO}0Gh!4!a=<)kjhyC>{>_?dfLyDC;Wg+Fb5b=2bsDBa{Uwb8(J{4s+Nz1>mtF{Fdmc007Xss8ydgG8hF)yQ$=ha0yo(cT%YC$N(MJK>K9}u=}Jz)<a~kVm|XAN+r>r+90$`(MzXmlVdY^*Cx!SJIu1uXS;cgK{p!Pi0lt?}V*'
    )

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
            raise TypeError("decoded payload must be a mapping of filename -> text content")
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
║  MODE: Embedded source/assets archive -> verify -> write -> import -> exec  ║
║  FILES: {len(cls.MANIFEST):<3} entries                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""".strip("\\n")

    @classmethod
    def verify(cls) -> Dict[str, Any]:
        payload = cls.decode_payload()
        payload_canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        identity_ok = cls.identity_hash() == cls.IDENTITY_SHA256
        payload_ok = hashlib.sha256(payload_canonical).hexdigest() == cls.PAYLOAD_SHA256

        files = {}
        for name, text in payload.items():
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            expected = cls.MANIFEST[name]["sha256"]
            files[name] = {
                "ok": digest == expected,
                "sha256": digest,
                "expected": expected,
                "size": len(text.encode("utf-8")),
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

        for name, text in payload.items():
            file_path = out / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(text, encoding="utf-8")
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
            raise FileNotFoundError(f"missing rehydrated entry module: {entry_path}")

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
