# Fail loud on missing balance

## `update_stop_loss_asset_amount` fails loud instead of crashing silently deep in the engine thread

**Status:** active
**Confirmed** (commit `862a96b`, PR #63)

Found while reproducing a SPOT-exchange crash that didn't happen under `isolated_margin` — the same underlying bugs were present there too, just hidden. Root causes found and fixed together:
- UBRA's `get_open_orders` actually returns a `list`, but Cython's strict typing enforced `Optional[dict]`
- aggTrade price arrives as a `str`, crashing under Cython's strict float typing
- `keep_threshold=""` slipped past an `is not None` gate

The key behavioral fix: `update_stop_loss_asset_amount` now fails loud (fires `callback_error`/email/Telegram notifications, then `stop_manager()` and `sys.exit(1)`) instead of letting `total, free = None` unpack with a bare `TypeError` deep in the engine thread — which previously let the stream keep running silently after the crash.

**Rejected alternative (implicit — the bug being fixed):** letting the `TypeError` propagate unhandled. That's what was happening before; the fix isn't "catch and continue," it's "catch, notify loudly through every configured channel, then stop the engine" — same fail-loud pattern already used elsewhere in this file for `symbol_info is None` (see `manager.py` ~line 1097).

**Reason:** a silently-dead engine thread that still looks alive is worse than a crashed one that says so — the whole point of a trailing stop loss is that it's watching the market; a silent partial failure means it stops protecting a position without anyone knowing.
