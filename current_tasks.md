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

## 아직 push 안 한 변경 (중요)

> 디자인 리뉴얼·태그·byline·이메일 변경·Mermaid·AI 코딩 1편·CLAUDE.md/current_tasks.md가 **로컬에만 있고 아직 커밋/푸시 전**일 수 있음. 다음 세션은 `git status` 확인 후 커밋·푸시.

## 다음에 할 일

1. **빌드 확인 후 커밋·푸시** (위 변경분 일괄). 커밋 메시지 분리 권장(디자인 / 태그 / AI코딩 시리즈).
2. **AI 코딩 시리즈 2~7편** 작성 (지형도·태스크 주는 법·컨텍스트·검증·디버깅·함정). 전부 문제→해결 톤.
3. AI 코딩 1편의 "다음 편 *(예정)*" → 2편 생기면 링크로 교체.
4. (선택) About 페이지 + 헤더 "소개" 메뉴 + footer 이메일.
5. (선택) 7편 외 다른 편 LinkedIn 요약(`social/`).

## 주의사항

- 새 글마다 `npm run build` 통과 확인 필수(frontmatter 스키마·내부 링크 오류 빈발).
- `source_sections`의 `7.6` 등 소수점은 **따옴표** 필수.
- push는 SSH + 샌드박스 해제. Pages Source = GitHub Actions 유지.
- 이메일 생주소를 정적 HTML/문서에 노출하지 말 것(난독화 유지).
