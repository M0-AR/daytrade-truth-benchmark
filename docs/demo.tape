# VHS demo tape — source of truth (reproducible, reviewable in PR)
# Install: scoop install vhs / brew install vhs / go install github.com/charmbracelet/vhs@latest
# Requires: ttyd + ffmpeg on PATH. Render: vhs docs/demo.tape
# Fallback (no VHS): bash scripts/record_demo.sh (ffmpeg slideshow, deterministic)

Output assets/demo.gif
Output assets/demo.mp4

Set Shell "bash"
Set FontSize 18
Set Width 1280
Set Height 720
Set Theme "Catppuccin Frappe"
Set Padding 20
Set WindowBar Colorful
Set CursorBlink false
Set TypingSpeed 75ms

Hide
Type "cd /home/md/src/daytrade-truth-benchmark && PYTHONPATH=src pytest -q 2>&1 | tail -n 3"
Enter
Sleep 2s
Type "clear"
Enter
Show

Type "# DayTrade Truth: live Yahoo gaps 2024-2026"
Enter
Sleep 1s
Type "PYTHONPATH=src python -m dtb.benchmark_real --out results/real_benchmark.json"
Enter
Sleep 4s
Type "# open results/dashboard.html for the full table"
Enter
Sleep 2s
