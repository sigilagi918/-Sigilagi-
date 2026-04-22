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
    PAYLOAD_SHA256 = 'f07f8bb6a586d586410aca86cf63c4e11645ecf00b21e578f852f5e2eba024f8'
    ENTRY_MODULE = 'sigil_stack.py'
    ENTRY_CLASS = 'SigilAGIStack'
    ENTRY_METHOD = 'demo'
    METADATA = {
    "name": "sigilagi-real",
    "slice": "core-control-indexed-retrieval-pricing-discovery-registry-corpus",
    "version": "v7"
}
    MANIFEST = {
    "corpus.json": {
        "sha256": "656980e88297b4dc91b07352daea00435f55ed2e64e5c1a3bf57294fb136a330",
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
    "index_builder.py": {
        "sha256": "103adf62c7e4dd5baa78190851d322b13b380b5579ce8135b369d2504179f57e",
        "size": 1220
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
        "sha256": "0df1a682e7d485084dacf3d13dc8f508e486a6d1cbf55052959bfa58dace60ea",
        "size": 2933
    },
    "system_refiner.py": {
        "sha256": "276f899f3361837e8e1a887ec3d08ac2b608405df19b4abd9c2d78f916c24f35",
        "size": 1024
    }
}

    ENCODED_PAYLOAD = (
        'c-qw(U325M@vorjL&%h7>`O1xQK~d)a>=A~xn%A#eUUUAnuKiRD3T#apH)@=y}Jv51V~Vp+vK5_nV2FM`;Gkqj*F~n>Q2VL$f{f{7wb*Q*b)E7*k+MeSt9byVhPW8#i72x0%*QjL<XSckFEOr9e(~HZAB&-0<m3{b&^X~l`Q8iZ}y@T5<W9|*xyzKJn%=Jb*%t^w9M{dP0kvA2SAO0b!mw|>!!-POxzZnwM|;eUDfPmY;myXZJMWTid-Bwiy}SnMscKAJt5#JniWe^Ja~nAt3R@RT8bT)tpr(iqU3B3YynTAeBfnU0mK7uB#I((cp=&Y@h{u7<xG}oE$=H>4BU^Daa&a_dq@ibGQjf7BpY~sN;)a-L~+%mcV6*+YO2Qrt1D3gOYH4e-!ZZnaE<zII2r<YV-*MoqUK<*oB{f74>B4HwOvz6RyRBol50ycFx4Gb^76+T?Dh=VG*u(qrrd7IMWp>SDXKK*O<W(qS$9pfXGyZ_fCru=Ozi8bX@Q5bYDt}PQxZ&_w)cg&H2^=sPyMAm)S|pIAHES;8?mp-L&RQ#hBu{tkDFsd|7ArgCHtCqc}=V=l}z9lzzUePO_D(JViz&ZF%n;bQXBSfq8zfTFW8%^<a#Ck!v(Pg&sGE)Sg*pEG?{~mnjnlDF00~!2O)B07(nF^aiW1DtWl&j5GS#=TZ^XHG0@Y5G?0OHG6*eD{MV#t-)}|1-&F0lRafS(nx<-k9avLHiCR=x*bZR8tYgHd&7x<P7zX=;oT%Fv8JEF?m4>Hzg8mxtGOKc+vDz%Uc6ap`z!gqJ5x@mFZ<+A`kw>fmN&IsBe5kqNf1^E%?K|1BTX13ak9R-5p|xX<t4uDvY6Usg+W`>$UPMf^d=LAE@e+1S1EGM}8Z$Iy9@j-I2NGjgp8&gF0-|>mC%{E0(~?!Uzwk`SF`_vH3PrwD%YkzfBJB6GeEc&lx_L&7XDCvLT%mT<YE&Dib<N8>I8JHVQ4O?C8d?u8w_)U4V<MfkLcN-Sx1$njpBBY;ybbJc5j&p3F@n>?QDO;^BY4jbt0LXs<|%tzvPXyK0bWH>T1K%h7czq#)+SlCzlC)3+<1qKQlx?ytbzJh-oS@G9Sz}6#kw#1H9^%tq+9*mbUZXM@EgtJTgZdjJL*PM4dlKhculKbmFb?70o2d;kVUMY59mBgwu9~8+VR!k{#uJa7h`8bX#-3RTXkU6Y}5f?n&$~Z>zIv?OGmczG>p&UkI)N1Zs0^|ZB$KBcDF5<uh42Ba&C072m`f3KoWMtP1ZFHWMp_tC<24h@kxwHjjCB}9l36N%Xe72tqjUZ)WAhCT9K_*uw!c8WC*tK#0TTVfUUuF5oqKeGtyQ}#%G_fo9pZNI*izhQH<inl-^E23Gx&*D6RrUaiD|fBQ4&9j^r1Hx2}|3jT;8*AVX03^s(pk<Oy$sg&b8}^;o9jYg3;MinzNlSP^af;SFoZR1bweyila39!x3C2d7v^K=tGWGGeJnszvkxrn^>Eep*9k!>SIGBUM0^tNoq0C;gf?WcD#Q6!2-0^eg<7AyptiVoT!U2J4xnJ}TONxK2M>ASVj*yu8PJkJYrI19kS{nW6rP0(OY0uLfe@7+O|bHS|qX!p>zm3PhJwm7rX#)6UmPPUS|Vbe7HTv2jSW#v^tevM*Nb)6w=cG|uh~lZ?;+5MulVf@lk_`i?gh=y1<-fgPJ=7;w5@JJFyay(pkW#pZx;e64r6Zu`Jaa)+&Kd(SZ_i9I-t+x|g&i`8;GL4LBLfhRycTLYgxsetdx3}xXX4#_FfJAQ%qKi)!X@&KXHwjxA{qWZwvv;hl$uDU@i1hac+ryFu*Z~yC$03&z7TFUm7zp@wqtD;^$si;><grPlFMehX)dJT#&?K4x_0mtexaFGF9E@+g{9-gZUQ!`@x{;jq0=gZv(mSq@`sMdIf_q-N+fqB(lFSUMHjRT_tdJpuy5;Ro8pQjYmOX;b^gDb4X2NAas73W%@Z8$B?4K|A0Gz>{@J5fA;7;$mL{vL_^UD416{1PoLGH6Ebt9%IFZS|g);$J+#_J-=~AymT;J3eb^*03bTNm~uB6GzL>|M0gUTyKx3&1SRs2r3w8$v@zrf$By8#<CHy#}aZG6tw7m1CG$CsYx$7k<9nZ=PO;DtYMvH=b&C5%p=E>({ClRg<`~po~9mL;ugfPkm_M7=>p_6VwR%-_1tOMmXod(+u9X%nDAq!y~BT~I|tBoqAr+eGXa!3P=K9jK&PCL2G)uJ68BtBjDMeOg3a@In~lp`$$6Pz){rP7r+&wYH`Mqy`@Z*Z9M(7FK=0}o7~~!}Dz2-t6(tm}ldr?l82Y>bpF$5U?P@V_4(^+FMN6O&)GDC~kxH$Tj><6EyX&Z9(y!MDhc?lk=DxqE$hC6ak`=rRdXrCUPsHj18-i0<8aiN^ZqQ92%-V#a9>SV8lZw_%rV}$T|Gi?Pnauy7={$Qv&~rF0a;F;y8jOQ%`CjFzcQ{i2>bvhJ$p=~}bq1i|9$tDNB&0Du98X-K>o!$!)u;a}o&K)+e&A|yLNTDDxw%wBbZ>g?XX#6Z!yE60*F2ns(OjK{={Y_NHAv$HI!$C$CoLr8dOKApRzR}~z|)lkSQ0zkiG7<wEj`26{UOI0?JV5M_4dKxlt{cuG^;xE>0iqsZ9VObYfD}$T<CYs6bYNkLqhUvf**hU{sWZRKoR`-B3fE|+qkQ9#G}?bWX$2!u$yL6_H29J@17|G`qTE@UYe}xzisC?*p!s|vOTkjDC15Rn(y22oNwZBL2$;H;k@hm$r{^)o*=8YwF=0;Ux?LYs1BV!<}x1Qofh~!&@4dz){i3y%t_YQwaHT35uC|GF6=m8^|k5$NA)au3f-|*?ynt=X&5QBt?J}G&DKHQPcIq93?-Rea}iE^SdFPj+UBD%vcF<B1&^;F(-k$A#HP^eYbz{b`=ZKI$SEeQ>Q%j<b?PPbvN3eCe_}WBwar!4wHF=A<-7#<U$K4q7+^_65`+=E2`4=PQESo<2{A#!C~ojTXnHh?UBqheTqA@F1Z-Y-z@-`R0m)3yUiEytXYmsyUc^50A8pA}0PR+zAKH)g^5*7d`}AoTtr^~IXR3ti@sQ~I1h{OsSsax#r$1gVk2sjumFxN=WZ<JM>i^~@JU!9Mqw;3Ec&!xO!VeADw1)>Y>m_X?b*F%?M_>-k-v2gHbaZ22{_=tTrt)9X(4~^bfV`u(Z`Dh4q&Gei9B8{|Ws!4wrB{0=%?5*SGOX84>UpzfTz_kL=aPnjwQoykIA?xh;Ou!vPv1#(19dw!*-6V(=kL&_&p$TQc38P42*Sxt4Q+$fMEw)kLES5_rY8%G&H;X`<q7O<DmfUmG51BlbwvS=Yuyit>(o8T(?ra?aYdRK-y%tJzOSt6(x)<g*uQcN9JqXa!Z!8|GnE?C+!jRnf>jjQegOQdX_7(`o)N=!ioiwdL=(q`aeo4A@0-Ak23I%N5uIYMuoCRb?EdB&M=*Gfwz3XDBXyV!;E<%k|B}{=f!2elUs`nZ!Kb0}QW2T)oOsfato=2)2|N(|Jl&=57J>(C?i9-d>KhMuz{Xd-JRsu%te4ohO!hV8P6n9eMLVzcbvw6hW4kdMovz#M=*rXm4o#@<tG<CZ{^Yc4xNR?J)rjNqK6l4Z>0NR!+P-@1wHfRB6#T<EC>pk+z5|$5<xb$mLshu0UO4#}{VpGnD>qbsM_M~l8>OcvlB;dt&OR2VEF#sY!&lk&@u%@n!NI6bq`X)S7Q}jr^gKa-v!@F5{p6a&JeuQ-)hH5}OCUEda4*}MfiJL^)OlF1{$XSF2eo6FW@<`j3^+FBq`?Z$9_Kq}OBTjnDmt|B<8Y65m&OIw<1gFku-T(lD@nS$ub)?3G*mTSP7LX1Paq*qEv6?R)_hDqdayW#RoI+Yv*A*~s%L*BoSlF<9&pzBbNcs9l;;uIaNDN_Xqys4);@){fWj5@4LU|a_0kns3pn*06ay6B!v4Bh*#>lfH1GDc4AiQK0%h4kzzGdDvi`NADX<#EEDQBLT`EcvWFblVdqwK%k17FQJwm^(SPWIqFwUIMX&bVt?#u3+^BR9YcP`_Urb~Maxf^bkVF5NC$V32Ew5fMaGn*+?6vyKz&2E6Gt(~ZL@1^%W$l$!W<3T<hy+=$o+4N<Nl0B*`)Mzg#B0bfpY2Tqk)KwDo?M*h*w37#^tJc`2Dk7)&2<xF6#Q}|aMb|G7tM`z~y0xqCnbEafx*Km_M}|@dCmDbyoWI$t4gj@s)&RTJl0?L*=jdwY?wV!}FrW_d{&>WDdZz3*%qA99ZLZ?iMT#?1Ont}zg*W&cIoH4jUajj~#P%ullRd-rd5)lb_H)x;UOP+Ia0(_@3oOS}dRN}AH%jQq9}82}ESZ5d35-IzevCW`53{BI9O5AN^dAj(1>p'
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
