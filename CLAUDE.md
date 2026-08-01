# CLAUDE.md — 작업 프로토콜

> 이 파일은 설명서가 아니라 **행동 규칙**이다. 작업 전 반드시 따른다.
> (배경 철학: [코딩 에이전트와 장기 협업하는 문서화 시스템](content/posts/ai-coding-series/01-doc-system-for-llm-collaboration.md))

## 0. 작업 시작 전

1. **`current_tasks.md`를 먼저 읽어** 직전 작업 상태·다음 할 일·주의사항을 파악한다.
2. 이 파일(`CLAUDE.md`)의 규약을 확인한다.

## 1. 프로젝트 개요

Astro 정적 블로그. LLM·AI 에이전트·온프레미스·AI 코딩 주제의 한국어 기술 글.
GitHub Pages 배포: **https://daehyoung.github.io/blog/** (프로젝트 페이지, base `/blog`).

## 2. 구조

```
content/drafts/                  # 작성 중 초안. 빌드 제외 + git 추적 안 함(.gitignore)
content/posts/
  2026-06-28-llm-agents.md      # 원본(pillar)
  llm-agents-series/            # 시리즈: LLM 발전과 에이전트 (이론)
  ai-coding-series/             # 시리즈: AI 코딩 실전
  <series>/_map.md             # 시리즈별 원본↔분할 추적 (빌드 제외)
src/
  layouts/Layout.astro          # 디자인·다크모드·이메일 난독화·byline
  pages/index.astro             # 홈 (series별 그룹, series_order 정렬)
  pages/[...slug].astro         # 글 페이지 (byline 자동 출력)
  pages/tags/                   # 태그 목록 + 태그별 필터
  content.config.ts             # 컬렉션 스키마 (frontmatter)
social/                         # 배포 초안(LinkedIn 등). 빌드 안 됨
```

## 3. 글 추가 규칙

### 0) 글의 세 가지 상태 — 어디에 두느냐로 정해진다

| 상태 | 위치 | 사이트 | git |
|---|---|---|---|
| **작성 중** | `content/drafts/` | 안 뜸(컬렉션 밖) | **추적 안 함**(.gitignore) |
| **완성·보류** | `content/posts/` + `draft: true` | 안 뜸(게이트) | 커밋함 |
| **예약 발행** | `content/posts/` + 미래 `date` | 그날 cron이 공개 | 커밋함 |

- **새 글은 `content/drafts/`에서 시작한다.** 완성·검토가 끝나면 `content/posts/`로 옮긴다(그때 발행이다).
- `content/drafts/`는 컬렉션 `base` 밖이라 **어떤 실수로도 사이트에 뜨지 않는다.** 게다가 git이 추적하지 않으므로 **공개 리포 소스에도 노출되지 않는다**(이 리포는 public이다).
- `draft: true`는 *완성됐지만 지금은 안 내보내는* 글에 쓴다(예: 근거 논문 대기). 미완성 초안을 posts에 두고 플래그로 막는 방식은 **쓰지 않는다.**
- ⚠️ **`git add -A content/posts` 금지.** 경로를 명시해 add한다. 과거에 이 명령으로 미검토 에세이가 커밋돼 예약 공개 직전까지 간 적이 있다.


1. `content/posts/<series>/NN-slug.md`로 작성. frontmatter 필수:
   ```yaml
   ---
   title: "..."
   date: 2026-06-29
   tags: [..]
   canonical_url: https://daehyoung.github.io/blog/<series>/<slug>/
   license: CC BY-NC 4.0
   series: "시리즈명"        # 홈 그룹 키
   series_order: N
   ---
   ```
   - `source_sections`에 `7.6` 같은 **소수점 값은 따옴표로** 감싼다(YAML이 숫자로 파싱).
2. 작성 후 해당 시리즈 **`_map.md` 상태표를 갱신**한다.
3. 시리즈 글은 끝에 **내비게이션**(이전/현재/다음 + 원본 링크)을 단다. **다음 편이 실제로 생기면 `(예정)`을 링크로 바꾼다.**
4. **문체 원칙: 문제(고통) → 해결 서사.**
5. **교차링크는 의무가 아니다.** "가능하면 걸어라"는 옛 규약(초기 pillar 분할 시절)이며 **폐기**한다. 링크는 독자가 실제로 얻을 게 있을 때만 건다.
   - 걸기 전 **대상 글 본문을 열어 그 내용을 정말 다루는지 확인**한다. *URL이 살아 있는 것 ≠ 내용이 맞는 것* — 빌드 통과는 이걸 못 잡는다.
   - 긴 글(20k자 이상)은 **절 단위로** 가리킨다. 가리킬 절이 없으면 링크하지 않는다.
   - `draft: true` 글로는 링크 금지(프로덕션 404).
6. 본문에 H1(`# 제목`)을 넣지 않는다 — 제목은 frontmatter→템플릿이 렌더(중복 방지).

## 4. 핵심 규약 (실측·하드 제약)

- **base `/blog`**: 내부 링크는 `/blog/...` 절대경로. 템플릿에선 `import.meta.env.BASE_URL.replace(/\/$/, '')`로 슬래시 정규화.
- **slug**: 파일명에서 경로 세그먼트별로 `^\d{4}-\d{2}-\d{2}-` 접두사 제거.
- **`_` 접두사 파일은 빌드 제외**(`_map.md` 등). 스키마: `glob({ pattern: ['**/*.md', '!**/_*.md'] })`.
- **코드블록**: shiki 듀얼 테마(`defaultColor:false`) + CSS `data-theme`로 라이트/다크 전환.
- **다이어그램**: ` ```mermaid ` 블록은 `astro-mermaid`가 렌더(다크모드 자동 연동).
- **이메일**: `luxsoft.kr@gmail.com`. 템플릿에서 `data-user`/`data-domain`로 난독화 → 생주소를 정적 HTML에 박지 말 것.
- **byline**: 작성일·작성자(조대형, 클로드)는 `[...slug].astro`가 자동 출력. 본문에 따로 적지 않는다.
- **예약 발행**: 모든 콘텐츠 쿼리는 `getPublishedPosts()`(`src/lib/posts.ts`)를 쓴다 — KST 기준 `date ≤ 오늘`만 공개. 새 글 `date`를 미래로 적고 푸시하면 일일 cron이 그날 자동 공개. **새 페이지 쿼리도 `getCollection` 직접 말고 이 헬퍼를 쓸 것.**

## 5. 작업 완료 시 (동기화)

1. **`npm run build`로 빌드 통과를 반드시 확인**(스키마/링크 오류 자주 발생).
2. 관련 문서 갱신: 해당 `_map.md`, 시리즈 내비, (필요 시) 이 `CLAUDE.md`.
3. 커밋에 문서 변경 포함. 커밋 메시지 끝에:
   `Co-Authored-By: Claude <모델명> (1M context) <noreply@anthropic.com>`
   - `<모델명>`은 **자리표시자다.** 작업한 세션의 실제 모델명으로 반드시 치환한다 (예: `Opus 5`).
   - 치환하지 않은 채로 커밋하지 않는다.
4. **`current_tasks.md` 갱신**(완료/진행/다음/주의).

## 6. 배포

- `main`에 push → GitHub Actions가 자동 빌드·배포.
- **push는 SSH**(`git@github.com:daehyoung/blog.git`). 샌드박스 환경에선 네트워크 때문에 `dangerouslyDisableSandbox`로 실행.
- Pages Source는 **GitHub Actions**여야 함(Settings → Pages).

## 7. 세션 종료 시

`current_tasks.md`에 완료/진행 중/다음 할 일/주의사항을 기록한다. 드리프트가 느껴지면 망설이지 말고 새 세션으로 전환(비용은 `current_tasks.md`가 흡수).
