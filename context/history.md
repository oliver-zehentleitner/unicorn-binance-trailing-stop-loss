# History

## LUCIT-Systems-and-Development origin, including a dropped commercial license

**Type:** decision
**Status:** superseded — repo now lives under `oliver-zehentleitner`, MIT-licensed
**Evidence:** confirmed
**Source:** commit `4c14327` "Merge branch 'LUCIT-Systems-and-Development:master' into master"; commit `2d56481`

This repo once had a proprietary licensing layer: `license='LSOSL - LUCIT Synergetic Open Source License'`, with `lucit-licensing-python` as a dependency and dedicated `licensing_manager.py`/`licensing_exceptions.py`/`LucitLicensingManager` code. Commit `2d56481` ("Remove LUCIT branding, switch to MIT license, update Python support") removed the license code entirely, not just the branding — switched to plain MIT.

**Reason:** LUCIT is no longer part of how this project is licensed, distributed, or supported. Unlike a pure rebrand, this one actually removed functioning licensing-check code from the package.

## CI fixes from the same cleanup

**Type:** workaround
**Status:** active
**Evidence:** confirmed
**Source:** commits `5ef6695`, `b183472`, `759ffd3`

- CI initializes against `binance.us`, not `binance.com` — GitHub Actions runners are US-based and Binance blocks `binance.com` access from restricted (US) locations. Same reasoning as UBRA's and UBWA's unit tests.
- `build_wheels.yml` previously only got Windows wheels to PyPI — `actions/upload-artifact@v4` stopped merging same-named artifacts across OSes silently, so Linux/Mac wheel uploads were overwritten instead of coexisting. Fixed with per-OS artifact names.
- conda distribution switched to conda-forge; the in-repo `build_conda.yml` workflow was removed (this is why current `AGENTS.md` already only lists three workflows and explicitly notes "no in-repo conda build" — that part of `AGENTS.md` was already accurate, not stale).

## Stale doc found and fixed while writing this: CLI config path

**Type:** decision
**Status:** superseded — fixed in this pass
**Evidence:** confirmed
**Source:** commits `48f4450`, `0cb7324`; verified in `cli.py:47-49`

`AGENTS.md`'s "Notes & Gotchas" claimed CLI config files default to `~/.lucit/ubtsl_*.ini` ("legacy path — not renamed"). That's inaccurate: the config path was migrated to `~/.unicorn-binance-suite/config/` (commit `48f4450`), and the `.lucit` fallback path was deleted outright afterward (commit `0cb7324`, "Remove legacy .lucit path fallback — clean break") — there is no `.lucit` reference left in `cli.py`. Fixed in `AGENTS.md` alongside this history entry.
