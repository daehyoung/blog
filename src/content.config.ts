import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// 루트의 content/posts/*.md 를 'posts' 컬렉션으로 읽는다 (README 구조 유지)
const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).optional(),
    canonical_url: z.string().url().optional(),
    license: z.string().optional(),
    draft: z.boolean().optional(),
  }),
});

export const collections = { posts };
