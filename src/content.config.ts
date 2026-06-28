import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// 루트의 content/posts/**/*.md 를 'posts' 컬렉션으로 읽는다 (README 구조 유지)
// '_' 접두사 파일(예: _map.md)은 추적용 내부 문서이므로 빌드에서 제외한다.
const posts = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!**/_*.md'], base: './content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).optional(),
    canonical_url: z.string().url().optional(),
    license: z.string().optional(),
    draft: z.boolean().optional(),
    // 시리즈 추적 (원본 ↔ 분할 관계)
    series: z.string().optional(),
    series_order: z.number().optional(),
    series_label: z.string().optional(), // 카드 뱃지 표기 override (예: "에필로그")
    source_post: z.string().optional(),
    source_sections: z.array(z.string()).optional(),
  }),
});

export const collections = { posts };
