#!/usr/bin/env bash
# Deterministic demo render without VHS (ffmpeg slideshow from committed PNGs).
# Source of truth for assets/demo.mp4 + assets/demo.gif when `vhs` is unavailable.
set -euo pipefail
cd "$(dirname "$0")/.."
for f in volatility_pond gap_gross_vs_net gme_gap_equity dashboard; do
  ffmpeg -y -loglevel error -i assets/$f.png \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=#0b0b0f" \
    assets/slide_$f.png
done
ffmpeg -y -loglevel error \
  -loop 1 -t 3 -i assets/slide_volatility_pond.png \
  -loop 1 -t 3 -i assets/slide_gap_gross_vs_net.png \
  -loop 1 -t 3 -i assets/slide_gme_gap_equity.png \
  -loop 1 -t 4 -i assets/slide_dashboard.png \
  -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0,format=yuv420p" \
  -movflags +faststart assets/demo.mp4
ffmpeg -y -loglevel error -i assets/demo.mp4 \
  -vf "fps=8,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse" \
  assets/demo.gif
ls -lh assets/demo.mp4 assets/demo.gif
echo "OK: play with ffplay assets/demo.mp4 | GIF <2MB best practice ✔"
