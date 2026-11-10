# Karting video style (Ash's karting channel)

Combined from @brad-philpot and @cameron-das-racing (3 videos each, studied 2026-11-10). Use this for any of Ash's karting builds (kart-silverstone-lap, kart-spins-reel, south-garda-final-lap, daytona-mk-tnl, formula75-reveal and new ones). Say "build this like @brad-philpot" or "@cameron-das-racing" to lean one way; otherwise apply this blend.

Karting only. Keep it separate from the bodybuilding / Team Apexx style.

## What both creators do (the core)
1. **Hook in under 40s with the stakes in numbers.** Cold open on the best or most dramatic 2–4s. Then one line of prestige or scale. Then the handicaps stacked up ("old kart", "never driven one", "P11", "sick"). Then the goal, matching the title word for word. Then "we're about to find out" and straight into chapter 1.
2. **Every stake gets a stamp on screen.** "P11 +4 pts", "70bhp", "0-60 2.5s", "200 DRIVERS", "+0.100s EVERY LAP".
3. **Races look like TV.** Race intro card, then grid, then start lights, then onboard with a live HUD, then a position slam at the flag, then a debrief.
4. **A live HUD on every onboard.** Position, lap / time left, FINAL LAP, best lap and delta (Brad); face chip, session badge, battle table (Cameron).
5. **Many camera angles.** Steering-wheel cam, nose cam, rear-facing cam at the driver, side-pod low cam, trackside telephoto pans, drone / track map.
6. **Selective subtitles only.** Helmet-on, in-kart and shouted lines. No karaoke captions on 16:9 race videos.
7. **Scripted voiceover** for the story and the race narration; live selfie clips for reactions.
8. **Breakout formats** (about 5x views): a one-off challenge with a ridiculous or high-stakes goal (Brad's superkart with zero practice, 165k; Cameron's 24h endurance, 154k).

## House HUD for Ash (blend; build once as a Hyperframes overlay comp)
- Top-left: Ash's face chip + "ASH" name.
- Top-centre: session label / TIME LEFT / FINAL LAP bar; checkered-flag state.
- Top-right: big position number with a session label ("HEAT 2 · P6").
- Left: best / previous lap + delta (green faster, red slower). Only if Ash has lap data (AiM / Alfano export or manual timings).
- Bottom-left: mini battle table when racing someone (P5 / ASH / P7).
- Rival name tags pinned above karts for key battles.
- Frame glow colour: Ash's brand (check `assets/brand-tokens.css`). Don't use Cameron's teal or Brad's pink/green.

## Graphics kit to build (priority order)
1. Onboard HUD comp (above).
2. Race intro card: track name, session, weather / track temp, track outline SVG, "X KM · N TURNS".
3. Animated track-map flyover (SVG path drawn section by section) for lap narration. Trace each of Ash's tracks once.
4. Position slam at the flag (huge white translucent "P2", about 0.6s, whoosh).
5. Stamp captions (bold condensed caps with an outline) for stakes, stats, chapter cards ("QUALIFYING", "HEAT 1", "FINAL").
6. Grid tiles with Ash and rivals highlighted; start-light dots; final results table with Ash's row highlighted.
7. Goal card + goal tracker for lap-time challenge videos.
8. "COMING UP" / "REPLAY" tags; label + arrow callouts for people; lower-third name tags.
9. Depth-masked giant stat text behind Ash (reuse the Vision person-matte pipeline).

## Copyright / don't copy
- Never reuse broadcaster or official live-stream graphics or footage without permission.
- Don't copy either creator's brand names, colourways, catchphrases, sponsor reads or end screens.
- Music: follow the copyright memory. Check Content ID before using any track; venue PA music in footage gets flagged.
