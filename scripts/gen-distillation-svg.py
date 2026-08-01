#!/usr/bin/env python3
"""증류 시리즈 도해 3장을 생성한다.

    python3 scripts/gen-distillation-svg.py

출력: public/distillation-limits/{tail,distillation,scanner}.svg

왜 스크립트인가 — 종모양 곡선이 계산된 점 220개라 손으로 못 고친다.
색·라벨만 바꿀 거면 SVG를 직접 편집해도 되지만, 곡선 모양(±σ 범위,
꼬리 경계 CUT, student 분포 폭 등)을 바꾸려면 여기서 바꾸고 다시 돌린다.

다크모드: ⚠️ prefers-color-scheme 를 쓰지 않는다. 이 사이트의 테마는 OS 설정이
아니라 <html data-theme> 수동 토글(localStorage, Layout.astro)인데, <img>로 불린
SVG는 별개 문서라 그 data-theme 을 볼 수 없고 OS 설정만 안다. 그래서 "OS는
다크인데 사이트는 라이트"에서 도해만 뒤집혀 흰 바탕에 흐린 글씨가 됐다(실제로 겪었다).

대신 어느 배경에서나 읽히는 중립 팔레트로 그린다 — 면은 전부 반투명
(fill-opacity)이라 배경색이 비쳐 보이고, 글자·선은 양쪽 대비 3:1 이상인
중간 톤(#6b7280·#8a99ad)과 강조색(#3b82f6·#dc5a47)만 쓴다.
public/ 에 두고 <img>로 쓰는 것은 그대로다(벡터라 최적화가 의미 없다).
"""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "distillation-limits"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = """
    .curve  { fill: none; stroke: #4a90d9; stroke-width: 2.2; }
    .curve2 { fill: none; stroke: #17a8bd; stroke-width: 2.2; }
    .fillA  { fill: #4a90d9; fill-opacity: .22; }
    .fillB  { fill: #17a8bd; fill-opacity: .20; }
    .tailA  { fill: #dc5a47; fill-opacity: .32; }
    .ghost  { fill: #8a99ad; fill-opacity: .22; }
    .box    { fill: none; stroke: #8a99ad; stroke-opacity: .75; stroke-width: 1.6; rx: 10; }
    .axis   { stroke: #8a99ad; stroke-width: 1.4; }
    .gridln { stroke: #8a99ad; stroke-width: 1; stroke-dasharray: 4 4; }
    .dash   { stroke: #8a99ad; stroke-width: 1.4; stroke-dasharray: 5 5; fill: none; }
    .arrow  { stroke: #4a90d9; stroke-width: 2.4; fill: none; }
    .lbl    { fill: #6b7280; font-family: system-ui,-apple-system,'Apple SD Gothic Neo',sans-serif; }
    .mut    { fill: #8a929e; font-family: system-ui,-apple-system,'Apple SD Gothic Neo',sans-serif; }
    .warn   { fill: #dc5a47; font-weight: 700; }
    .accent { fill: #3b82f6; font-weight: 700; }"""


def bell(cx, base, peak, half, smax=3.4, width=1.0, a=None, b=None, close=True):
    """중심 cx·밑변 base·봉우리 peak·반폭 half 인 종모양 path.
    width < 1 이면 분포가 좁아진다(= 꼬리가 얇아진다). a,b 로 구간만 그린다."""
    a = -smax if a is None else a
    b = smax if b is None else b
    n = 200
    pts = []
    for i in range(n + 1):
        s = a + (b - a) * i / n
        pts.append((cx + s / smax * half, base - math.exp(-(s / width) ** 2 / 2) * (base - peak)))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    if close:
        d += f" L {cx + b/smax*half:.1f},{base} L {cx + a/smax*half:.1f},{base} Z"
    return d


def write(name, w, h, aria, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"\n'
           f'     aria-label="{aria}">\n  <style>{STYLE}\n  </style>\n{body}</svg>\n')
    (OUT / name).write_text(svg)
    print(f"  {name}  ({len(svg)} bytes)")


# ── ① tail.svg — 정규분포의 중앙과 꼬리 ─────────────────────────────
W, H, X0, X1, BASE, PEAK, SMAX, CUT = 760, 350, 70, 690, 265, 65, 3.6, 1.8
px = lambda s: X0 + (s + SMAX) / (2 * SMAX) * (X1 - X0)
py = lambda s: BASE - math.exp(-s * s / 2) * (BASE - PEAK)
g = lambda a, b, close=True: bell((X0 + X1) / 2, BASE, PEAK, (X1 - X0) / 2, SMAX, 1.0, a, b, close)

write("tail.svg", W, H, "정규분포 곡선에서 중앙과 양쪽 꼬리를 표시한 그림", f'''
  <path class="tailA"  d="{g(-SMAX,-CUT)}"/>
  <path class="fillA"  d="{g(-CUT,CUT)}"/>
  <path class="tailA"  d="{g(CUT,SMAX)}"/>
  <path class="curve"  d="{g(-SMAX,SMAX,False)}"/>
  <line class="gridln" x1="{px(-CUT):.1f}" y1="{py(-CUT):.1f}" x2="{px(-CUT):.1f}" y2="{BASE}"/>
  <line class="gridln" x1="{px(CUT):.1f}"  y1="{py(CUT):.1f}"  x2="{px(CUT):.1f}"  y2="{BASE}"/>
  <line class="axis" x1="{X0-10}" y1="{BASE}" x2="{X1+10}" y2="{BASE}"/>
  <text class="lbl accent" x="{px(0):.1f}" y="175" font-size="19" text-anchor="middle">중앙</text>
  <text class="mut" x="{px(0):.1f}" y="199" font-size="14" text-anchor="middle">자주 들어오는 입력</text>
  <text class="mut" x="{px(0):.1f}" y="219" font-size="14" text-anchor="middle">— 여기는 잘 배운다</text>
  <text class="lbl warn" x="{px(-2.65):.1f}" y="{BASE-52}" font-size="19" text-anchor="middle">꼬리</text>
  <text class="lbl warn" x="{px(2.65):.1f}"  y="{BASE-52}" font-size="19" text-anchor="middle">꼬리</text>
  <text class="mut" x="{px(-2.65):.1f}" y="{BASE-32}" font-size="13" text-anchor="middle">드문 입력</text>
  <text class="mut" x="{px(2.65):.1f}"  y="{BASE-32}" font-size="13" text-anchor="middle">드문 입력</text>
  <text class="mut" x="{px(-2.65):.1f}" y="{BASE+22}" font-size="13" text-anchor="middle">↑ 얇지만 0이 아니다</text>
  <text class="mut" x="{px(2.65):.1f}"  y="{BASE+22}" font-size="13" text-anchor="middle">↑ 얇지만 0이 아니다</text>
  <text class="lbl" x="{W/2}" y="{H-38}" font-size="14" text-anchor="middle">가로축 = 있을 수 있는 입력들 · 높이 = 그 입력이 들어올 확률</text>
  <text class="mut" x="{W/2}" y="{H-14}" font-size="13" text-anchor="middle">넓이가 곧 학습이 신경 쓰는 양 — 꼬리는 넓이가 작아서 무시된다</text>
''')

# ── ② distillation.svg — teacher → student ─────────────────────────
W, H, TB = 820, 380, 250
write("distillation.svg", W, H,
      "큰 teacher 모델이 작은 student 모델에게 정답 신호를 넘겨주는 증류 구조도", f'''
  <rect class="box" x="30" y="55" width="290" height="230"/>
  <rect class="box" x="500" y="95" width="290" height="190"/>
  <text class="lbl accent" x="175" y="82" font-size="17" text-anchor="middle">teacher · 큰 모델 (선생님)</text>
  <text class="lbl accent" x="645" y="122" font-size="17" text-anchor="middle">student · 작은 모델 (학생)</text>
  <path class="fillA" d="{bell(175,TB,120,120)}"/>
  <path class="curve" d="{bell(175,TB,120,120,close=False)}"/>
  <line class="axis" x1="50" y1="{TB}" x2="300" y2="{TB}"/>
  <text class="mut" x="175" y="272" font-size="12.5" text-anchor="middle">꼬리까지 두껍다</text>
  <path class="ghost"  d="{bell(645,TB,160,120)}"/>
  <path class="fillB"  d="{bell(645,TB,160,120,width=0.62)}"/>
  <path class="curve2" d="{bell(645,TB,160,120,width=0.62,close=False)}"/>
  <path class="dash"   d="{bell(645,TB,160,120,close=False)}"/>
  <line class="axis" x1="520" y1="{TB}" x2="770" y2="{TB}"/>
  <text class="warn" x="645" y="272" font-size="12.5" text-anchor="middle">꼬리가 얇아진다</text>
  <path class="arrow" d="M 330 175 L 480 175"/>
  <path class="arrow" d="M 470 168 L 482 175 L 470 182"/>
  <text class="lbl" x="405" y="150" font-size="14.5" text-anchor="middle">정답 신호를 넘긴다</text>
  <text class="mut" x="405" y="200" font-size="12.5" text-anchor="middle">soft label(확률 분포)</text>
  <text class="mut" x="405" y="218" font-size="12.5" text-anchor="middle">또는 생성 텍스트</text>
  <text class="lbl" x="{W/2}" y="330" font-size="14.5" text-anchor="middle">증류 = 정답을 사람이 아니라 <tspan class="accent">더 잘하는 모델</tspan>에게서 가져오는 것</text>
  <text class="mut" x="{W/2}" y="355" font-size="13" text-anchor="middle">중앙은 선생님에 근접하지만, 회색으로 남은 꼬리만큼이 구조적으로 손실된다</text>
''')

# ── ③ paintball-{before,after}.svg — 격자로 훑어 형상을 드러낸다 ────
# ⚠️ 중요: 자국을 '윤곽 위'에 찍으면 안 된다 — 그건 이미 모양을 아는 셈이다.
# 쏘는 쪽은 모양을 모르니 **일정 간격 격자로 난사**하고, 맞은 점의 집합이
# 형상으로 드러난다. 그래서 두 장으로 나눴다:
#   before — 격자만 있다(무엇이 어디 있는지 모른다)
#   after  — 맞은 점이 모여 삼각형·사각형·원이 드러난다. 쏜 발수는 세지만
#            격자를 어디까지 넓혀야 하는지는 모른다(= 분모 문제)
PW, PH = 340, 286                 # 패널 하나 크기
STEP = 20                         # 격자 간격
GX0, GY0 = 26, 30                 # 패널 안 격자 시작 오프셋
NX, NY = 15, 12                   # 격자 점 개수


def grid_pts():
    return [(GX0 + i * STEP, GY0 + j * STEP) for j in range(NY) for i in range(NX)]


def in_tri(x, y):
    cx, cy, side = GX0 + 7 * STEP, GY0 + 6 * STEP, 200
    h = side * math.sqrt(3) / 2
    a, b, c = (cx, cy - h * 2 / 3), (cx + side / 2, cy + h / 3), (cx - side / 2, cy + h / 3)
    def sign(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    s1, s2, s3 = sign(a, b, (x, y)), sign(b, c, (x, y)), sign(c, a, (x, y))
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


def in_sq(x, y):
    cx, cy, s = GX0 + 7 * STEP, GY0 + 5.5 * STEP, 168
    return abs(x - cx) <= s / 2 and abs(y - cy) <= s / 2


def in_circ(x, y):
    """일부러 격자 오른쪽 밖으로 삐져나가게 둔다 — '격자 밖은 아예 안 쐈다'를 보이려고."""
    cx, cy, r = GX0 + 11 * STEP, GY0 + 5.5 * STEP, 108
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def panel(ox, name, hit, note, extra=""):
    pts = grid_pts()
    hits = [(x, y) for x, y in pts if hit(x, y)]
    dots = "".join(
        f'<circle cx="{ox + x}" cy="{y}" r="2.2" fill="#8a99ad" fill-opacity=".38"/>'
        for x, y in pts if not hit(x, y))
    marks = "".join(
        f'<circle cx="{ox + x}" cy="{y}" r="6.4" fill="#4a90d9" fill-opacity=".85"/>'
        for x, y in hits)
    return len(hits), len(pts), f'''
  <rect x="{ox}" y="14" width="{PW}" height="{PH}" rx="12" fill="#8a99ad" fill-opacity=".05"
        stroke="#8a99ad" stroke-opacity=".4" stroke-width="1.6"/>
  {dots}{marks}{extra}
  <text class="accent" x="{ox + PW/2:.0f}" y="{PH + 44}" font-size="17" text-anchor="middle">{name}</text>
  <text class="lbl" x="{ox + PW/2:.0f}" y="{PH + 68}" font-size="14" text-anchor="middle">맞은 자국 {len(hits)}발 / 쏜 {len(pts)}발</text>
  <text class="mut" x="{ox + PW/2:.0f}" y="{PH + 88}" font-size="12.5" text-anchor="middle">{note}</text>'''

# before — 격자만
gp = grid_pts()
dots_only = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#8a99ad" fill-opacity=".55"/>'
                    for x, y in gp)
write("paintball-before.svg", 980, 420,
      "아주 멀리 있어 모양이 보이지 않는 표적. 겨눌 곳이 없으므로 일정 간격 격자로 쏠 자리만 정해 둔 그림", f'''
  <rect class="box" x="30" y="176" width="104" height="66"/>
  <rect x="134" y="200" width="16" height="16" fill="#4a90d9"/>
  <text class="lbl accent" x="82" y="166" font-size="14" text-anchor="middle">질문 한 발 = 페인트볼 한 발</text>
  <text class="mut" x="82" y="262" font-size="12.5" text-anchor="middle">모양이 안 보이니 겨눌 곳이 없다</text>

  <line x1="156" y1="208" x2="600" y2="208" class="dash"/>
  <text class="lbl" x="378" y="196" font-size="14.5" font-weight="700" text-anchor="middle">표적이 아주 멀다</text>
  <text class="mut" x="378" y="228" font-size="12.5" text-anchor="middle">무슨 모양인지, 얼마나 큰지 보이지 않는다</text>

  <g transform="translate(608,80)">{dots_only}</g>
  <rect x="626" y="100" width="{NX*STEP+8}" height="{NY*STEP+8}" rx="10" fill="none"
        stroke="#8a99ad" stroke-opacity=".45" stroke-width="1.6" stroke-dasharray="7 7"/>
  <text class="lbl" x="{626+(NX*STEP+8)/2:.0f}" y="88" font-size="14.5" font-weight="700"
        text-anchor="middle">그래서 일정 간격으로 훑는다</text>
  <text class="accent" x="{626+(NX*STEP+8)/2:.0f}" y="{100+NY*STEP+30:.0f}" font-size="14"
        text-anchor="middle">격자 {NX}×{NY} = {len(gp)}발</text>
  <text class="mut" x="{626+(NX*STEP+8)/2:.0f}" y="{100+NY*STEP+50:.0f}" font-size="12.5"
        text-anchor="middle">각 점이 "여기 쏴 본다"는 뜻</text>

  <text class="warn" x="490" y="404" font-size="16" text-anchor="middle">쏘기 전 — 무엇인지도, 얼마나 큰지도, 격자를 어디까지 넓혀야 하는지도 모른다</text>
''')

# after — 맞은 점의 집합이 형상
h1, n1, p1 = panel(20, "삼각형", in_tri, "격자 간격이 굵으면 경계가 계단처럼 뭉개진다")
h2, n2, p2 = panel(400, "사각형", in_sq, "같은 격자, 같은 발수인데 자국 수가 다르다")
# '격자 밖'을 눈에 보이게 — 원이 여기로 삐져나갔지만 한 발도 안 쐈다
_cx = 780 + GX0 + (NX - 1) * STEP + 12
clip_note = (f'<rect x="{_cx}" y="14" width="{1120 - _cx}" height="{PH}" fill="#dc5a47" fill-opacity=".13"/>'
             f'<text class="warn" x="{_cx + (1120 - _cx) / 2:.0f}" y="{PH - 6}" font-size="11" '
             f'text-anchor="middle" transform="rotate(-90 {_cx + (1120 - _cx) / 2:.0f} {PH - 6})">'
             f'격자 밖 · 안 쐈다</text>')
h3, n3, p3 = panel(780, "원", in_circ,
                   "오른쪽이 격자 밖으로 나갔다 — 거기는 아예 안 쐈다", clip_note)

write("paintball-after.svg", 1160, 486,
      "쏜 뒤. 격자에서 맞은 점들의 집합이 삼각형·사각형·원의 형상으로 드러난 그림", f'''
{p1}{p2}{p3}
  <text class="lbl" x="580" y="{PH + 112}" font-size="15" text-anchor="middle"><tspan class="accent">회수해서 봐도</tspan> 손에 남는 건 격자 위 맞음/안 맞음 기록뿐 — 격자 사이는 여전히 유추다</text>
  <text class="warn" x="580" y="{PH + 140}" font-size="16.5" text-anchor="middle">사격장 표적지엔 테두리가 있어 전체 면적을 안다. 지식 분포에는 그 테두리가 없다</text>
  <text class="mut" x="580" y="{PH + 164}" font-size="13" text-anchor="middle">분자(쏜 발수)는 세지는데 분모가 없다 — 그래서 "몇 %"가 아예 계산되지 않는다</text>
''')

# ── ④ convergence.svg — 겉보기 수렴 vs 실제 지형 ────────────────────
# 본문은 이것을 '로컬 미니멈'이 아니라 '평지(plateau)'로 설명한다.
# 로컬 미니멈 = 빠져나오기 어려운 웅덩이 / 평지 = 애초에 미는 힘이 없는 곳.
# 원인이 '확률 가중이 작아 gradient가 안 실림'이므로 평지가 맞다.
W, H = 880, 430
AX, AY, AW, AH = 70, 90, 320, 175          # 왼쪽 패널(계기판)
BX, BY, BW, BH = 500, 90, 320, 175         # 오른쪽 패널(지형)

def loss_curve():
    n = 120
    pts = []
    for i in range(n + 1):
        t = i / n
        y = 0.08 + 0.92 * math.exp(-t * 6.5)          # 빠르게 떨어져 바닥에 눕는다
        pts.append((AX + t * AW, AY + (1 - y) * AH))
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def landscape(t):
    """왼쪽에 깊은 골짜기, 오른쪽에 높고 평평한 평지."""
    return 0.62 - 0.55 * math.exp(-((t - 0.24) / 0.135) ** 2) + 0.12 / (1 + math.exp(-(t - 0.52) / 0.035))

def land_path():
    n = 200
    # SVG는 y가 아래로 커진다. loss가 낮을수록 화면 아래(골짜기)가 되도록 반전.
    pts = [(BX + i / n * BW, BY + (1 - landscape(i / n)) * BH) for i in range(n + 1)]
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

bx_valley, bx_flat = 0.24, 0.82
vx, vy = BX + bx_valley * BW, BY + (1 - landscape(bx_valley)) * BH
fx, fy = BX + bx_flat * BW, BY + (1 - landscape(bx_flat)) * BH

write("convergence.svg", W, H,
      "왼쪽은 평평해진 loss 곡선, 오른쪽은 골짜기에 안착한 공과 평지에 방치된 공", f'''
  <text class="lbl accent" x="{AX+AW/2:.0f}" y="62" font-size="16" text-anchor="middle">우리가 보는 것 — 계기판</text>
  <text class="lbl accent" x="{BX+BW/2:.0f}" y="62" font-size="16" text-anchor="middle">실제로 일어나는 것 — 지형</text>

  <line class="axis" x1="{AX}" y1="{AY+AH}" x2="{AX+AW+12}" y2="{AY+AH}"/>
  <line class="axis" x1="{AX}" y1="{AY-8}"  x2="{AX}" y2="{AY+AH}"/>
  <text class="mut" x="{AX-8}" y="{AY+4}" font-size="12" text-anchor="end">loss</text>
  <text class="mut" x="{AX+AW+14}" y="{AY+AH+16}" font-size="12" text-anchor="end">학습 진행 →</text>
  <path class="curve" d="{loss_curve()}"/>
  <line class="gridln" x1="{AX+AW*0.55:.0f}" y1="{AY+AH*0.86:.0f}" x2="{AX+AW:.0f}" y2="{AY+AH*0.86:.0f}"/>
  <text class="lbl" x="{AX+AW*0.78:.0f}" y="{AY+AH*0.72:.0f}" font-size="13.5" text-anchor="middle">더 안 줄어든다</text>
  <text class="mut" x="{AX+AW/2:.0f}" y="{AY+AH+42:.0f}" font-size="13" text-anchor="middle">전체 loss가 납작해졌다 → &quot;수렴했다, 학습 끝&quot;</text>
  <text class="warn" x="{AX+AW/2:.0f}" y="{AY+AH+63:.0f}" font-size="13" text-anchor="middle">그런데 이 곡선은 평균이라, 꼬리의 실패를 못 본다</text>

  <path class="curve" d="{land_path()}"/>
  <line class="gridln" x1="{fx-70:.0f}" y1="{fy:.0f}" x2="{fx+60:.0f}" y2="{fy:.0f}"/>
  <circle cx="{vx:.0f}" cy="{vy-9:.0f}" r="9" fill="#2563eb"/>
  <circle cx="{fx:.0f}" cy="{fy-9:.0f}" r="9" fill="#dc2626"/>
  <text class="lbl accent" x="{vx:.0f}" y="{vy-64:.0f}" font-size="13.5" text-anchor="middle">중앙</text>
  <text class="mut"        x="{vx:.0f}" y="{vy-46:.0f}" font-size="12" text-anchor="middle">바닥에 도착</text>
  <text class="mut"        x="{vx:.0f}" y="{vy-29:.0f}" font-size="12" text-anchor="middle">= 정답</text>
  <text class="lbl warn" x="{fx:.0f}" y="{fy-26:.0f}" font-size="13.5" text-anchor="middle">꼬리</text>
  <text class="mut"      x="{fx:.0f}" y="{fy+28:.0f}" font-size="12" text-anchor="middle">평지에 방치</text>
  <text class="mut"      x="{fx:.0f}" y="{fy+45:.0f}" font-size="12" text-anchor="middle">= 틀린 채로 멈춤</text>
  <text class="mut" x="{BX+BW/2:.0f}" y="{BY+BH+42:.0f}" font-size="13" text-anchor="middle">둘 다 기울기 ≈ 0 이라 안 움직인다 — 증상이 같다</text>
  <text class="warn" x="{BX+BW/2:.0f}" y="{BY+BH+63:.0f}" font-size="13" text-anchor="middle">하나는 도착이고 하나는 방치다</text>

  <text class="lbl" x="{W/2}" y="{H-42}" font-size="14.5" text-anchor="middle">꼬리가 멈춘 건 <tspan class="accent">다 배워서</tspan>가 아니라 <tspan class="warn">미는 힘이 없어서</tspan>다</text>
  <text class="mut" x="{W/2}" y="{H-18}" font-size="13" text-anchor="middle">빠져나오기 어려운 웅덩이(로컬 미니멈)가 아니라, 애초에 경사가 없는 평지다 — 그래서 힘을 실어주면 다시 움직인다</text>
''')

# ── ⑤ sampling.svg — 샘플링 간격: 중앙은 촘촘, 꼬리는 뻥 뚫림 ────────
# 03편 §3의 논지. teacher는 유한 번만 샘플링하고, 그 사이는 student가
# 보간(추측)으로 메운다. 꼬리는 저빈도라 샘플이 드물어 보간 거리가 멀다.
# 샘플 위치를 확률의 등간격 분위수로 잡으면 밀도가 자연히 분포를 따른다.

def inv_norm(p_):
    """표준정규 역누적분포. erf 이분법으로 충분히 정확하게."""
    lo, hi = -6.0, 6.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p_:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

W, H = 820, 400
SX0, SX1, SBASE, SPEAK, SM = 80, 740, 255, 70, 3.2
sx = lambda s: SX0 + (s + SM) / (2 * SM) * (SX1 - SX0)
sy = lambda s: SBASE - math.exp(-s * s / 2) * (SBASE - SPEAK)
sg = lambda a, b, close=True: bell((SX0 + SX1) / 2, SBASE, SPEAK, (SX1 - SX0) / 2, SM, 1.0, a, b, close)

N = 23
samples = [inv_norm(k / (N + 1)) for k in range(1, N + 1)]
samples = [s for s in samples if abs(s) <= SM]

ticks = "".join(
    f'<line x1="{sx(s):.1f}" y1="{SBASE:.0f}" x2="{sx(s):.1f}" y2="{sy(s):.1f}" '
    f'stroke="#2563eb" stroke-width="1.6" opacity="0.75"/>'
    f'<circle cx="{sx(s):.1f}" cy="{SBASE:.0f}" r="3.2" fill="#2563eb"/>'
    for s in samples)

# 강조할 두 간격: 중앙 한 쌍, 꼬리 한 쌍
mid = len(samples) // 2
c1, c2 = samples[mid - 1], samples[mid]
TC = samples[-1]           # 샘플이 존재하는 마지막 지점 = 꼬리 음영 경계
t1, t2 = TC, SM            # 마지막 샘플 ~ 분포 끝: 샘플이 하나도 없는 구간
gap_y = SBASE + 34

def gap(a, b, y, label, sub, cls):
    xa, xb = sx(a), sx(b)
    return (f'<line class="axis" x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}"/>'
            f'<line class="axis" x1="{xa:.1f}" y1="{y-5}" x2="{xa:.1f}" y2="{y+5}"/>'
            f'<line class="axis" x1="{xb:.1f}" y1="{y-5}" x2="{xb:.1f}" y2="{y+5}"/>'
            f'<text class="{cls}" x="{(xa+xb)/2:.1f}" y="{y+22}" font-size="13" text-anchor="middle">{label}</text>'
            f'<text class="mut" x="{(xa+xb)/2:.1f}" y="{y+39}" font-size="12" text-anchor="middle">{sub}</text>')

write("sampling.svg", W, H,
      "종모양 분포 아래 샘플 눈금이 중앙에는 촘촘하고 꼬리로 갈수록 성기게 찍힌 그림", f'''
  <path class="tailA" d="{sg(TC, SM)}" opacity="0.5"/>
  <path class="tailA" d="{sg(-SM, -TC)}" opacity="0.5"/>
  <path class="fillA" d="{sg(-TC, TC)}" opacity="0.55"/>
  <path class="curve" d="{sg(-SM, SM, False)}"/>
  {ticks}
  <line class="axis" x1="{SX0-10}" y1="{SBASE}" x2="{SX1+10}" y2="{SBASE}"/>

  <text class="lbl accent" x="{sx(0):.0f}" y="38" font-size="15" text-anchor="middle">│ = teacher에게 실제로 물어본 지점</text>
  <text class="mut" x="{sx(0):.0f}" y="56" font-size="12.5" text-anchor="middle">무한히 물을 수 있지만, 실제로는 유한 번만 묻는다</text>

  {gap(c1, c2, gap_y, "간격 좁다", "사이를 추측해도 거의 안 틀린다", "lbl accent")}
  {gap(t1, t2, gap_y, "여기는 샘플이 0개", "통째로 추측해서 메운다", "lbl warn")}

  <text class="warn" x="{sx(2.65):.0f}" y="{SBASE-52:.0f}" font-size="14" text-anchor="middle">꼬리</text>
  <text class="mut"  x="{sx(2.65):.0f}" y="{SBASE-35:.0f}" font-size="12" text-anchor="middle">샘플이 없다</text>
  <text class="lbl accent" x="{sx(-2.7):.0f}" y="{SBASE-52:.0f}" font-size="14" text-anchor="middle">꼬리</text>
  <text class="mut"        x="{sx(-2.7):.0f}" y="{SBASE-35:.0f}" font-size="12" text-anchor="middle">샘플이 없다</text>

  <text class="lbl" x="{W/2}" y="{H-42}" font-size="14.5" text-anchor="middle">샘플이 드물수록 <tspan class="warn">보간 거리</tspan>가 멀어지고, 멀어질수록 추측이 크게 빗나간다</text>
  <text class="mut" x="{W/2}" y="{H-18}" font-size="13" text-anchor="middle">페인트볼로 치면 자국 밀도 — 촘촘한 데는 형상이 살고, 성긴 데는 사이를 지어내야 한다</text>
''')

