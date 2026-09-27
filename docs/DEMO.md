# Demo — video + screenshots (best practice 2026)

> Show, don't tell: 13-second loop, <2MB, one complete value flow (mdkit 2026, banger-readme 2026).

## Watch

- `assets/demo.mp4` (99KB, 13s, 1280×720, faststart for GitHub streaming)
- `assets/demo.gif` (219KB, 960px, 8fps, 128 colors — under 2MB cap)
- `assets/dashboard.png` (Playwright full-page screenshot 1666×1419, taken 2026-09-27 via `playwright_browser_take_screenshot`)
- Charts: `assets/volatility_pond.png`, `assets/gap_gross_vs_net.png`, `assets/gme_gap_equity.png` (matplotlib, regenerated from live CSVs)

To re-render: `bash scripts/record_demo.sh`. For a scripted terminal cast: `vhs docs/demo.tape` (needs `ttyd`+`ffmpeg`).

## Publish video (for README hero on YouTube)

1. Upload `assets/demo.mp4` to YouTube as Unlisted → copy `VIDEO_ID`.
2. Replace `YOUR_VIDEO_ID` in README badges/hero with the ID.
3. Keep `demo.gif` inline (autoplay in README) + link GIF → YouTube for sound/full res:
   `[![Demo](assets/demo.gif)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)`
4. Verify mobile legibility (80×24 terminal, ≥14pt font rule) + loop cleanliness.

## Screenshot provenance

Dashboard served via `python3 -m http.server 8000`, navigated with Playwright MCP
(`playwright_browser_navigate` → snapshot table verified → `take_screenshot fullPage`),
saved to `assets/dashboard.png`. Re-capture: restart server, re-run the two MCP calls.

## Why this shape

- GIF = highest README conversion (~3×, mythos-agent DEMO-SCRIPT 2026); MP4 = streaming + YouTube source.
- `.tape` in git = reviewable, deterministic, CI-regenerable (charmbracelet/vhs-action).
- Slideshow fallback = zero-dependency reproducibility when VHS absent.
