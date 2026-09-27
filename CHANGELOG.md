# Changelog (Keep a Changelog)

## [0.2.0] - 2026-09-27
### Added
- Live Yahoo data (8×686 bars) + `benchmark_real.py` with 5 cost arms; `results/real_benchmark.json` hash `900e12da`
- SSR/LULD/IML halt gate in `guardrails.py`; `tests/test_real.py`
- `results/dashboard.html` + Playwright screenshot `assets/dashboard.png`
- `assets/demo.mp4`/`demo.gif` + `docs/demo.tape` + `scripts/record_demo.sh`; `docs/DEMO.md`
- MIT repo hygiene: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, CITATION, CI, templates
### Fixed
- `datetime.utcnow()` → timezone-aware; Dockerfile pip retries + `data/` baked in; Stooq-wall documented

## [0.1.0] - 2026-09-27
- Synthetic Monte-Carlo + scanner + 20 guardrails + 6 docs + audited searches.
