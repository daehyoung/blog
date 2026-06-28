// @ts-check
import { defineConfig } from 'astro/config';
import mermaid from 'astro-mermaid';

// https://astro.build/config
export default defineConfig({
  // GitHub Pages 프로젝트 페이지: https://daehyoung.github.io/blog/
  site: 'https://daehyoung.github.io',
  base: '/blog',
  // ```mermaid 코드블록을 다이어그램으로 렌더 (다크모드 data-theme 자동 연동)
  integrations: [mermaid({ theme: 'default', autoTheme: true })],
  // 코드블록: 라이트/다크 듀얼 테마 (CSS의 data-theme로 전환)
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: false,
      wrap: true,
    },
  },
});
