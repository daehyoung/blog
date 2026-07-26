---
title: "부록 — Claude Code 엔지니어링 플러그인: 이 방법론을 AI 파트너로"
date: 2026-07-25
tags: [ClaudeCode, AI코딩, 플러그인, 소프트웨어공학, 도구]
canonical_url: https://daehyoung.github.io/blog/ai-era-engineering/06-appendix-claude-plugins/
license: CC BY-NC 4.0
series: "AI 시대의 실전 엔지니어링"
series_order: 6
series_label: "부록"
---

> 📚 시리즈 **「AI 시대의 실전 엔지니어링」 부록**입니다. 본문이 *방법론*이라면, 이 부록은 그 방법론을 **Claude Code에서 AI 파트너로 적용·연습하게 돕는 도구** 이야기입니다.

AI는 이 공학을 *연습하기에 가장 좋은 파트너*이기도 합니다. 마침 Anthropic이 배포하는 **`knowledge-work-plugins`** 마켓플레이스의 **`engineering` 플러그인**이, 이 시리즈가 다룬 주제(디버깅·테스트·설계·리뷰)를 거의 그대로 스킬로 담고 있습니다.

## 설치

Claude Code에서 두 줄이면 됩니다.

```bash
# 1) 마켓플레이스 등록
claude plugin marketplace add anthropics/knowledge-work-plugins

# 2) engineering 플러그인 설치
claude plugin install engineering@knowledge-work-plugins
```

설치 후 `/plugin`(또는 `claude plugin list`)로 확인할 수 있습니다.

## 무엇이 들어있나 — 그리고 이 시리즈와의 매핑

`engineering` 플러그인(v1.2.0)은 스킬 10개를 제공합니다. 굵게 표시한 것이 이 시리즈와 직접 겹칩니다.

| 스킬 | 하는 일 | 이 시리즈 |
|---|---|---|
| **`debug`** | 재현 → 격리 → 진단 → 수정 구조화 디버깅 | **3편 디버깅** (같은 방법론) |
| **`testing-strategy`** | 테스트 전략·커버리지·테스트 계획 | **4편 유닛테스트** |
| **`system-design`** | API·데이터 모델·서비스 경계 설계 | 설계(유스케이스 하류) |
| `architecture` | ADR(결정 기록)·설계 검토 | 설계 |
| `code-review` | 보안·성능·정확성 코드 리뷰 | 품질 |
| `tech-debt` | 기술 부채 식별·우선순위 | 품질 |
| `documentation` | 기술 문서·런북·README | 문서화 |
| `incident-response` | 장애 대응·포스트모템 | 운영 |
| `deploy-checklist` | 배포 전 점검 | 운영 |
| `standup` | 스탠드업 업데이트 생성 | 협업 |

## 사용법 — 그냥 말하면 된다

이 스킬들은 슬래시 명령이 아니라 **상황을 자연어로 말하면 각 스킬의 설명(description)에 맞춰 자동 발동**합니다. 매뉴얼을 뒤질 필요 없이, 그냥 상황을 말하면 됩니다. 스킬별 발동 예:

- `debug` — *"스테이징은 되는데 프로덕션만 500 떨어져. 원인 찾아줘"*
- `testing-strategy` — *"이 결제 모듈, 뭘 어디까지 테스트해야 해?"*
- `system-design` — *"주문·결제·배송의 서비스 경계를 어떻게 나누지?"*
- `architecture` — *"Kafka vs SQS 골라주고, 결정 근거를 ADR로 남겨"*
- `code-review` — *"이 PR 머지 전에 보안·성능 관점으로 리뷰해줘"*
- `tech-debt` — *"이 레포에서 먼저 갚아야 할 기술 부채 top 5"*
- `documentation` — *"이 서비스 운영 런북 초안 잡아줘"*
- `incident-response` — *"방금 장애 났어. 대응 순서와 포스트모템 틀"*
- `deploy-checklist` — *"내일 배포 전 점검 항목 만들어줘"*
- `standup` — *"어제 한 일로 스탠드업 업데이트 써줘"*

어떤 스킬이 로드됐는지는 Claude Code가 그때그때 알려줍니다. 즉 [3편의 디버깅 파이프라인](/blog/ai-era-engineering/03-debugging-methodology), [4편의 테스트 전략](/blog/ai-era-engineering/04-unit-testing)을 **AI에게 붙여** 실전에서 굴릴 수 있습니다.

## 한 가지 정직하게 — 유스케이스는 빠져 있다

이 플러그인엔 **유스케이스/요구사항 전용 스킬이 없습니다.** 그래서 [1편(유스케이스)](/blog/ai-era-engineering/01-usecases-not-feature-lists)·[2편(모델 검증)](/blog/ai-era-engineering/02-model-verification)의 작업은 이 플러그인으로 대체되지 않습니다. 유스케이스·설계 검증은 본문에서 다룬 방법으로 직접 하고, 이 플러그인은 그 *다음* 단계(구현·리뷰·디버깅·테스트·배포)에서 손발을 맞추는 용도로 보시면 됩니다.

> 다른 마켓플레이스 플러그인(`product-management`·`design`·`data` 등)도 같은 방식으로 설치됩니다 — `claude plugin install <이름>@knowledge-work-plugins`.

## 최선은 직접 쓰는 것 — 플러그인은 그다음

한 가지 오해를 막아둡니다. **가장 좋은 건 이 방법론을 *직접* 쓰는 것입니다.** 앞선 시리즈에서 강조한 [작업 지침](/blog/teaching-swe-to-models/04-work-instructions)·[관리 문서 시스템](/blog/ai-coding-series/01-doc-system-for-llm-collaboration)과 워크플로우는 *당신의 도메인·팀·코드베이스*에 맞춰져 있어, 어떤 범용 스킬보다 정확합니다. 플러그인 스킬은 **범용 방법론**이라 당신의 맥락을 모릅니다.

그러니 우선순위는 이렇습니다:

1. **최선** — 워크플로우·작업 지침·관리 문서를 *직접* 쓴다(내 맥락에 맞음).
2. **차선** — 그게 없으면, 플러그인 스킬이라도 얹는다(범용이라도 맨몸보단 낫다).
3. **최악** — 아무 방법론 없이 자연어만 던진다.

**없는 것보단 플러그인이라도 있는 게 낫습니다.** 다만 그건 *직접 쓰기까지의 발판*이지 종착지가 아닙니다.

## 스킬은 자연어로 쓴 프로그램이다

마지막으로 짚고 갈 게 있습니다. 이 블로그의 출발 명제는 *"자연어가 프로그래밍 언어가 되었다"*였는데 — **이 플러그인들이 바로 그 명제의 실물**입니다.

`SKILL.md`를 열어보면 코드가 아니라 **산문**입니다. "이런 상황이면 이렇게 하라, 이 순서로 점검하라"는 자연어 절차. 그런데 그게 *프로그램처럼 동작*합니다 — 패키지로 묶이고(`plugin`), 버전이 붙고(v1.2.0), **패키지 매니저로 설치**되고(`claude plugin install`), 런타임(LLM)이 그걸 읽어 실행하죠. 소스가 프로그래밍 언어가 아니라 **자연어**일 뿐, 소프트웨어의 배포·버전·재사용 생태계를 그대로 갖췄습니다.

그러니 앞 절의 사다리를 다시 보면 —

- **직접 쓰는** 워크플로우·작업 지침·관리 문서 = *당신이 자연어로 짠 프로그램*(내 도메인에 맞춤)
- **플러그인 스킬** = *남이 자연어로 짜서 배포한 프로그램*(범용 라이브러리)

둘 다 **자연어로 쓴 프로그램**입니다. 차이는 맞춤이냐 기성품이냐일 뿐 — 코드를 직접 짤지 라이브러리를 가져다 쓸지 고르는 것과 똑같습니다. 그래서 최선은 직접 쓰기고, 없으면 스킬을 얹는 겁니다.

이게 시리즈를 한 바퀴 돌려 닫습니다. 자연어가 프로그래밍 언어가 됐다고 *프로그래밍이 사라지는* 게 아닙니다 — **문법이 자연어로 바뀌었을 뿐**이죠. 그러니 잘 짜인 자연어(명세·설계·검증·지침)를 쓰는 능력, 곧 **소프트웨어 공학**이 그대로 사람의 핵심 기술로 남습니다.

---

#### 📚 시리즈 내비게이션

- **이전:** [4편 · 유닛테스트를 어떻게 쓰는가](/blog/ai-era-engineering/04-unit-testing)
- **부록 (지금):** Claude Code 엔지니어링 플러그인 ← 현재 글 · **시리즈 끝**
- **처음으로:** [개요 · 코딩은 과학이다](/blog/ai-era-engineering/00-overview)
