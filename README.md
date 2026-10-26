# Blogizi SEO Autopilot

Codex skill for SEO content planning and production on [Blogizi](https://blogizi.com). It researches a business website, audits existing posts, discovers and scores keywords with DataForSEO, writes sourced articles with a TL;DR and internal links, generates OG and inline images with Codex imagegen, then uploads assets and schedules posts through Blogizi MCP.

This package is instructions and helper scripts. It is not an unattended scheduler. Blogizi publishes a post after `schedule_post` succeeds. Full agent instructions are in `SKILL.md`. If a reference file disagrees with that workflow, `SKILL.md` wins.

## Requirements

- Codex with Blogizi MCP and DataForSEO connected. Tool schemas are discovered at runtime.
- Codex built-in `$imagegen`. Do not use a third-party image MCP by default.
- Python 3 and Pillow (`python -m pip install Pillow`) for `scripts/prepare_og.py`.
- A Blogizi account API key so cover and content images can be uploaded as base64 with `upload_post_image`. Local file paths are not a substitute.

## Install

Copy this directory to `~/.agents/skills/blogizi-seo-autopilot/` (or your project's `.agents/skills/blogizi-seo-autopilot/`) so `SKILL.md` sits at the skill root.

## What a run does

The agent acts as orchestrator: onboarding, strategy, keyword scoring, editorial review, Blogizi writes, scheduling, and the final report. Bounded research and drafting can be delegated to cheaper workers when the runtime supports it. Workers must not schedule, publish, upload, or modify Blogizi posts. The orchestrator reviews worker output before any write. Start with at most three concurrent workers.

### Onboarding

On a new campaign, missing details are collected in order. Information already provided is not asked again.

1. Marketing website URL, then a business research brief (product, audience, positioning, goals). Unverified features, prices, testimonials, and differentiators are not invented.
2. Blog URL, then the matching Blogizi project via `list_projects`. Multiple possible matches are not guessed.
3. Existing-post audit via `list_posts` (`status: "all"`, `limit: 100`, plus pagination or export only when the runtime actually supports it). Topics that duplicate an existing intent need a clear reason and approval.
4. Article length: short (800–1,200), standard (1,200–1,800), long-form (1,800–2,500), comprehensive (2,500–3,500), or adaptive. The range is a target, not padding.
5. Remaining preferences: country, language, audience, brand voice, article count, publishing frequency, timezone, preferred time, OG style, whether images include text, inline image count, and API or image budget. Publishing dates and times are never invented.

### Research and planning

Seed topics come from the business brief, not from volume or difficulty alone. DataForSEO supplies ideas, volume, difficulty, intent, related searches, and SERP results for the target location and language. The target is at least 30 candidates and 10 distinct opportunities when the budget allows, clustered by overlapping intent and checked against the existing inventory.

Each opportunity is scored 0–100:

| Factor | Weight |
|---|---:|
| Business relevance | 30% |
| Search intent and conversion potential | 25% |
| Ranking feasibility | 20% |
| Keyword cluster demand | 15% |
| Topical authority and linking value | 10% |

Prefer keywords with at least 100 monthly searches when comparable options exist. Lower-volume topics are allowed when strategic or commercial value is strong. Missing metrics are not filled in. Overlapping volumes are not summed as unique users.

Before writing, the top five opportunities are shown (keyword, volume, difficulty, intent, supporting keywords, score, business rationale, SERP evidence). A single-article run needs topic approval. A larger paid batch needs an approved content calendar first.

### Writing

Each article is researched against current SERPs, outlined from sources, and written in original Markdown: H1, introduction, TL;DR (3–5 bullets after the intro), H2/H3 sections, examples, about 2–5 contextual internal links when relevant published posts exist, verified external links, inline images, and a conclusion. Meta descriptions aim for 160 characters or fewer. URLs, statistics, studies, quotes, product features, and citations are not invented. Existing published posts are not edited for reciprocal links without approval.

### Images and Blogizi writes

1. `draft_post` creates the post before any image upload. The schedule is not set yet. A failed or uncertain response is not followed by a blind recreate.
2. `$imagegen` makes a unique landscape cover from an article-specific brief. `scripts/prepare_og.py` center-crops it to 1200×630 WebP under 2 MB. The script does not create artwork or add branding.
3. `upload_post_image` with `type: "cover"` stores the cover on the post. Cover attachment alone does not prove `og:image` is rendered.
4. Inline images follow the user's count. Defaults: 1 (short), 1–2 (standard), 2–3 (long-form), 3–4 (comprehensive). `upload_post_image` with `type: "content"` (5 MB limit) returns a Markdown snippet. That snippet is inserted, then the full body is saved with `update_post`. Image URLs are not invented. Factual charts use verified data and a deterministic charting tool.

### Scheduling and reporting

`schedule_post` runs only when the user has authorized the date and time, in the project timezone. A draft with a confirmed future `scheduledAt` is scheduled. Do not call `publish_post` to schedule.

A local manifest tracks each article:

`planned` → `researched` → `written` → `reviewed` → `drafted` → `cover_uploaded` → `inline_images_uploaded` → `content_updated` → `validated` → `scheduled`

A step is marked complete only after confirmation. The final report lists keyword, volume, difficulty, score, word count, TL;DR, link counts, image status, slug, post ID, schedule, and any errors. Success is reported only from tool confirmation.

The first run is one article through the full path above. Scale to a campaign only after that test succeeds.

## Package

| Path | Role |
|---|---|
| `SKILL.md` | Agent workflow |
| `references/blogizi-mcp.md` | Blogizi MCP notes |
| `references/quality.md` | Article, image, and scheduling checklist |
| `scripts/prepare_og.py` | Crop and compress the OG image |
| `scripts/manifest.py` | Record local campaign progress |

Blogizi docs referenced by the skill: [list posts](https://blogizi.com/docs/mcp-list-posts), [upload post image](https://blogizi.com/docs/mcp-upload-post-image), [update post](https://blogizi.com/docs/mcp-update-post), [schedule post](https://blogizi.com/docs/mcp-schedule-post).

## Invocation

```
$blogizi-seo-autopilot Create ONE test SEO article for my Blogizi project. Research using DataForSEO, generate a branded OG image using built-in imagegen, attach it as cover, and prepare it for scheduling. Ask before choosing a date/time or scheduling.
```
