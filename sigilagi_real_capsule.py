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
    PAYLOAD_SHA256 = '9cb2c1309abf97e6e18a2b535b16e34a99a2f9eb9b74aa3724accd7620ede26b'
    ENTRY_MODULE = 'sigil_stack.py'
    ENTRY_CLASS = 'SigilAGIStack'
    ENTRY_METHOD = 'demo'
    METADATA = {
    "name": "sigilagi-real",
    "slice": "core-control-retrieval-pricing-discovery-registry-corpus",
    "version": "v6"
}
    MANIFEST = {
    "corpus.json": {
        "sha256": "4ce532e782550c58688830b685097c1bfb7b071ef7fed0da1f953826efc18fd4",
        "size": 604
    },
    "corpus_loader.py": {
        "sha256": "073ed3585e8219d6efa1bdc8b8565d36083904ea2edac30f4edbaf824942e47d",
        "size": 1177
    },
    "discount_combiner.py": {
        "sha256": "c8acbd07442bc95e74f596b08a61a73a0ca95fbbb58d6f5b5d7b69cffff24fb3",
        "size": 1409
    },
    "enhancement_discovery.py": {
        "sha256": "23eaf9ffa500d13027607278358ddc0be5546379074cb749e26b9de032a2ada9",
        "size": 1349
    },
    "proxy_pointer_rag.py": {
        "sha256": "bc2957347fc33c852c716e0470e2c54382c0479ae8a73da0849695f7b15c4351",
        "size": 1196
    },
    "registry_manifest.py": {
        "sha256": "dc5886fc2360659e367e9a0a2712eee9e0e2c7c488b8418e0f78dd87597ebe3c",
        "size": 1256
    },
    "sigil_stack.py": {
        "sha256": "8109804b8e020be738031aaf4739d6bef27fff650f69f4ab169f790641b9a3ed",
        "size": 2607
    },
    "system_refiner.py": {
        "sha256": "276f899f3361837e8e1a887ec3d08ac2b608405df19b4abd9c2d78f916c24f35",
        "size": 1024
    }
}

    ENCODED_PAYLOAD = (
        'c-plZYj4~(@~;qkU!*`*?DSF`_HKg)d7(v`21#*Wb{B$H;@WJqk}68B7ry=PH!~z9Qli%OUF#sW9>aNYI8WU#vZ|>&8UH4$a<N>jHzi~D_=~a4BCoPU<eSA3uCI$@eRBcOe6xrQK+Er1_4)(8{yA+$CK&>;eU){ROIDRE=Phpzq7)KdGkHAhssb+f9nZQ}06<!1H?SsW4ZjAUM!>qX#M`>5@-7p*g0r?sOS!L_gN!W>4!lkCv`vwV`^}<AkGxSFDOOJic#3AllHytv7fpKYmFja--5pt7i4r7WUtWJ;B$I4Y<f!4u>TO!E>K0y$G6#`z2I#v3FIyu++cl+Rb;C0uxt5iIFxP+y<N-a@AQ|Z4adP!k9~Mrl^XQfBi+;%tX({$x0>3%mi;}Yg=p4io<t<220R%{g{4tTk1JNEyFi=9vnJm*<-c+p;#og&$RkaKl6(GnH#4|iA={DtdQ!XNHr%6$zId9_n2*$c^ssl@seFqxmNy5aTu9_B@E31|$%1ucyb=uw(VrKw8!>xYP9&1rvn-_0I)<*1gd5qXcU}971=Xf|a^e-z?DcKw1<s-4OR3d@ufEAFuO_D(JVjnThF%n;bwi@;yq8ze|SL{<&a=j9Na6xRrvlW2`)}t^cJITQSn;?uEF00~}2O)B07(nF^aiW1DtWl&j5GS#=TZ^XHGtkq7G?0OHG6*eD{Ap6O-uI&5pQ`qK)s^|Xrm31>51T2ZL@g>TY!5K7t7F8c&7x<P7>4Z!IZ?MUGA@G&D-BQc1T8k;Wme@tW3^dy?f&8)fGeDcB7h69$}-~tB9B-BlKAEL^;mPo|3+IDJ9M&TJ2;^1r?0<!qP1g=t4uDvY6Usg+W`=df{2)C`2kK5<0bfm22KmHHD+kaJg$pa4kX5~J^}W<1Vry%oB$W0OiNbne&d;vV?=ZC6pDPQmILR;N!ZV4`S^EQbn}cD%TS~cxkBxz)u=X3>zbE&a6hGGyEV`{X=pt>+=h{Fjq!EX3iW6P-gZi;eOeS>^ER;GMeP0*juD(Dh7wEg9Kkn!TovhIm#6G*$?hDU2Y3}DXc_ssT*wSgSes<kVFw=hss0WbB~JwrMg#Sayp9iTIvU)c@^wG-Yl5l)Pq+HD>3C>-;9Je(7YG&FI_gGL4TOg!SWT-QmFa=g2B_O_5F@SITQr^}+r#m1ZU1U;ztQ5)`Pf-k+5l6-Q5_gH2X(-g=6Qn9+GpeC(vj^v4P&!-6M6y23>+`5H&s)V-L8f0E3_Jjoa<dI!a%JMkYc#*ChM980y8`%6oEnM*d+R-Mul}-N3I#~_#Sh&l|ec28n`INU1X~joS2$78G<c5{=pbAU~4d31RD7>M%s#L^VxHDb$J<Ih7o%)@=?5)(%TD2upXiY`A48A4s;NGq{W-ik^GVFtt(|$<AK2}&k$5Lecy9>^0>EQha6R0^jN0i>#aWP6!CPSvm)Af<8^DuR1bwWUMNyi52lpngHx;{pt|w`8L^Zn)gt-;(|xNFKdqs&ZdJR<kt!gE*Y-}_lYY$;+V(Lx<hW^(^eg<7AygnhVoT!UhTStueN^=R;W~Y3ft<+A^YRAcJ=O|}4&>R#C%XCv64=3~z8i?WHMA_hYUmrUgvtGK<cJ=VRf2LcPdlF{Ihh-g(or_M!LlgP8jsjz$X>13ccbHJXq-J8CK%xcfQ#`b2%;^xDmy+^pu+>t1r{~d#(>fN-iZb`(u)F8R4fh%#~Xdhb!7zmB==a#wl^G|k~o0TxD^tVx0o%*6XYk$8+aVllQr=Dg9`Yu%up6S;*g9Yz2=V)|Cb$<Cb!@k?Og;fQB;4hHf>;s|EX$SOa!wVs5l!kWp9b-_W&bv!CcC=m4C4p|F5E6KB%a7N`#^KS4r<96!Z}kVVVO>X$K6e%fLhiY`LInyFETt7ba&!|NUoc<?oL-A6S;5N1|Ng3D)yb90bNyd%e{9VKp|4j%Ynl_e#)E34b0^P%ot?6Avyh7av62MwFaufwti^IXBqIbJy4xN_1Z+0SW)=1l{Y{f3Vi*#JS3hPp2}&%C)ibv2IO0GxqUz$e`}mXC>s9*B_poh1>OVmHBgTa~^cuvDl6VmZMpA&(b#L4a5V5Sm7Mdg-&8Fc?y0>bMkwK0a7zk)yX%iYCwkX9uo$CPtb`<6uG6;n<{C-8G}Eh7LJ6h07?Tq$gP#l%Zyr~<48&EwJPh=cT(=Ci0+BP%NQjc({kbQa29C|@UlAuR~DZd5pst28u4g3G1{lJ2HA6VNbiDzmx0CtdG{6k|9;wnPzYYJOHcZ(v~b2jjoSh!vfku5V43O6l`iJNN&!?`gB10+US3^YZD&_FjRRO>?q?S`{sUJ*adAILaQfTj@*c|=RHNYm^>}p^p1i))^?X`+vwlx2LOZ>oBQf=Q3e$Q?CqOk~O@lTuedE6>V>J!xpEaE)`=6e}vDW~jofZ*C+46&mMPG3!@cP4#6IDZ*q*~z$?)IezLPDtG!wBLctID>iii<wPU+55b(dYaZlSci3j#}eV^~t><w4Vkn88&FVfmZWy7DjV*7N+O;EYu*47w9yRQ4JhO$n|!rP|R{>6@WvA1XvP#U2VNjAzz;1>*knaA9fb*<ko0|!6}g-)@xREkkEHJ$brn;hmCP<$%~dKsh<$&XHG!E!tt1p{F>miXW#ySR2nFP9Y2be*4{Sm>KyT?^={nLGo0Zx%{HKBOYr{mOc~Ixw&%{$WL5ueJAc5Yq|}@3nL|W<-N{1pejA>%O&kdXXErmOH(ftjvp3<SH9%uY-1+R=pW|Lfv#j~Cn0YtOaC;~>Db(O<laq!9h>d~$N>9J2hbHwM_qGRC-KKBkv|;sXZ_C7B@U=Mfx=GM7YsNuF!#mSP18a}{>_BD0#aG;}r}wHsx2v&QgGn=4Yj))-bpqFGbv04w1a?s1%BwpM6MAI4n&@o;yMtm7wx}_qOt4)6g=u1qF5@~?O=fq3ndJOXSzgblIX!4vIeQYggrBpG{dL1;5z?H|=G026733%rH5(K=r3zfwX%kf~!)(di4oTtGP0s9Xiu?J4ZR~+5OjlQz5zSCm=%czaySci=svf(zE35q;sZk1m$CqLFKhk<J(7F}%ON)+fyBjJm6_FX^h$pdfJ$8$}^4XV3IZnk7;~SNEz~)-59#CI?>j4{okKp6qapJQ$v~^l<w{r(Cwle}J^P%Bf#D)~dOzW%`FC42!gm@x2K8JQ?kX|P@qQ%449}itQ!*)2$!=bCCzj}c@bT9Bz8&y)TUN{v8ZgbwF)w{0#2CnMvDeUSjTXJQbZmzsA#hy|OHRNTV_npQ`sDn{;DZN+?7Q}jrbpEN|*;y#Pw~1Jinikh;bUw{s@ahGgFk3V5225A=NPEQ(cHB4b$1=?f())=9)|dSzVn-o7JI-->i`MF10&3d%ak#DhrP=QF_{}(ZJ9$-TMI!fr^to*KaMEflnb^_S9(O=|S}aFXch*-<`qG2N*+PZQc{J;X6s)=)mnV3v52+{vI?~`y^*M$R+ZEWXa#9nBxa0%Eeq0a1jK06gyF)DlwJM?y*~%6UXK1jI{w|TCz_bRV1mvJJl1&n1AW8bEtQwrEEalyuXamJysPfveOMgmgn^kq6>*bu+c>mO<f|ETh?E-H<%;YhJ821bytn*@~0XgeSmA}J=oMtyb)Rt)~+kfn|jJBIM*F4ClO^t}jCYwI2QL;Pr0UGWXq(Pp1$|OVI_)$lBYBV-kjNiaazXl`wQ6H*d>q-$h#rLrOv{_(tPd%dH6=Iz(2N>&{Cq1R7kDloBLi=Mbh`~7I05swJcTuXVt(CI|*sYc%B2L5UikZp3W)3h=@3U__`F`~N4SmW*Rh#b^>mtQ!6oUjZK<)wlM$Qm@;ME$26WgcIPxcJg=Q)D(&(BRi`aet8a0*+l7FdR<^scO39~7VeU6}a4WCqr_e{zZXGV+8Aj5Ydoh$Zsrzv1ljoB'
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
