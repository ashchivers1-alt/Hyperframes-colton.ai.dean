# @brad-philpot — Style Fingerprint

Rolled up across 3 videos (all 16:9 long-form YouTube, 24–29 min). See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-11-10.

## Signature moves (consistent across videos)
- **Hook pattern (first 25–40s):** cold open on the most exciting footage, then scripted VO stating the stakes in plain numbers (old kart / 11th, 4 points behind / never driven one), then a modest or ridiculous goal that matches the title word for word, then "We're about to find out." Stakes always get a yellow stamp on screen ("MISSION A-FINAL", "P11 +4 pts", "70bhp").
- **Narration:** scripted voiceover recorded afterwards, laid over b-roll and onboards. Live selfie clips are for reactions and debriefs. In race footage he narrates as a commentator: what's happening, who's around him, what he's thinking.
- **Race-as-broadcast package** (every race):
  1. race intro card (dark frosted panel: event, heat number, location, weather/temps, track outline, "1.0 KM · 10 TURNS · CLOCKWISE")
  2. grid tiles (numbered, names, his row or rivals highlighted)
  3. red start-light dots
  4. onboard with a live HUD (best/prev lap + delta, TIME LEFT / FINAL LAP, P-position, mph, track icon, checkered flag on the last lap)
  5. giant white translucent position slam at the flag ("P2", "P12")
  6. selfie debrief
- **Captions:** no karaoke. Yellow outlined condensed caps for stamps / chapter cards ("FRIDAY PRACTICE", "WARM-UP", "SUNDAY", "LAST TIME..."). White bottom-centre subtitles only for in-kart or helmet-on lines and punchlines. Other people's lines in a different colour.
- **Camera angles in races:** steering-wheel cam (main), nose-cam, rear-facing cam at the driver, side-pod low cam, helmet cam, trackside telephoto pans, drone fly-over / top-down.
- **Transition rotation:** mostly hard cuts; motion-blur whip-pans between locations; black-and-white for flashbacks / replays.
- **Face treatment:** wide-angle handheld selfie with a reporter mic (signature prop) plus a tripod mid-shot for the scripted explainer. Natural grade, no PiP.
- **Palette:** #FFE600 yellow (stamps), #FFFFFF (subtitles, slams), #E8318A magenta, #39FF14 neon green, #0E1116 dark UI panels.
- **Energy profile:** front-loaded hook (cuts every 1–3s), then long sustained race blocks with angle changes every 5–15s, a breather selfie between sessions, and an outro with friends/family plus an end screen.

## What to steal (ranked by Hyperframes copy-ability)
1. **Onboard race HUD overlay**: position, lap, delta, time left, speed. One reusable Hyperframes comp fed by a JSON of lap times / positions per clip. Biggest single upgrade for Ash's onboard footage.
2. **Race intro card + track outline**: one comp per track (Silverstone, South Garda, Daytona MK, Rye House, etc.), with the session name and weather as props.
3. **Animated track-map flyover**: SVG path drawing section by section (green current, pink done) while the lap is narrated.
4. **Position slam at the flag**: huge white translucent "P1" for 0.6s with a whoosh.
5. **Yellow outlined stamp captions** for stakes, stats and chapter cards.
6. **Grid tiles with highlighted rivals**, **start-light dots**, **final standings table with the driver's row highlighted**.
7. **Selective white subtitles** for helmet-on and in-kart lines only.
8. **Hook script formula**: past result or handicap, then exact numeric stakes, then the title question, then "we're about to find out". Then cut straight into chapter 1.
9. **Label + arrow callouts** for people.

## Don't copy
- "USE. MORE. KERB." branding, the reporter-mic bit, his purple/pink/green colourway, "GO ON! SUBSCRIBE!" end screen, membership / season-planner upsell, his sponsor reads.
- Official TV broadcast footage and leaderboards (needs permission from the series broadcaster).
- His specific jokes (plane metaphor, "old enough to be their dad").

## Videos studied
- [a-final-in-a-10-year-old-kart](videos/a-final-in-a-10-year-old-kart/analysis.md): London Cup at Rye House in a 2017 kart; MISSION A-FINAL hook; TV leaderboard plus onboard HUD.
- [can-this-race-save-my-season](videos/can-this-race-save-my-season/analysis.md): GX-UK final round at Llandow; "P11 +4 pts" stakes; animated track flyover; rivals highlighted on the grid.
- [superkart-race-zero-practice](videos/superkart-race-zero-practice/analysis.md): 250cc superkart with no practice; stat stamps; P9 to P1 climb. The breakout video (165k views).
