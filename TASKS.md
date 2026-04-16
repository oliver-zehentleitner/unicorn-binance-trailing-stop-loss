# TASKS.md — UNICORN Binance Trailing Stop Loss

Open development tasks, ideas, and decisions.

---

## In Progress

*(none)*

---

## Backlog

### [ ] Audit and fix all silent except/pass blocks
- Every `except ...: pass` without logging is a blind error sink — bugs disappear silently
- For each occurrence: either add `logger.debug/warning/error(...)` with context, or justify why
  silence is correct (e.g. `del key` idiom, `asyncio.CancelledError` during shutdown)
- Suite-wide initiative — same task tracked in all unicorn-* repos

---

## Done

*(none)*
