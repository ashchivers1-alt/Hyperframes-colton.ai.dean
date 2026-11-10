# Creator Profile — Ash | Team Apexx

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Name on-screen**: Ash | Team Apexx
- **Instagram**: @ash_teamapexx
- **TikTok**: @ash_teamapexx
- **YouTube**: @thebodybuildingcoach_ash
- **X / other**: —

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

**Instagram Reels first** (cross-post to TikTok / Shorts optional). Default format: **9:16 vertical, 1080×1920**, 30fps. Design for the Reels UI safe zones (keep key text out of the bottom ~20% and right-edge icon column).

## Content niche

**Bodybuilding, contest prep, physique coaching, and training.** Ash coaches under the Team Apexx brand. Assume this niche for every new video unless told otherwise. Typical topics: prep-phase updates, training breakdowns, posing, nutrition/peak week, client transformations, coaching tips.

## On-camera mix

**Both.** Some videos are face-cam (Ash on camera / in the gym), others are faceless (motion graphics, B-roll, client footage). Ask which mode at the start of each video if it isn't obvious.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mix of both.** Pick per video:

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

- **Logo**: `assets/brand/team-apexx-logo.svg` (source) + `assets/brand/team-apexx-logo.png` (trimmed, transparent). Red distressed brush-stroke X behind a gritty silver-white "TEAM APEX" wordmark. Copy into a project's `assets/` when used.
- **Palette** (in `assets/brand-tokens.css`): near-black `#0a0a0a` background, logo red `#d80609` accent (dark side `#922a2b`), white `#f6f6f6` text, silver `#a19f9f` secondary.
- **Feel**: gritty, hardcore, competition-stage. Red is the single hero accent — use it for emphasis words, stamps, and the X motif, not as a fill everywhere.
- **Display font**: bold condensed (Anton / Bebas Neue); bundle the font file per project.

## Inspiration creators

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>`.

Studied so far (2026-10-11):
- **@aubergine-avenger** — illustrate every key noun: yellow glow hero words, inset diagram cards, b-roll flashes, disclaimer box on PED topics
- **@colton-ai-dean** — face-cam bottom half + self-assembling glass UI cards top half, numbered steps, "Comment <word>" CTA
- **@ash-teamapexx** (own reel, baseline) — two-angle talking head, yellow hero-word captions, glowing cut-out stickers

## Posting cadence & length defaults

- _Cadence_: _(TBD — set during /setup)_
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
