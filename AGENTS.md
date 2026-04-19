# AGENTS.md — UNICORN Binance Trailing Stop Loss

> **End-user cheatsheet for AI-assisted consumption:** [`llms.txt`](llms.txt) — use that one if you're writing code *against* this library.
> **This file** is for AI agents working *on* this repo itself.

## Planning & Backlog

Open development tasks and decisions are tracked in **[TASKS.md](TASKS.md)**.

---

## Project Overview

Python SDK + CLI tool (MIT License) for running a trailing stop loss engine against Binance. Monitors a configured market via WebSocket, adjusts a stop-loss order on the exchange as the price moves in the favourable direction, and closes out automatically once triggered. Supports a separate `jump-in-and-trail` mode for smart entries.

**Current Version:** 1.3.1
**Python Compatibility:** 3.9 – 3.14
**Author:** Oliver Zehentleitner
**PyPI:** `unicorn-binance-trailing-stop-loss`
**CLI entry point:** `ubtsl`
**Abbreviation used in Suite:** UBTSL

---

## Directory Structure

```
unicorn_binance_trailing_stop_loss/     # Main package
    manager.py                          # Core class BinanceTrailingStopLossManager (~1277 lines)
    cli.py                              # Command line interface (~661 lines, entry point 'ubtsl')
    __init__.py                         # Package exports

unittest_binance_trailing_stop_loss.py  # Unit tests (main test file, run in CI)
example_binance_trailing_stop_loss.py   # Usage example
dev/                                    # Local dev scripts (set_version.py etc.) — NOT run in CI
docs/                                   # Pre-built HTML documentation (Sphinx)
```

---

## Supported Exchanges

Configured via the `exchange` constructor parameter:

| Exchange String | Notes |
|---|---|
| `binance.com` | Spot (default) |
| `binance.com-testnet` | Spot testnet |
| `binance.com-margin` | Cross Margin |
| `binance.com-isolated_margin` | Isolated Margin |
| `binance.com-futures` | USD-M Futures |

---

## Dependencies

Managed in `requirements.txt`, `setup.py`, `pyproject.toml`, `environment.yml` and `meta.yaml` — **all five must be kept in sync manually**, with `setup.py` as source of truth:

- `unicorn-binance-websocket-api>=2.12.2` — WebSocket stream management (UBWA)
- `unicorn-binance-rest-api>=2.2.0` — REST order placement (UBRA)
- `requests` — HTTP
- `Cython` — C extension compilation (release builds only)

---

## Running Tests

```bash
# Unit tests with coverage (this is what CI runs)
coverage run --source unicorn_binance_trailing_stop_loss unittest_binance_trailing_stop_loss.py

# Unit tests without coverage
python -m unittest unittest_binance_trailing_stop_loss.py
```

Tests connect to **binance.us** (live, unauthenticated public data) for CI compatibility. Scripts in `dev/` are local helpers — not run in CI.

---

## Build & Packaging

Development and testing use **plain Python** — no Cython compilation needed during development.

Cython compilation only for **release builds**:

```bash
python setup.py bdist_wheel
```

**Version bump** — done manually before each release via `dev/set_version.py`. The version string lives in three places that must stay in sync:
1. `setup.py` — `version=` in `setup()`
2. `pyproject.toml` — `version =`
3. `unicorn_binance_trailing_stop_loss/manager.py` — `__version__`

**CI/CD:** GitHub Actions in `.github/workflows/`
- `unit-tests.yml` — Python 3.9–3.14
- `build_wheels.yml` — Linux/macOS/Windows wheels + PyPI publish via trusted publisher
- `codeql-analysis.yml` — Security scanning

Conda packaging is handled by the [conda-forge feedstock](https://github.com/conda-forge/unicorn-binance-trailing-stop-loss-feedstock) — no in-repo conda build.

---

## Code Conventions

- **File header:** Full MIT license block with author/copyright (Oliver Zehentleitner)
- **Encoding:** UTF-8, UNIX line endings
- **Logging:** `logging.getLogger("unicorn_binance_trailing_stop_loss")`
- **Type hints:** Present throughout
- **Versioning:** Keep in sync across `setup.py`, `pyproject.toml`, `manager.py` manually

---

## Key Classes

| Class | File | Purpose |
|---|---|---|
| `BinanceTrailingStopLossManager` | `manager.py` | Main class, manages the trailing stop loss engine |

---

## Architecture

**High-level flow:**
1. Instantiate `BinanceTrailingStopLossManager(market=..., stop_loss_limit=...)` with credentials and parameters
2. Manager opens a WebSocket stream via UBWA for the market and (for `jump-in-and-trail`) waits for the entry condition
3. Once in position, a stop-loss order is placed via UBRA
4. WebSocket price updates trail the stop-loss order in the favourable direction (re-submission via UBRA)
5. On fill, `callback_finished` is invoked; on error `callback_error`; on partial fills `callback_partially_filled`

**Engine modes:**
- `engine="trail"` (default) — classic trailing stop loss on an existing position
- `engine="jump-in-and-trail"` — buys first (spot/margin/futures), then trails. Requires `borrow_threshold` for margin.

**Threading:** Engine runs in a background thread. Use `with` context manager or call `stop_manager()` to shut down cleanly.

**`stop_loss_limit`:** string parameter — `"2%"` (percent trail from reference price) or `"50"` (absolute price distance).

---

## Usage Patterns (Quick Reference)

```python
from unicorn_binance_trailing_stop_loss import BinanceTrailingStopLossManager

def on_error(msg):
    print(f"Error: {msg}")

def on_finished(msg):
    print(f"Finished: {msg}")

with BinanceTrailingStopLossManager(
    api_key="...",
    api_secret="...",
    exchange="binance.com",
    market="BTCUSDT",
    stop_loss_limit="2%",
    stop_loss_order_type="LIMIT",
    callback_error=on_error,
    callback_finished=on_finished,
    print_notifications=True,
) as ubtsl:
    while not ubtsl.is_manager_stopping():
        pass
```

**CLI**

```sh
# Create config
ubtsl --createconfigini
ubtsl --createprofilesini

# Run with profile
ubtsl --profile BTCUSDT_SELL --stoplosslimit 0.5%

# Test
ubtsl --test binance-connectivity
```

---

## Notes & Gotchas

- `stop_loss_order_type` **must** be set (`"LIMIT"` or `"MARKET"`) — otherwise the engine doesn't start
- Engine runs in a background thread — always use `with` context or a `while not is_manager_stopping()` loop
- For `jump-in-and-trail`, the `borrow_threshold` parameter is required on margin exchanges; missing it leads to silent non-entry
- `stop_loss_limit="2%"` vs. `"50"` semantics differ: percent is relative, bare number is an absolute price distance
- Partially filled orders are not handled automatically — use `callback_partially_filled` if reaction is needed
- CLI config files default to `~/.lucit/ubtsl_*.ini` (legacy path — not renamed)
