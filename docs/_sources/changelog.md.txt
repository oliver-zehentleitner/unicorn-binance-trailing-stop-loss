# unicorn-binance-trailing-stop-loss Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

[How to upgrade to the latest version!](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/readme.html#installation-and-upgrade)

## 1.1.0.dev (development stage/unreleased/unstable)

## 1.1.0
### Added
- `manager.is_manager_stopping()`
- Support for "binance.com"

## 1.0.0
### Added
- Additional infos for a better user experience
- Support for Python 3.11 and 3.12
- Integration of the `lucit-licensing-python` library for verifying the UNICORN Binance Suite license. A license can be 
  purchased in the LUCIT Online Shop: https://shop.lucit.services/software/unicorn-binance-suite
- License change from MIT to LSOSL - LUCIT Synergetic Open Source License:
  https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/LICENSE
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
