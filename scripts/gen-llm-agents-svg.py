#!/usr/bin/env python3
"""「LLM의 발전 과정과 에이전트」 4장(MoE)용 도해 2장을 생성한다.

  python3 scripts/gen-llm-agents-svg.py   → public/llm-agents/{model-layers,moe-block}.svg

왜 스크립트인가: 완전연결 신경망 그림은 원이 수십 개에 선이 수백 개라
좌표를 손으로 못 고친다. mermaid로도 못 그린다(노드-엣지 다이어그램이라
'층이 쌓인 망' 모양이 안 나온다). scripts/gen-distillation-svg.py 와 같은 이유다.

왜 이 그림이 필요한가: 기존 MoE 도해(라우터 + 전문가 풀)만 보면 **모델에 층이
하나뿐인 것처럼** 읽힌다. 실제로는 블록마다 라우터가 따로 있고 층마다 새로
고른다. 그 오해를 먼저 끊는 그림이다.

다크모드: 색은 전부 클래스로 주고 @media (prefers-color-scheme: dark)에서 뒤집는다.
그래서 이 SVG는 반드시 public/ 에 두고 <img>로 불러야 한다(CLAUDE.md §4).
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "llm-agents"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "system-ui,-apple-system,'Apple SD Gothic Neo','Noto Sans KR',sans-serif"

STYLE = f"""
    text   {{ font-family: {FONT}; }}
    .lbl   {{ fill: #6b7280; font-size: 15px; text-anchor: middle; }}
    .lblb  {{ fill: #6b7280; font-size: 16px; font-weight: 700; text-anchor: middle; }}
    .mut   {{ fill: #8a929e; font-size: 14px; text-anchor: middle; }}
    .accent{{ fill: #3b82f6; font-size: 16px; font-weight: 700; text-anchor: middle; }}
    .warn  {{ fill: #dc5a47; font-size: 15px; font-weight: 700; text-anchor: middle; }}
    .tag   {{ fill: #8a929e; font-size: 13px; }}
    .tagOn {{ fill: #3b82f6; font-size: 13px; font-weight: 700; }}
    .node  {{ fill: #8a99ad; fill-opacity: .10; stroke: #4a90d9; stroke-width: 2; }}
    .nodeQ {{ fill: #8a99ad; fill-opacity: .22; stroke: #4a90d9; stroke-width: 2; }}
    .nodeA {{ fill: #3b82f6; fill-opacity: .28; stroke: #3b82f6; stroke-width: 2; }}
    .nodeOff {{ fill: none; stroke: #98a2b0; stroke-width: 1.5; }}
    .wire  {{ stroke: #8a99ad; stroke-width: 1; opacity: .5; }}
    .wireD {{ stroke: #8a99ad; stroke-width: 1; opacity: .38; stroke-dasharray: 4 4; }}
    .wireOn{{ stroke: #3b82f6; stroke-width: 2.4; }}
    .wireOff{{ stroke: #98a2b0; stroke-width: 1; opacity: .55; stroke-dasharray: 4 4; }}
    .panel {{ fill: #8a99ad; fill-opacity: .09; stroke: #8a99ad; stroke-opacity: .5; stroke-width: 2; }}
    .panel2{{ fill: #8a99ad; fill-opacity: .05; stroke: #98a2b0; stroke-opacity: .7; stroke-width: 2; }}
    .panel3{{ fill: #3b82f6; fill-opacity: .05; stroke: #4a90d9; stroke-width: 2; }}
    .router{{ fill: #dc5a47; fill-opacity: .12; stroke: #dc5a47; stroke-width: 2; }}
    .flow  {{ stroke: #dc5a47; stroke-width: 2; opacity: .85; fill: none; }}
"""

# ⚠️ 다크모드를 매체 쿼리로 처리하지 않는 이유
#
# 이 블로그의 테마는 OS 설정이 아니라 <html data-theme>를 손으로 토글한다
# (Layout.astro, localStorage). 그런데 <img>로 불린 SVG는 별개 문서라
# 그 data-theme를 볼 수 없고 prefers-color-scheme(=OS)만 안다.
# 그래서 "OS는 다크인데 사이트는 라이트"에서 도해만 까맣게 뒤집힌다.
# 선 그림은 티가 덜 나지만 이 도해들처럼 **면이 큰 그림은 그대로 검은 박스**가 된다.
#
# 결론: 매체 쿼리를 쓰지 말고, 어느 배경에서나 읽히는 중립 팔레트로 그린다.
#   - 면은 전부 반투명(fill-opacity) — 배경색이 비쳐 보이므로 양쪽에서 어울린다
#   - 글자·선은 중간 톤(#6b7280 / #8a99ad)과 강조색(#3b82f6 / #dc5a47)만 쓴다
#     (흰 바탕·어두운 바탕 모두 대비 3:1 이상)


def head(w, h, extra=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="LLM 층 구조 도해"><style>{STYLE}</style>{extra}'
    )


def col(cx, n, cy, gap, r=11, cls="node"):
    top = cy - (n - 1) * gap / 2
    pts = [(cx, top + i * gap) for i in range(n)]
    body = "".join(f'<circle cx="{x}" cy="{y:.1f}" r="{r}" class="{cls}"/>' for x, y in pts)
    return pts, body


def mesh(a, b, cls="wire"):
    return "".join(
        f'<line x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}" class="{cls}"/>'
        for x1, y1 in a for x2, y2 in b
    )


# ── ① 모델은 '층이 쌓인' 구조 ────────────────────────────────────────
def model_layers():
    W, H, cy = 1160, 500, 250
    s = [head(W, H,
              '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
              'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#dc5a47"/>'
              '</marker></defs>')]
    xs = [90, 250, 400, 550, 700, 850, 1010]
    counts = [4, 9, 9, 0, 9, 9, 5]
    gaps = [40, 30, 30, 0, 30, 30, 36]
    cols = [col(x, n, cy, g)[0] if n else [] for x, n, g in zip(xs, counts, gaps)]
    mid = [(550, cy - 60), (550, cy), (550, cy + 60)]

    s.append(f'<rect x="200" y="60" width="700" height="380" rx="14" class="panel"/>')
    s.append(mesh(cols[0], cols[1]))
    s.append(mesh(cols[1], cols[2]))
    s.append(mesh(cols[2], mid, "wireD"))
    s.append(mesh(mid, cols[4], "wireD"))
    s.append(mesh(cols[4], cols[5]))
    s.append(mesh(cols[5], cols[6]))
    for x, n, g in zip(xs, counts, gaps):
        if n:
            s.append(col(x, n, cy, g)[1])
    s.append(f'<text x="550" y="{cy + 10}" class="mut" font-size="30">⋯</text>')

    for x, nm in zip(xs, ["입력 토큰", "블록 1", "블록 2", "", "블록 N-1", "블록 N", "출력"]):
        if nm:
            s.append(f'<text x="{x}" y="455" class="lbl">{nm}</text>')
    s.append('<text x="90" y="478" class="mut">임베딩</text>')
    s.append('<text x="1010" y="478" class="mut">다음 토큰 확률</text>')
    s.append('<text x="550" y="42" class="accent">트랜스포머 블록 × N층 — 대형 모델이면 수십~백여 층</text>')
    s.append('<text x="550" y="88" class="mut">각 블록 = 어텐션 + FFN · 파라미터의 대부분은 FFN에 있다</text>')
    s.append(
        f'<path d="M 90 {cy + 172} L 1010 {cy + 172}" class="flow" marker-end="url(#ar)"/>'
        f'<text x="550" y="{cy + 158}" class="warn">'
        f'토큰 하나가 답이 되려면 이 전체를 처음부터 끝까지 한 번 통과한다</text>'
    )
    s.append("</svg>")
    return "".join(s)


# ── ② 한 블록 안: Dense FFN vs MoE ──────────────────────────────────
def moe_block():
    W, H = 1160, 470
    s = [head(W, H)]

    def panel(x0, w, cls, title, sub, tcls):
        s.append(f'<rect x="{x0}" y="52" width="{w}" height="372" rx="14" class="{cls}"/>')
        s.append(f'<text x="{x0 + w / 2:.0f}" y="36" class="{tcls}">{title}</text>')
        s.append(f'<text x="{x0 + w / 2:.0f}" y="404" class="mut">{sub}</text>')

    panel(20, 520, "panel2", "Dense 블록", "매 토큰마다 FFN 전체를 읽고 계산한다 → 대역폭이 곧 속도", "lblb")
    a_in, g1 = col(95, 6, 240, 32)
    attn, g2 = col(235, 6, 240, 32, cls="nodeQ")
    ffn, g3 = col(395, 8, 240, 26, cls="nodeA")
    a_out, g4 = col(505, 6, 240, 32)
    s += [mesh(a_in, attn), mesh(attn, ffn), mesh(ffn, a_out), g1, g2, g3, g4]
    s.append('<text x="235" y="140" class="mut">어텐션</text>')
    s.append('<text x="395" y="112" class="lblb" font-size="15">FFN — 하나, 통째로</text>')

    panel(600, 540, "panel3", "MoE 블록", "이 층의 라우터가 top-k만 고른다 · 층마다 새로 고른다", "accent")
    b_in, h1 = col(665, 6, 240, 32)
    attn2, h2 = col(785, 6, 240, 32, cls="nodeQ")
    s += [mesh(b_in, attn2), h1, h2]
    s.append('<text x="785" y="140" class="mut">어텐션 (항상 dense)</text>')

    RX, RY = 890, 240
    s.append(mesh(attn2, [(RX, RY)]))
    s.append(f'<path d="M {RX - 26} {RY} l 26 -22 l 26 22 l -26 22 z" class="router"/>')
    s.append(f'<text x="{RX}" y="{RY - 34}" class="warn" font-size="13">라우터</text>')

    EX = 985
    for i, ty in enumerate([110, 190, 270, 350]):
        on = i in (1, 2)
        _, g = col(EX, 3, ty, 22, r=9, cls="nodeA" if on else "nodeOff")
        s.append(f'<line x1="{RX + 26}" y1="{RY}" x2="{EX - 12}" y2="{ty}" '
                 f'class="{"wireOn" if on else "wireOff"}"/>')
        s.append(g)
        s.append(f'<text x="{EX + 30}" y="{ty + 5}" class="{"tagOn" if on else "tag"}">'
                 f'전문가 {i + 1}{" ✓" if on else ""}</text>')
    s.append(f'<text x="{EX + 10}" y="74" class="accent" font-size="15">FFN 자리 = 전문가 여럿</text>')
    s.append('<text x="580" y="452" class="warn" font-size="16">'
             'MoE가 바꾸는 것은 모델 전체가 아니라 "블록마다의 FFN 자리"다</text>')
    s.append("</svg>")
    return "".join(s)


for name, svg in [("model-layers.svg", model_layers()), ("moe-block.svg", moe_block())]:
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"  public/llm-agents/{name}  ({len(svg):,} bytes)")
