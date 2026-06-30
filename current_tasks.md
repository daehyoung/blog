# 현재 작업 컨텍스트

> 세션 핸드오프 문서. 새 세션은 `CLAUDE.md` → 이 파일 순으로 읽는다.

## 프로젝트 한 줄

Astro 블로그(`/blog`), GitHub Pages 배포. LLM/에이전트 이론 시리즈 + AI 코딩 실전 시리즈.

## 완료된 것

- **이론 시리즈**: 원본(`2026-06-28-llm-agents`) + `llm-agents-series/` 1~6편 + 스핀오프 7편(메모리 부족). 앞뒤 내비 링크 연결됨.
- **디자인 리뉴얼**: AstroPaper풍 미니멀 모던 — Pretendard, 다크모드 토글, 블루 액센트, 카드형 목록, 듀얼 테마 코드.
- **태그 기능**: `/tags` 목록 + `/tags/<태그>` 필터, 카드/글의 태그칩 클릭 가능.
- **byline**: 글마다 작성일·작성자(조대형 + 이메일 난독화 `luxsoft.kr@gmail.com`, 클로드) 자동 출력.
- **Mermaid**: `astro-mermaid` 도입(다크모드 연동). 검증 완료.
- **AI 코딩 시리즈 시작**: `ai-coding-series/01-doc-system-for-llm-collaboration.md` (원문 가이드를 **문제→해결** 서사로 재구성). `_map.md` 작성.
- **문서화 시스템 도그푸딩**: 이 repo에 `CLAUDE.md` + `current_tasks.md` 도입.
- **예약 발행 세팅**: `getPublishedPosts()`(KST date 게이트) + 일일 cron. 미래 날짜로 푸시 → 자동 drip.
- **AI 코딩 시리즈 확장**(원문 `ai-context.md` 기반):
  - `00-overview.md` 개요(06-29, "AI 코딩 문제 = 사람 팀이 이미 푼 문제 / 약점도 물려받음 / 바이브코딩=말로만 하기의 비효율") — 발행.
  - `02-tokens-context-keep-light.md`(07-02 예약), `03-divide-and-conquer.md`(07-05 예약) — 작성, 게이트로 대기.
  - (원문 `development_workflow.md` 기반) `04-docs-over-code.md`(07-08), `05-verify-design-before-code.md`(07-11), `06-workflow-as-agent-prompts.md`(07-14), `07-epilogue-the-bar-rises.md`(에필로그, 07-18) — 작성, 게이트로 대기. **시리즈는 에필로그로 완결.**
  - 카드 뱃지 override용 `series_label`(예: "에필로그") 스키마·index 추가.
  - 시리즈 thesis: 구조로 소통 / 코드→문서 역전 / 자동화 경계(개념·요구=사람, 나머지=에이전트) / 단계별 프롬프트 + 검증 게이트(= 에이전트 루프 검증 = pⁿ).

## 최근 푸시 상태

> 디자인 리뉴얼·태그·byline·이메일·Mermaid·AI코딩 1편·CLAUDE.md/current_tasks.md 모두 **푸시 완료**
> (커밋 `2c3945d` 디자인 / `5a85bd3` 콘텐츠 / `0e33303` AI코딩+문서 / `d4f9f98` 예약발행 → origin/main, GitHub Actions 배포됨).
> **AI 코딩 시리즈 완결**(00 + 02~07편 + `series_label` 스키마 + index/_map) **푸시 완료** — 00·01편 발행, 02~07편 미래 날짜 drip 대기.
> **이번 세션 푸시**: `b44634d` 목록 디자인(AstroPaper풍 단순 목록, 섹션 타이틀 구분선) / `c916094` LLM pillar 보강(목차 앵커 링크 + MoE mermaid 구조도 + 활성파라미터 설명 박스). 새 초안 `2026-06-30-how-llms-work.md`(draft)는 별도 커밋.

## 다음에 할 일

1. ✅ **발행 cadence — 완료(①)**: future-date 게이트(`src/lib/posts.ts`, KST 기준 `date ≤ 오늘`만 공개) + 일일 cron(`.github/workflows/deploy.yml`, 00:00 UTC=09:00 KST 리빌드).
   - **새 글 발행법**: frontmatter `date`를 원하는 **미래 날짜**로 적고 그냥 푸시 → 그 날짜(KST 09시 cron)에 **자동 공개**. 여러 편을 미래 날짜로 한 번에 푸시해도 하나씩 뜸.
   - 급히 즉시 공개: Actions 탭에서 `workflow_dispatch` 수동 실행, 또는 `draft:true` 병행 사용.
2. ✅ **AI 코딩 시리즈 00·02~07편 완료** — 작성·빌드·커밋·푸시 끝. 02~07편은 미래 날짜 drip 대기.
3. ✅ AI 코딩 1편의 내비 링크 연결됨(다음 편 실제 존재).
4. **신규 pillar 집필 중**: `2026-06-30-how-llms-work.md`(「LLM은 어떻게 작동하는가 — 토큰 하나가 답이 되기까지」, **draft**). 입문·비유 중심 롱폼 10장 + 부록 A~E. 목차/골격 완성, `› (초안)` 메모를 본문으로 채우는 단계. 비유 줄기: 자동완성→레고→**유유상종 지도**→형광펜→끝말잇기. **출처 명시 완료**(라시카 『Build a LLM (From Scratch)』 학습 기반 → 최상단 「이 글에 대하여」 박스 + 미주 [^4][^5][^6] + 부록 E 코드 헤더 규칙). 재료: 루트 `01_embedding.md`·`02_attention.md`.
5. (선택) About 페이지 + 헤더 "소개" 메뉴 + footer 이메일.
6. (선택) AI 코딩 시리즈 LinkedIn 요약(`social/`) — 현재 7편(메모리 부족)만 있음.
7. (모니터링) 07-02부터 격일 cron drip 공개가 의도대로 뜨는지 확인.

## 주의사항

- 새 글마다 `npm run build` 통과 확인 필수(frontmatter 스키마·내부 링크 오류 빈발).
- `source_sections`의 `7.6` 등 소수점은 **따옴표** 필수.
- push는 SSH + 샌드박스 해제. Pages Source = GitHub Actions 유지.
- 이메일 생주소를 정적 HTML/문서에 노출하지 말 것(난독화 유지).
