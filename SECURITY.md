# Security Policy

**Do not trade live on this code.** Research only. If you find a security issue (secret leak,
dependency CVE, data-integrity bug that could mislead a thesis):

- Report privately via GitHub Security Advisories (preferred) — do not open a public issue.
- Response target: acknowledge within 72h, fix or triage within 14 days.
- Please include: file + commit hash + reproduction (`pytest` / `docker compose` log).

We run `pip` pinned deps + Dependabot; please do not commit `.env`, keys, or broker tokens
(`.gitignore` blocks them, CI scans diffs).
