# unicorn-binance-trailing-stop-loss Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

[How to upgrade to the latest version!](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/readme.html#installation-and-upgrade)

## 1.3.1.dev (development stage/unreleased/unstable)
### Fixed
- `BinanceTrailingStopLossManager.get_open_orders()` return type
  annotation was `Optional[dict]` while Binance's
  `GET /api/v3/openOrders`, `cancel_all_open_margin_orders` and
  `futures_get_open_orders` all return a `list`. The Cython-compiled
  module enforced the dict annotation and raised
  `TypeError: Expected dict, got list` on SPOT/Margin engine start
  whenever an open order existed for the symbol. Corrected the
  annotation and docstring to `Optional[list]`.
- `BinanceTrailingStopLossManager.process_price_feed_stream()` passed
  the raw aggTrade `price` (a `str` from the Binance payload) into
  `create_stop_loss_order(current_price=...)`, which is Cython-typed
  as `float` and raised
  `TypeError: Argument 'current_price' has incorrect type (expected float, got str)`.
  The price is now converted once via `float()` and the same float
  value is reused for `self.current_price`, the
  `calculate_stop_loss_price()` call and the
  `create_stop_loss_order()` call, keeping the instance attribute
  consistent with its `float` class annotation.
- `BinanceTrailingStopLossManager.create_stop_loss_order()` checked
  `if self.keep_threshold is not None:` but the CLI initialises
  `keep_threshold = ""`. When no `--keepthreshold` was given the
  empty string passed the not-None gate and `float("")` raised
  `ValueError`. Replaced with a truthy check, matching the existing
  `borrow_threshold` / `stop_loss_start_limit` handling.
- `self.stop_loss_quantity` was only assigned in the
  `keep_threshold` branch (via `update_stop_loss_quantity()`), so
  the engine's "Created stop/loss order" notification displayed the
  stale init value `0.0` whenever no keep_threshold was used. The
  instance attribute is now assigned after both branches with the
  rounded quantity that is actually sent to Binance, and the
  `calculate_stop_loss_amount()` path now also applies
  `round_decimals_down()` for parity with the `keep_threshold`
  path.
- `BinanceTrailingStopLossManager.update_stop_loss_asset_amount()`
  unpacked the `get_owning_amount()` result without checking for
  `None`, which happens whenever the configured asset has no
  balance / is not listed for the account (typical for
  `binance.com-isolated_margin` if the trading pair was never
  activated). This raised a bare
  `TypeError: 'NoneType' object is not iterable` deep inside the
  engine thread and left the streams running. The engine now
  fails loud with a clear message ("Asset `X` not found on
  `EXCHANGE` - no balance or asset not listed for this account.
  Stopping engine."), dispatches the email/Telegram/`callback_error`
  notifications, calls `stop_manager()` and exits, matching the
  existing fail-loud pattern used for `symbol_info is None`.

## 1.3.2
### Changed
- Bumped minimum `unicorn-binance-websocket-api` dependency from
  `>=2.12.2` to `>=2.13.0` in `setup.py`, `requirements.txt`,
  `pyproject.toml`, `environment.yml` and `meta.yaml`. UBWA 2.13.0
  introduces the per-category Futures WebSocket routing
  (`/public`, `/market`, `/private`) required by Binance since
  2026-04-23 and raises `ValueError` on mixed-category streams.
  See
  [unicorn-binance-websocket-api#437](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/437).

## 1.3.1
### Changed
- Bumped minimum `unicorn-binance-websocket-api` dependency from
  `>=2.1.1` to `>=2.12.2` in `setup.py`, `requirements.txt`,
  `pyproject.toml`, `environment.yml` and `meta.yaml`. 2.12.2 is the
  cleanup-round UBWA release; also adds support for features relied
  on since UBWA 2.12.
- Replaced all remaining `lucit.tech` URLs in source files, tests and
  config with their github.com / github.io equivalents:
  - Package headers (`manager.py`, `cli.py`, `__init__.py`,
    `unittest_binance_trailing_stop_loss.py`, `example_binance_trailing_stop_loss.py`,
    `dev/set_version.py`): project website, docs URL, changelog URL
    and setup.py/pyproject.toml project_urls.
  - `.github/ISSUE_TEMPLATE/config.yml`: documentation link.
  - `.github/FUNDING.yml`: `shop.lucit.services` → `github.com/sponsors/oliver-zehentleitner`.
  - `SECURITY.md`: replaced the lucit.tech contact form URL with the
    GitHub Security Advisories private-reporting URL.
  - `CODE_OF_CONDUCT.md`: replaced the lucit.tech contact form URL
    with the project maintainer's GitHub profile.
- README: switched all conda references from the legacy `lucit` channel
  to `conda-forge`. Added conda-forge version / downloads / feedstock
  build badges. Replaced the old multi-channel install block with a
  single `conda install -c conda-forge unicorn-binance-trailing-stop-loss`.
- README: reworded the PyPy paragraph to
  "PyPy wheels are available for all supported Python versions."
  The old wording made sense when we shipped wheels for pre-3.9 CPython.
  Also dropped the stale "Anaconda packages are available from Python
  version 3.9 and higher" line.
- Removed the "Build and Publish Anaconda" badge from the header and
  updated the "Packages are created automatically" section to reflect
  that conda packaging is handled by the conda-forge feedstock.
- Aligned dependency lists across `requirements.txt`, `setup.py`,
  `pyproject.toml`, `environment.yml` and `meta.yaml` using `setup.py`
  as the source of truth. Added explicit `>=2.2.0` / `>=2.1.1` pins
  on `unicorn-binance-rest-api` / `unicorn-binance-websocket-api` in
  `environment.yml` (they had no constraint).
- `environment.yml`: dropped the `lucit` and `defaults` channels;
  removed `lucit::` prefixes on suite deps.
- `meta.yaml`: removed the leftover `channels:` and `dependencies:`
  blocks (they are `environment.yml` keys, not valid in `meta.yaml`).
  Dropped the `lucit::` channel prefixes from suite deps. Re-embedded
  the current `README.md` into `about.description`.
### Fixed
- Added `MANIFEST.in` so the source tarball on PyPI actually ships the
  Python sources of the package. Previously only `setup.py` was included
  which made the sdist unbuildable (e.g. conda-forge builds from sdist).
### Removed
- `.github/workflows/build_conda.yml`: the conda-forge feedstock
  (`conda-forge/unicorn-binance-trailing-stop-loss-feedstock`) now
  builds and publishes the conda package; no in-repo build is needed.

## 1.3.0
### Added
- Readable error messages for invalid or missing config files (closes #20)
- Unit tests now run on all supported Python versions (3.9-3.14)
### Changed
- License changed back from LSOSL to MIT
- Author/copyright updated to Oliver Zehentleitner
- GitHub URLs migrated from `LUCIT-Systems-and-Development` to `oliver-zehentleitner`
- Minimum Python version raised from 3.7 to 3.9, added support up to 3.14
- CLI help output streamlined, removed LUCIT branding
- build_wheels.yml: Fixed artifact upload so Linux and Mac wheels are published to PyPI (not just Windows); added explicit `CIBW_BUILD` for Python 3.9-3.14; upgraded `cibuildwheel` to `v3.4.1`; updated runner OS to `ubuntu-24.04`/`windows-2025`/`macos-14`
- Unit tests switched to `binance.us` exchange for CI compatibility
### Removed
- LUCIT licensing dependency (`lucit-licensing-python`, `LucitLicensingManager`)
- `licensing_manager.py` and `licensing_exceptions.py`
- Gitter references (service is dead)
- LUCIT branding from README, meta.yaml, CLI, badges, and all source file headers

## 1.1.0
### Added
- `manager.is_manager_stopping()`
- Support for "binance.com"

## 1.0.0
### Added
- Additional info for a better user experience
- Support for Python 3.11 and 3.12
- Integration of the `lucit-licensing-python` library for verifying the UNICORN Binance Suite license. A license can be 
  purchased in the LUCIT Online Shop: https://shop.lucit.services/software/unicorn-binance-suite
- License change from MIT to LSOSL - LUCIT Synergetic Open Source License:
  https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/LICENSE
- Conversion to a C++ compiled Cython package with precompiled as well as PyPy and source code wheels.
- Setup of a "Trusted Publisher" deployment chain. The source code is transparently packaged into wheels directly from
  the GitHub repository by a GitHub action for all possible platforms and published directly as a new release on GitHub
  and PyPi. A second process from Conda-Forge then uploads it to Anaconda. Thus, the entire deployment process is
  transparent and the user can be sure that the compilation of a version fully corresponds to the source code.
- Support for `with`-context.

## 0.8.0
### Added
- Parameter `installupdate` (only available in Bot mode)
### Fixed
- Create logfile parent dir if not exists
- Handling exceptions while opening a non existing ini file
- Bug in test "streams"

## 0.7.1
### Fixed
- `self.test` not iterable as None type

## 0.7.0
### Added
- `engine` parameter to manager class and integrate `jump-in-and-trail` mode to `manager.py` 
- Parameter `stop_loss_start_limit`, `callback_partially_filled`, `ubra_manager` and `ubwa_manager` to `manager.py`
- Support for `binance.com`, `binance.com-testnet`, `binance.com-futures`, `binance.com-isolated_margin`, `binance.com-margin`   
- `listopenorders` and `cancelopenorders` to cli interface
- Test `streams`
### Changed
- `manager.py.calculate_stop_loss_price()` is a static method now
- Instead of creating two ubwa instances we use the new stream specific `process_stream_data` parameter within one instance
- `stoplossmarket` and `stop_loss_market` to `market`
### Renamed
- cli.py: `load_examples_ini_from_git_hub()` to `load_examples_ini_from_github()`

## 0.6.0
### Added
- Parameter `-- createconfigini` to cli interface
- Parameter `-- createprofilesini` to cli interface
- Parameter `-- openconfigini` to cli interface
- Parameter `-- openprofilesini` to cli interface 
- Parameter `-- example` to cli interface
- `cli.load_examples_ini_from_git_hub()`
### Changed
- ini files are no longer included into setup files of standalone versions
- Messages of test notification are now specific not general

## 0.5.0
### Added
- Warn on updates parameter
- `config` and `pandas` to dependencies
### Changed
- CLI help msg
- Config file path to {home}/.lucit/ubtsl_*.ini
### Fixed
- Ignore missing ubtsl_profile.ini if test is not None
- `Optional` bracket in `manager.get_exchange_info()`
- Using `\` as path separator in windows

## 0.4.2
### Fixed
- Module name for console_scripts in setup.py

## 0.4.1
### Fixed
- Installation via PIP on Windows

## 0.4.0
### Changed
- Many updates in the command line interface `ubtsl`

## 0.3.0
### Added
- Parameter `test` to lib and cli. Supported mode is "notification" to test email and telegram notifications.
- Parameter `print_notificatons`. If True the lib is printing user friendly information to terminal. 
- Count profit to CLI interface
- General output to CLI interface
### Changed
- Returning order details instead of text msg to callback_finished function
### Fixed
- Control notification settings to avoid exceptions

## 0.2.0
CLI update

## 0.1.2
General updates

## 0.1.1
General updates

## 0.1.0
Init
