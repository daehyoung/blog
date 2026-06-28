# 시리즈 매핑 — 「AI 코딩 실전」

> LLM 코딩 도구를 **실제로 다루는 현장**을 다루는 시리즈.
> 톤 원칙: **문제(고통) → 해결** 서사 (블로그 정체성 "문제와 해결의 연쇄"와 일치).
> 이 파일(`_` 접두사)은 사이트로 빌드되지 않는 내부 추적 문서다.

## 연결 이론 (뿌리)

- 「LLM의 발전 과정과 에이전트」 시리즈 → `/blog/llm-agents`

## 글 목록

| 편 | 파일 | 제목 | 출처 / 발행일 | 상태 |
|---|---|---|---|---|
| 개요 | `00-overview.md` | AI 코딩의 문제는 사람 팀이 이미 푼 문제다 | 06-29 | ✅ 발행 |
| 1 | `01-doc-system-for-llm-collaboration.md` | 코딩 에이전트와 장기 협업하는 문서화 시스템 | `llm-collaboration-doc-system-guide.md` / 06-29 | ✅ 발행 |
| 2 | `02-tokens-context-keep-light.md` | 토큰·컨텍스트를 가볍게 유지하는 법 | `ai-context.md` / **07-02 예약** | 🟡 예약발행 |
| 3 | `03-divide-and-conquer.md` | 분할정복 — 모듈로 쪼개 AI와 일하기 | `ai-context.md` / **07-05 예약** | 🟡 예약발행 |
| 4 | `04-docs-over-code.md` | 코드보다 문서다 — AI 시대의 역전 | `development_workflow.md` 부록A / **07-08 예약** | 🟡 예약발행 |
| 5 | `05-verify-design-before-code.md` | 코드 쓰기 전에 설계를 검증하라 | `development_workflow.md` 본문 / **07-11 예약** | 🟡 예약발행 |
| 6 | `06-workflow-as-agent-prompts.md` | 워크플로우를 에이전트에게 — 자동화 경계·단계별 프롬프트 | `development_workflow.md` / **07-14 예약** | 🟡 예약발행 |
| 에필로그 | `07-epilogue-the-bar-rises.md` | AI가 되살린 엔지니어링, 더 높아진 사람의 격 | `development_workflow.md` 부록A / **07-18 예약** | 🟡 예약발행 |

> 시리즈는 **에필로그로 완결**. (도구 지형도·디버깅·함정 등은 추후 선택적 추가 — 추가 시 에필로그 앞 8~번대로.)

## 핵심 thesis (개요)

AI 코딩의 고통 = **사람 팀이 이미 푼 문제**. AI가 사람을 닮아 해법(모듈화·문서·ADR·리뷰·인터페이스)이 통하고, **사람을 닮아 약점도 물려받음**. 바이브코딩(말로만 하기)의 비효율 → 구조(문서·모듈·인터페이스)로 해결.

## 예약 발행 메모

- 2·3편은 frontmatter `date`가 미래(07-02/07-05) → 그날 cron 리빌드로 자동 공개.
- 개요·1편의 "다음 편"은 깨진 링크 방지를 위해 **링크 없이 '(공개 예정)' 표기**. 공개되면 링크로 바꿔도 됨(또는 dynamic nav 도입 검토).

## 추적 규칙

- 각 글 frontmatter: `series: "AI 코딩 실전"`, `series_order`, (해당 시) `source_post`.
- 모든 글은 **문제 제기 서론 → 처방** 구조를 따른다.
- 가능하면 기존 이론 시리즈(`/blog/llm-agents...`)의 해당 개념으로 교차링크한다.

## 상태 범례

- ✅ 완료 · 🟡 작성 중 · ⬜ 예정
