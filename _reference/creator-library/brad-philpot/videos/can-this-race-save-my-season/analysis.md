# can-this-race-save-my-season — @brad-philpot

**Source:** https://youtu.be/Cy7FO-lo7Hc ("Can This Race SAVE My Karting Season?")
**Duration:** 1515.10s (25:15)
**Aspect:** 16:9
**Resolution:** 1280x720 (720p study copy), 60fps
**Studied:** 2026-11-10
**Engagement (at time of study):** 32,304 views, 702 likes, 106 comments (uploaded 2026-10-22)
**Sample rate:** first 60s at 1fps; after that 1 frame per 4s, contact sheets 3, 7, 11, 13 read (about 100 frames across the 25 min). Transcript: first 3 minutes (Whisper small.en).

## Hook (0–60s)
- 0–1s: old 2024 onboard (GoPro look), white caption "2024..." (flashback marker).
- 1–4s: the same shot with a results row building one at a time: "Heat 1 / Heat 2 / Heat 3 / Final" headers with yellow "P1" stamping under each. That's a quick proof of past form.
- 4–6s: selfie in the awning (beanie, team kit), talking.
- 6–8s: drone fly-over of Llandow circuit and paddock.
- 8–17s: selfie, then onboard snippets (rear-facing cam plus front-facing), fast cuts.
- 17–20s: drone top-down again.
- 20–25s: desaturated (black and white) trackside shot with a magenta "CHAMPIONSHIP POSITION" header, then yellow "P11", then "P11 +4 pts", building word by word. Stakes in numbers.
- 25–30s: full championship standings table (dark UI) then the same table flashes green with a big tick (the top-10 cut-off).
- 30–40s: trackside, then a rear-cam with "LAST TIME..." in yellow (flashback to the previous round) and an engine/parts cutaway (hands on the kart).
- Spoken hook (VO): "Two years ago, I won every single race I entered at this track. Today, I'm back at Llandow for the final round of GX-UK, and I could really do with some of that happening again. This season hasn't exactly gone to plan ... I'm currently 11th, just four points outside the top 10, and finishing inside that top 10 earns me a seeded number ... There's one round left. I'm four points behind. So let's see if we can rescue something from this season."
- Script pattern: past glory, then present problem, then exact numeric stakes, then what changed since last time, then "we're about to find out", then a one-line call to action ("let's see if we can rescue something").

## Pacing
- Hook cuts every 1–3s for the first 40s, then a long race block.
- Each heat block: drivers' briefing b-roll, then grid, then a 4–6 minute race onboard with only occasional cutaways (nose-cam, rear-cam, helmet-cam), then a short selfie debrief.
- Shortest / longest: about 1s (results stamps) / several minutes of onboard.
- Distribution feel: front-loaded, chopped intro, then sustained racing with angle changes every 5–15s.

## Captions
- Yellow outlined Bebas-style caps for stakes and section markers ("LAST TIME...", "P11 +4 pts", "THIS KART IS NOW FOR SALE!", "ASH CRASH").
- Magenta outlined caps for headers ("CHAMPIONSHIP POSITION").
- White subtitle lines (bold sans, soft shadow, bottom-centre) only for in-kart muttering or lines that would otherwise get lost ("We can't seem to stick with them at all.", "Little bit of a tow this time.", "Not a good strategy there, don't do that.", "right-hander").
- Membership plug in yellow outlined caps, two lines ("SEASON PLANNER FREE WITH £2.99 MEMBERSHIP!").

## Scene types
1. Flashback onboard with a results row stamping in (P1 P1 P1 P1).
2. Drone fly-over and top-down of the circuit.
3. Selfie to camera in the awning or paddock (wide lens, handheld mic, beanie).
4. Interview / chat with team or family (two-shot, he holds the mic out).
5. Drivers' briefing b-roll (crowd of drivers, official on steps).
6. Race intro panel: dark frosted card, "GX-UK · THE DRAGON CUP", huge "HEAT 1", "LLANDOW, WALES", weather icon with air/track temps, track outline drawn in pink with a start marker, "1.0 KM · 10 TURNS · CLOCKWISE".
7. **Animated track flyover**: dimmed onboard background; a neon track line draws section by section (green = current section, pink = previous, white = rest), camera "flies" along the map, ending on the full layout with "LLANDOW" under it. He narrates the lap over it.
8. Grid reveal: numbered tiles in pairs (position number in a white or pink box, name, kart number); rivals in the championship are highlighted in **pink**.
9. Start: red start-light dots graphic (three red circles) over the onboard.
10. Onboard with the full HUD (best/prev lap + delta, TIME LEFT or FINAL LAP, position, speed bubble, track-map icon, checkered flag on the last lap).
11. Nose-cam (camera on the front fairing looking forward, yellow nose in frame) with a soft yellow glow vignette around the frame edge.
12. Rear-facing cam (looking back at the driver), black-and-white treatment for a replay moment.
13. Big translucent position number ("9") over a trackside replay at the flag.
14. Final standings table: dark list, his row highlighted in a pink bar.
15. Membership / app plug: branded "USE. MORE. KERB. SEASON PLANNER" title card, phone UI screenshots, channel page screenshot.
16. Outro: selfie wrap-up, family/friends group selfie, "ASH CRASH" joke caption, end screen ("GO ON! SUBSCRIBE!" / "YOU'LL LOVE THESE TOO!").

## Transitions
- Mostly hard cuts; blur/zoom push into the race intro card; the track flyover is itself a transition between grid and start.
- Black-and-white freeze or desaturated shot to mark "replay" or "stakes" moments.
- Same motion-blur whips between locations as in the other video.

## Face treatment
- Fullscreen selfie, wide lens, arm's length. Face upper-third, always with the handheld mic. Beanie / cap with his brand.
- Natural grade, a bit warm and punchy on sunny days. No PiP, no Ken Burns.

## Audio reactivity
- Stamps and number builds land on SFX hits. Engine audio stays high under onboards; VO ducks it.

## Palette
- #FFE600 yellow (captions, P1 stamps)
- #E8318A magenta (headers, rival highlights, end screen)
- #39FF14 neon green (track flyover current section, ticks)
- #0E1116 near-black UI panels (race intro, standings)
- #FFFFFF (big position numbers, subtitles)

## Signature move
Turning club racing into a broadcast: race intro card with weather and track, an animated neon track flyover he narrates, rivals highlighted on the grid, and a live HUD on every onboard.

## What to steal (actionable for Hyperframes builds)
- **Results-row flashback stamp**: column headers then "P1" stamping one by one. Easy GSAP stagger.
- **Stakes in numbers**: "CHAMPIONSHIP POSITION" then "P11" then "+4 pts", building word by word over a desaturated shot.
- **Race intro card**: frosted dark panel with event, heat, location, weather and a track outline SVG. Very portable to Hyperframes (one comp, props per race).
- **Animated track map flyover**: SVG path of the circuit with stroke-dashoffset drawing section by section in green, completed sections fade to pink. Ash can trace his tracks (Silverstone, South Garda, Daytona MK) once and reuse them.
- **Grid tiles** with highlighted rivals.
- **Start lights** graphic over the grid.
- **Selective subtitles** only for in-kart lines.
- **Final standings table** with the driver's row in a highlight bar.
- **Nose-cam with an edge glow** as a third onboard angle.

## What's creator-specific (don't copy literally)
- "USE. MORE. KERB." brand, the season planner app/membership plug, the reporter mic, the purple/pink/green colourway, the "GO ON! SUBSCRIBE!" end screen.
- Championship-specific names (GX-UK, Dragon Cup).

## Transcript
`transcript-0-3min.txt` (first 3 minutes) and `transcript.json`.
