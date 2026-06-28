import { getCollection } from 'astro:content';

// 예약 발행: frontmatter의 date가 '한국 날짜로 오늘 이하'인 글만 공개한다.
// (KST = UTC+9. 빌드 시각 기준이라, 매일 cron 리빌드가 그날 글을 자동 공개)
const KST_OFFSET_MS = 9 * 60 * 60 * 1000;

export async function getPublishedPosts() {
  const todayKST = new Date(Date.now() + KST_OFFSET_MS).toISOString().slice(0, 10);
  return (await getCollection('posts')).filter(
    (p) => !p.data.draft && p.data.date.toISOString().slice(0, 10) <= todayKST,
  );
}
