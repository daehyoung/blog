#!/usr/bin/env python3
"""마크다운 함정 검사 — ①닫히지 않는 볼드·이탤릭 ②이스케이프 안 된 물결표.

한국어 글에서 반복해서 밟은 두 함정이다. 둘 다 빌드가 잡아주지 않는다.

    python3 scripts/check-emphasis.py                 # content/posts 전체
    python3 scripts/check-emphasis.py <파일…>

왜 필요한가 — CommonMark의 right-flanking 규칙 때문이다. 닫는 구분자(`**`/`*`)는

    ① 앞이 공백이 아니어야 하고,
    ② 앞이 구두점이면 뒤가 공백이나 구두점이어야 한다.

그래서 `**명세(유스케이스)**를` 은 닫는 `**` 앞이 `)`(구두점)이고 뒤가 `를`(글자)이라
**닫히지 않고 별표가 그대로 노출된다.** 한국어는 괄호·인용부호 바로 뒤에 조사가 붙는 일이
잦아서 이 패턴이 계속 생긴다. 영어에선 뒤에 공백이 와서 거의 안 걸린다.

⚠️ **빌드는 이걸 못 잡는다.** 마크다운으로선 문법 오류가 아니라 그냥 리터럴 텍스트다.
실제로 이 검사기를 만들기 전까지 34개 파일 80여 곳이 별표를 노출한 채 배포돼 있었다.

고치는 방법(우선순위):
    ① 감싼 기호를 강조 밖으로 — `**"A"**이다` → `"**A**"이다`
    ② 뒤따르는 괄호를 밖으로 — `**전문가(expert)**로` → `**전문가**(expert)로`
    ③ 위 둘로 뜻이 바뀌면 `<strong>`/`<em>` 태그로 — 강조 범위가 정확히 보존된다
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORD = re.compile(r"[가-힣A-Za-z0-9]")


def is_punct(ch: str) -> bool:
    return bool(ch) and unicodedata.category(ch).startswith(("P", "S"))


def scan(path: Path):
    """(줄번호, 구분자, 강조 안쪽, 문맥) 목록을 돌려준다."""
    hits = []
    fence = False
    for no, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        for mark in ("**", "*"):
            # ** 를 볼 때는 그대로, * 를 볼 때는 ** 를 가려 놓고 본다
            probe = line if mark == "**" else line.replace("**", "\x00")
            parts = probe.split(mark)
            if len(parts) < 3 or len(parts) % 2 == 0:
                continue  # 짝이 안 맞는 줄은 판정하지 않는다
            for k in range(1, len(parts) - 1, 2):
                inner, after = parts[k], parts[k + 1]
                if not inner or inner.count("`") % 2:
                    continue
                if not is_punct(inner[-1]):
                    continue
                if not (after and WORD.match(after[0])):
                    continue
                shown = inner.replace("\x00", "**")
                hits.append((no, mark, shown, f"{mark}{shown}{mark}{after[:6]}"))
    return hits


def scan_tilde(path: Path):
    r"""이스케이프 안 된 물결표. GFM은 **물결표 하나로도** 취소선을 만든다.
    `2~3주 → 1~2일` 이 `2<del>3주 → 1</del>2일` 로 깨진 적이 있다.
    범위·근사 표기로 쓸 때는 `\~` 로 적어야 한다."""
    hits = []
    fence = False
    for no, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence or "~" not in line:
            continue
        tick = 0
        prev = ""
        for i, c in enumerate(line):
            if c == "`":
                tick += 1
            if c == "~" and tick % 2 == 0 and prev != "\\":
                hits.append((no, line[max(0, i - 20):i + 12]))
            prev = c
    return hits


def main() -> int:
    args = sys.argv[1:]
    files = [Path(a) for a in args] if args else sorted((ROOT / "content" / "posts").rglob("*.md"))
    files = [f for f in files if not f.name.startswith("_")]

    total = 0
    for f in files:
        tl = scan_tilde(f)
        if tl:
            total += len(tl)
            print(f"\n✗ {f} — 이스케이프 안 된 물결표 (GFM 취소선으로 깨질 수 있다)")
            for no, ctx in tl:
                print(f"    {no}: …{ctx}…   → `\\~` 로 적을 것")
        hits = scan(f)
        if not hits:
            continue
        total += len(hits)
        print(f"\n✗ {f.relative_to(ROOT) if f.is_absolute() else f}")
        for no, mark, _, ctx in hits:
            print(f"    {no}: …{ctx}…   ({mark} 가 닫히지 않는다)")

    if total:
        print(f"\n✗ 마크다운 함정 {total}곳.")
        print("  (모델 출력 원문을 그대로 인용한 자리라면 고치지 말고 그대로 둘 것 — 기록이다.)")
        return 1
    print(f"✓ {len(files)}개 파일 — 닫히지 않는 강조·이스케이프 안 된 물결표 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
