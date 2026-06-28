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
| 1 | `01-llm-usage-tips.md` | LLM 잘 쓰는 법 12가지 | 부록 C | `/blog/llm-agents-series/01-llm-usage-tips` | ✅ 완료 |
| 2 | `02-why-llm-gets-heavy.md` | 왜 LLM은 점점 무거워지나 (컨텍스트·MoE·양자화) | 3·4·5장 + 부록 A | `…/02-why-llm-gets-heavy` | ✅ 완료 |
| 3 | `03-anatomy-of-an-agent.md` | 에이전트 해부 — 도구·루프·검증·하네스 | 7.1~7.5 | `…/03-anatomy-of-an-agent` | ✅ 완료 |
| 4 | `04-small-model-big-loop.md` | 작은 모델 + 루프가 큰 모델을 이긴다 | 7.6·7.7 | `…/04-small-model-big-loop` | ✅ 완료 |
| 5 | `05-rag-naive-vs-agentic.md` | RAG: 전통 파이프라인 vs 에이전트 루프 | 9장 | `…/05-rag-naive-vs-agentic` | ✅ 완료 |
| 6 | `06-agent-company-moat.md` | 에이전트 회사의 해자 — 공개 vs 비밀 | 10장 | `…/06-agent-company-moat` | ✅ 완료 |
| 7 (스핀오프) | `07-why-memory-shortage.md` | 메모리 부족은 언제 풀릴까 (시장·수요 관점) | 부록 A | `…/07-why-memory-shortage` | ✅ 완료 |

## 추적 규칙

1. 각 글 frontmatter에 다음을 기록한다:
   - `series`: 시리즈 이름 (고정)
   - `series_order`: 편 번호
   - `source_post`: 원본 파일명 (`2026-06-28-llm-agents`)
   - `source_sections`: 원본에서 가져온 장·절 목록
2. **원본을 수정하면**, 영향을 받는 편의 상태를 `⬜ 재검토`로 바꿔 동기화한다.
3. 분할 글에서 원본의 다른 장을 가리킬 때는, 아직 안 나온 형제 글 대신 **원본(pillar)의 해당 섹션**으로 링크한다.

## 상태 범례

- ✅ 완료 (발행 가능)
- 🟡 작성 중
- ⬜ 예정
- 🔁 재검토 (원본 변경으로 동기화 필요)
