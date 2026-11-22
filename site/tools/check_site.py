#!/usr/bin/env python3
"""피지컬AI 실험실 정적 검사.

common/lab.js 의 PROBLEMS / TOOLS 를 읽어 폴더·링크·번호 규칙을 확인한다.
위반마다 한 줄 출력하고 종료 코드 1, 모두 통과하면 'OK <n> pages'.

  python3 tools/check_site.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"lib", "model", "tools"}
OLD = {"p00-basics": "basics", "p01-torque": "torque", "p02-vibration": "vibration", "p03-sag": "sag",
       "p04-slip": "slip", "p05-tipping": "tipping", "p06-sim2real": "sim2real", "p07-diverge": "diverge",
       "p08-contact": "contact", "p09-lag": "lag", "p10-payload": "payload"}


def entries(js, name):
    """lab.js 의 `const NAME = [ ... ];` 안 { id: "...", ..., ready: true } 들."""
    m = re.search(r"const %s = \[(.*?)\n  \];" % name, js, re.S)
    if not m:
        return None
    out = []
    for obj in re.findall(r"\{[^{}]*\}", m.group(1)):
        idm = re.search(r'\bid:\s*"([^"]+)"', obj)
        if idm:
            out.append((idm.group(1), bool(re.search(r"\bready:\s*true", obj))))
    return out


def main():
    errs = []
    js = (ROOT / "common/lab.js").read_text(encoding="utf-8")
    probs, tools = entries(js, "PROBLEMS"), entries(js, "TOOLS")
    if probs is None or tools is None:
        print("lab.js: PROBLEMS 또는 TOOLS 를 찾지 못함")
        return 1
    items = probs + tools
    if not any(r for _, r in items):
        errs.append("lab.js: ready:true 인 항목이 하나도 없음 (새 형식 아님)")
    ready = [i for i, r in items if r]
    # (a)(b) 폴더
    for i, r in items:
        d = ROOT / i
        if r and not (d / "index.html").is_file():
            errs.append(f"(a) {i}/index.html 없음")
        if not r and d.exists():
            errs.append(f"(b) 준비 중인데 폴더가 있음: {i}/")
    # 검사할 파일: 옛 주소 이동 폴더와 SKIP_DIRS 제외
    files = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if p.suffix not in (".html", ".js") or rel.parts[0] in SKIP_DIRS or rel.parts[0] in OLD:
            continue
        files.append(p)
    for p in files:
        t = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        for m in re.finditer(r"상황 ?\d", t):
            line = t.count("\n", 0, m.start()) + 1
            errs.append(f"(c) {rel}:{line} 번호를 직접 씀: {m.group(0)}")
        for m in re.finditer(r"""(?:href|src)=["'][^"']*\b(p\d\d-[a-z0-9]+)""", t):
            errs.append(f"(d) {rel}: 옛 폴더 링크 {m.group(1)}")
        if "OMX 동역학 실험실" in t:
            errs.append(f"(f) {rel}: 옛 사이트 이름")
    # (e) 각 ready 페이지
    for i in ready:
        f = ROOT / i / "index.html"
        if not f.is_file():
            continue
        t = f.read_text(encoding="utf-8")
        if '<script src="../common/lab.js">' not in t:
            errs.append(f"(e) {i}/index.html: ../common/lab.js 없음")
        if len(re.findall(r"<h1[ >]", t)) != 1:
            errs.append(f"(e) {i}/index.html: <h1> 이 하나가 아님")
    # (h) 사이드바가 생기기 전 화면을 그리지 않게: head 에 render-blocking expect, 본문 끝(스크립트 뒤)에 표시
    for f in [ROOT / i / "index.html" for i in ready] + [ROOT / "index.html"]:
        if not f.is_file():
            continue
        t = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT)
        head = t.split("</head>")[0]
        if '<link rel="expect" href="#shell-done" blocking="render">' not in head:
            errs.append(f"(h) {rel}: head 에 render-blocking expect 없음")
        m = t.rfind('<span id="shell-done" hidden></span>')
        if m < 0 or m < t.rfind("<script"):
            errs.append(f"(h) {rel}: 마지막 스크립트 뒤에 #shell-done 표시 없음")
    # (g) 옛 주소 폴더는 지웠음 (2026-11-21) — 다시 생기지 않게
    for old in OLD:
        if (ROOT / old).exists():
            errs.append(f"(g) 옛 주소 폴더가 남아 있음: {old}/")
    for e in errs:
        print(e)
    if errs:
        return 1
    print(f"OK {len(ready)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
