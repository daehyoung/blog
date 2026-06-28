// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // GitHub Pages 프로젝트 페이지: https://daehyoung.github.io/blog/
  site: 'https://daehyoung.github.io',
  base: '/blog',
  // 마크다운 코드블록 하이라이팅 등 기본값 사용
  markdown: {
    shikiConfig: { theme: 'github-light', wrap: true },
  },
});
