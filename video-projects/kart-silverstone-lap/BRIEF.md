# kart-silverstone-lap — BRIEF

- **Intent:** onboard lap of Kart Silverstone's new layout with a live track map showing where the kart is.
- **Source:** user's pre-edited reel (`assets/lap.mp4`, H.264 re-encode of the 720×1280 HEVC original, 88.8s). Not cut or re-timed.
- **Output:** 1080×1920, 30fps.
- **Overlay (rev 2):** track drawn as two white edge outlines only (no aerial photo), centred in the black band above the footage. Red snail trail fills the track between the outlines as the dot passes; dot = white core with red ring, pulse and glow. Fades out as the Instagram end card comes up (~84.4s).
- **Palette:** white outlines, red `#ff1a1a` trail/dot.
- **Sync method** (`scripts/`): skeletonised the white track to a centre line, measured camera yaw-rate per frame (phase correlation), aligned it to the map's curvature with DTW, then took corner apexes as anchors and spread the time between them with a corner-slower speed model. Direction: anticlockwise on the map (east along the bottom straight). Start/finish is on the bottom straight, and the lap completes at about 83.4s.
- **Audio:** original reel audio untouched; no SFX/music added.
