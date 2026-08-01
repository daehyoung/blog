# 시리즈 매핑 — 「LLM의 발전 과정과 에이전트」

> 이 폴더의 글들은 **원본(pillar)**을 주제별로 떼어낸 독립 글이다.
> 각 글은 끝에서 원본으로 링크하고, frontmatter로 원본 관계를 기록한다.
> 이 파일(`_` 접두사)은 사이트로 **빌드되지 않는** 내부 추적 문서다.

## 원본 (Pillar)

- 파일: `content/posts/2026-06-28-llm-agents.md`
- URL: `/blog/llm-agents`

## 분할 글 ↔ 원본 매핑

| 편 | 파일 | 제목 | 원본 출처(장·절) | URL | 상태 |
|---|---|---|---|---|---|
| 개요 | `00-overview.md` | 들어가며 — 왜 에이전트가 나타났는가 (목적 + 문제→해결 + 로드맵/가이드) | 시리즈 개요 | `/blog/llm-agents-series/00-overview` | ✅ 완료 |
| 1 | `01-llm-usage-tips.md` | LLM 잘 쓰는 법 12가지 | 부록 C | `/blog/llm-agents-series/01-llm-usage-tips` | ✅ 완료 |
| 2 | `02-why-llm-gets-heavy.md` | 왜 LLM은 점점 무거워지나 (컨텍스트·MoE·양자화) | 3·4·5장 + 부록 A | `…/02-why-llm-gets-heavy` | ✅ 완료 |
| 3 | `03-anatomy-of-an-agent.md` | 에이전트 해부 — 도구·루프·검증·하네스 | 7.1~7.5 | `…/03-anatomy-of-an-agent` | ✅ 완료 |
| 4 | `04-small-model-big-loop.md` | 작은 모델 + 루프가 큰 모델을 이긴다 | 7.6·7.7 | `…/04-small-model-big-loop` | ✅ 완료 |
| 5 | `05-rag-naive-vs-agentic.md` | RAG: 전통 파이프라인 vs 에이전트 루프 | 9장 | `…/05-rag-naive-vs-agentic` | ✅ 완료 |
| 6 | `06-agent-company-moat.md` | 에이전트 회사의 해자 — 공개 vs 비밀 | 10장 | `…/06-agent-company-moat` | ✅ 완료 |
| 7 (스핀오프) | `07-why-memory-shortage.md` | 메모리 부족은 언제 풀릴까 (시장·수요 관점) | 부록 A | `…/07-why-memory-shortage` | ✅ 완료 (§6 예측↔실측 표 보강, 참고자료 A·B 링크) |
| 참고자료 A | `08-memory-supply-demand.md` | 메모리 공급·수요 증가율 비율 분석 (2026 시장 데이터) | 부록 A / 외부 시장 데이터 | `…/08-memory-supply-demand` | ✅ 완료 |
| 참고자료 B | `09-token-usage-benchmark.md` | 모델별 토큰 사용량 실측 벤치마크 (자체 측정) | 부록 A / 자체 측정 | `…/09-token-usage-benchmark` | ✅ 완료 |

## 시리즈 랜딩(개요)

- **별도 Astro 인덱스 페이지 없음.** `00-overview.md`(들어가며)가 개요·랜딩 역할을 겸한다. (AI 코딩 실전과 동일한 방식)
- 내용: **왜 이 시리즈를 쓰게 되었나**(동기) + **무엇을 다루나**(로드맵, 편별 한 줄 요약) + **이렇게 읽으세요**(독자 유형별 가이드) + 원본 링크.
- frontmatter에 `series_order` 없음 → 홈 시리즈 목록에서 `?? 0`으로 **맨 앞**에 정렬, post-no 라벨 없이 제목만 노출.
- 새 편 추가 시 이 글의 "로드맵" 목록도 함께 갱신할 것.

## 추적 규칙

1. 각 글 frontmatter에 다음을 기록한다:
   - `series`: 시리즈 이름 (고정)
   - `series_order`: 편 번호
   - `source_post`: 원본 파일명 (`2026-06-28-llm-agents`)
   - `source_sections`: 원본에서 가져온 장·절 목록
2. **원본을 수정하면**, 영향을 받는 편의 상태를 `⬜ 재검토`로 바꿔 동기화한다.
3. 분할 글에서 원본의 다른 장을 가리킬 때는, 아직 안 나온 형제 글 대신 **원본(pillar)의 해당 섹션**으로 링크한다.

## 도해 (2026-08-01 추가)

원본(pillar)과 분할 편에 그림을 넣었다. **원본을 고치면 같은 그림을 쓰는 편도 함께 본다.**

| 어디 | 무엇 | 형식 |
|---|---|---|
| pillar §4 · 2편 | **모델은 층이 쌓인 구조** / **Dense FFN vs MoE 블록** | SVG `public/llm-agents/{model-layers,moe-block}.svg` — 생성기 `scripts/gen-llm-agents-svg.py` |
| pillar §4 · 2편 | 한 층의 전문가 풀(라우터 + top-k) | mermaid (pillar만) |
| pillar §7.1 · 3편 | 도구 사용 3층 + MCP + 실행 위치 경계 | mermaid |
| pillar §7.2 · 3편 | 에이전트 루프(4.a 되돌아감) | mermaid |
| 4편 | pⁿ 복리 오류 — 검증 없는 사슬 vs 검증 박힌 루프 | mermaid |
| pillar §9 · 5편 | 전통 RAG / Agentic RAG | mermaid |

⚠️ **왜 신경망 그림을 먼저 넣었나**: 기존 MoE 도해(라우터 + 전문가 풀)만 보면 **모델에 층이 하나뿐인 것처럼** 읽힌다. 실제로는 블록마다 라우터가 따로 있고 층마다 새로 고른다. 그 오해를 끊는 게 목적이라 **MoE 설명보다 앞에** 놓아야 한다.

⚠️ **mermaid 문법은 빌드가 안 잡는다.** 새 블록을 넣으면 `node scripts/check-mermaid.mjs <파일>` 로 검증할 것.

## 상태 범례

- ✅ 완료 (발행 가능)
- 🟡 작성 중
- ⬜ 예정
- 🔁 재검토 (원본 변경으로 동기화 필요)
