# Open questions

Found during a retrospective pass (2026-07) — genuinely unknown, not resolved by code, commit history, or existing docs. Flagging rather than guessing (per Keep the Why rule 1).

## Uncapped retry loop on Binance error `-2010`

**Status:** unknown — needs maintainer input

`manager.py` (~lines 573-580), inside `create_stop_loss_order`: on Binance error code `-2010`, the code does `time.sleep(5)` and loops (`while order_is_placed is False`) with no retry cap — indefinite retry on a fixed 5-second interval. Other error codes `return False` immediately instead of retrying.

**Why this needs an answer:** if `-2010` ("insufficient balance" in Binance's error scheme, among other cases) can also fire for a *permanent* condition, not just a transient one, this retries forever rather than failing loud — which would be inconsistent with the fail-loud pattern documented in `fail-loud.md`. Unknown whether `-2010` is scoped narrowly enough here that infinite retry is actually safe, or whether this needs a cap.

## Why `jump-in-and-trail` is margin-only

**Status:** unknown — needs maintainer input

The `jump-in-and-trail` engine mode is described (README, `meta.yaml`) as "still experimental, only available for Isolated Margin." Commit history for it (`d1ef241`, `6b0942e`, `acb2c88`, etc.) has only terse subject lines ("jump-in-and-trail", "integration of smart entry") with no design rationale in the commit bodies.

**Why this needs an answer:** it's unclear whether spot/futures support for this mode was tried and rejected, is simply not built yet, or is scoped out for a reason specific to margin's borrow mechanics (`borrow_threshold` is required for margin — see `AGENTS.md`'s Architecture section). Worth asking directly rather than inferring from the absence of evidence.
