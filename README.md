# 조대형의 기술 노트 (Tech Notes)

LLM·AI 에이전트·온프레미스 시스템을 중심으로 정리한 기술 글 모음입니다.
이 저장소가 모든 글의 **원본(single source of truth)**이며, 여기서 GitHub Pages로 렌더링하고 다른 플랫폼으로 배포(syndication)합니다.

---

## 📂 저장소 구조

```
.
├─ content/posts/        # 모든 글(.md)을 여기에 작성
├─ assets/images/        # 글에 쓰는 이미지
├─ .github/workflows/    # GitHub Pages 자동 배포 · syndication 워크플로
├─ LICENSE               # 코드·설정용 (Apache-2.0)
├─ LICENSE-CONTENT.md    # 글(콘텐츠)용 (CC BY-NC 4.0)
└─ README.md
```

> 글쓰기는 `content/posts/`에 `.md` 파일을 추가하는 것으로 끝납니다.
> push하면 GitHub Pages가 자동으로 다시 빌드됩니다.

---

## ✍️ 글 작성 방법

1. `content/posts/`에 `YYYY-MM-DD-slug.md` 형식으로 파일을 만든다.
2. 맨 위에 frontmatter를 넣는다:

   ```yaml
   ---
   title: "글 제목"
   date: 2026-06-28
   tags: [LLM, Agent, RAG]
   canonical_url: https://blog.example.com/slug   # 원본 주소(이 사이트) 고정
   license: CC BY-NC 4.0
   ---
   ```

3. 본문을 마크다운으로 작성한다.
4. `git add` → `git commit` → `git push`.

`canonical_url`을 박아두면, 다른 블로그로 배포할 때 검색 점수가 원본(이 사이트)으로 모입니다.

---

## 🔗 배포 전략 (Publish once, distribute everywhere)

이 저장소의 글 하나를 원본으로 두고 여러 채널로 퍼뜨립니다.

```
.md 작성 → 이 repo에 push
        ├─→ GitHub Pages 자동 빌드 ........... 원본 사이트 (canonical)   [자동]
        ├─→ dev.to / Hashnode ................ canonical=원본 지정       [자동, 예정]
        ├─→ velog / 티스토리 ................. 도입부 + 원본 링크         [수동]
        └─→ LinkedIn ......................... 핵심 관점 요약 + 링크      [수동]
```

- **canonical은 항상 이 저장소(GitHub Pages)**로 고정한다.
- velog·티스토리는 canonical 설정이 제한적이므로 **전문 대신 "도입부 + 원본 링크"**로 올린다.
- 마크다운 방언 차이로 각주·표가 깨질 수 있으니, 자동 배포 후 한 번씩 확인한다.

---

## 📝 글 목록

| 날짜 | 제목 | 태그 |
|---|---|---|
| 2026-06-28 | [LLM의 발전 과정과 에이전트 — 문제와 해결의 연쇄](content/posts/2026-06-28-llm-agents.md) | LLM, Agent, RAG, MoE, Quantization |

---

## ⚖️ 라이선스

이 저장소는 **이중 라이선스**입니다.

- 📝 **글(콘텐츠)** — `content/`, `assets/`의 글·이미지: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
  출처를 밝히면 공유·인용·번역·수정이 가능하나, **상업적 이용은 허용하지 않습니다.** ([LICENSE-CONTENT.md](LICENSE-CONTENT.md))
- 💻 **코드·설정** — 사이트 생성기 설정, 스크립트, GitHub Actions: [Apache-2.0](LICENSE)

> 인용 시: 글 제목, 작성자(조대형), 원본 링크를 함께 표기해 주세요.

---

## 👤 작성자

- **조대형** · luxsoft.kr@gmail.com
- 글 일부는 Claude(Anthropic)와 협업해 작성·교정했습니다.
