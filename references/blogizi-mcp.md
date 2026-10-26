# Blogizi MCP — verified October 2026

Base URL: `https://blogizi.com/api/mcp` (Streamable HTTP). Authentication: account API key (Bearer), see https://blogizi.com/docs/mcp. Codex config depends on its supported authentication flow; do not hardcode keys into checked-in files.

## `list_projects`
No arguments. Returns blog IDs, names, and slugs. `projectSlug` is required on post tools for multi-project accounts.
Source: https://blogizi.com/docs/mcp-list-projects

## `draft_post`
Required: `title`, `slug`. Optional: `description`, `keyword`, `content`, `scheduledAt`, `coverImageUrl`, CTA fields, `projectSlug` (required for multiple projects). Duplicate slugs fail. Future scheduledAt leaves status draft until publication.
Source: https://blogizi.com/docs/mcp-draft-post

## `update_post`
Upsert by slug; requires `title`, `slug`; optional other draft fields, `status` draft/published, `scheduledAt`. Omitting schedule preserves it. Avoid unintentional upserts or changes to published content.
Source: https://blogizi.com/docs/mcp-update-post

## `upload_post_image`
Upload for an **existing post**. Required: `type` (`cover` or `content`), `filename`, `contentBase64`; identify post with `postId` or `slug`; `projectSlug` for multiple projects; `alt` optional for content images. Cover maximum **2MB**, content maximum **5MB**. PNG/JPG/WebP/SVG. Recommended cover dimensions **1200x630**. For `type=cover`, the image is saved on the post directly. For `type=content`, use returned Markdown in `update_post` content.
Source: https://blogizi.com/docs/mcp-upload-post-image

## `schedule_post`
Required: `scheduledAt` (ISO or local `YYYY-MM-DDTHH:mm` interpreted in project timezone; `null` clears), `slug` OR `postId`, and `projectSlug` if multiple projects. Scheduling does not rewrite content. Returned `post.scheduledAt` is UTC ISO. A future-scheduled post stays `status: "draft"` until Blogizi publishes it. Do not call `publish_post` unless user wants immediate publication.
Example: `{ "slug": "how-we-built-our-auth-flow", "scheduledAt": "2026-10-26T09:00", "projectSlug": "my-app" }`
Source: https://blogizi.com/docs/mcp-schedule-post

## Known gaps

- No `list_posts` or `get_content_calendar` tool established in these docs; inspect runtime for new tools or use another authorized inventory.
- Cover upload does not itself prove the final website emits an `og:image` tag; verify website output.
- MCP expects base64 bytes, not local paths. Large payloads may need a supported bridge or authenticated HTTP upload API.
