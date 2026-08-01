#!/usr/bin/env node
// 마크다운 안의 mermaid flowchart 블록을 '문법만' 검증한다.
//
// 왜 필요한가: 빌드는 mermaid 문법 오류를 잡지 못한다(블록을 그대로 통과시켜
// 브라우저에서 깨진다). 그렇다고 mermaid.parse()를 그냥 부르면 DOM이 없어
// 실행 자체가 안 된다 — jsdom을 깔지 않으려고 flowchart 파서만 직접 물렸다.
//
// 한계(정직하게): jison 문법 단계까지만 본다. 그 다음 sanitize 단계는 DOM이
// 필요해 건너뛰므로, 거기서 걸리면 '문법 OK'로 취급한다. 괄호 미닫힘·subgraph
// 미종료 같은 구조 오류는 잡지만, `==!>` 처럼 토큰으로는 삼켜지는 오타는 못 잡는다.
// 즉 '통과 = 반드시 렌더된다'가 아니라 '실패 = 확실히 깨진다'로 쓸 것.
//
// 사용: node scripts/check-mermaid.mjs content/posts/*.md
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { globSync } from 'node:fs';

const require = createRequire(import.meta.url);
// mermaid는 flowchart를 청크로 쪼개 내보낸다. 해시가 붙어 있어 이름을 고정할 수 없다.
const dir = require.resolve('mermaid/package.json').replace(/package\.json$/, 'dist/chunks/mermaid.core/');
const chunk = globSync('flowDiagram-*.mjs', { cwd: dir })[0];
if (!chunk) { console.error('flowDiagram 청크를 못 찾음:', dir); process.exit(2); }
const m = await import(dir + chunk);

const files = process.argv.slice(2);
if (!files.length) { console.error('사용: node scripts/check-mermaid.mjs <파일…>'); process.exit(2); }

let checked = 0, bad = 0;
for (const f of files) {
  const blocks = [...readFileSync(f, 'utf8').matchAll(/```mermaid\n([\s\S]*?)```/g)].map((x) => x[1]);
  for (const [i, b] of blocks.entries()) {
    const head = b.trim().split('\n')[0];
    if (!/^(flowchart|graph)\b/.test(head)) continue; // flowchart 외 타입은 이 파서 소관이 아니다
    checked++;
    const d = m.createFlowDiagram();
    d.parser.parser.yy = d.db;
    try {
      await d.parser.parse(b);
    } catch (e) {
      const msg = String(e.message).split('\n')[0];
      if (/DOMPurify/.test(msg)) continue; // 문법은 통과, sanitize에서만 멈춘 것
      bad++;
      console.log(`✗ ${f} #${i + 1} (${head})\n  ${String(e.message).split('\n').slice(0, 4).join('\n  ')}`);
    }
  }
}
console.log(bad ? `\n✗ flowchart ${checked}개 중 ${bad}개 문법 실패` : `✓ flowchart ${checked}개 문법 통과`);
process.exit(bad ? 1 : 0);
