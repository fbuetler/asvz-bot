# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.7] - 18.12.23

### Added

- Added `Rämibühl`, `Toni-Areal` and `CAB Move` to the available facilities (#33).
- Added SWITCH edu-ID login.
- Added a check to ensure the enrollment was actually successful and show the enrollment number.
- Added Docker & Docker compose support (By [masus04](https://github.com/masus04)).
- Added the option to use HTTP proxy (By [leopold-franz](https://github.com/leopold-franz)).
- Added the functionality to register to one-time events (By [leopold-franz](https://github.com/leopold-franz)).
- Added `Bad City`, `Bad Oerlikon` and `Bad Bungertwies` to the available facilities (By [leopold-franz](https://github.com/leopold-franz)).

### Fixed

- UZH switched from own login to SWITCH edu-ID login (#31)

## [1.4.6] - 12.10.23

### Changed

- Upgraded `selenium` from `4.8.2` to `4.14.0` and `webdriver-manager` from `3.8.5` to `4.0.1`.
- Corrected README setup command from [peschee](https://github.com/peschee)


## [1.4.5] - 01.05.23

### Changed

- If lessons on a holiday are searched, the next day is displayed by the ASVZ website. Changed to now check if the found lesson is actually on the day specified by the user arguments (By [BRB2000](https://github.com/BRB2000)).

## [1.4.4] - 17.04.23

### Changed

- Changed trainer argument to being optional as there are lessons like fitness, that do not have a trainer. In these cases, the first lesson in the list is taken (By [sant0s12](https://github.com/sant0s12)).

## [1.4.3] - 07.03.23

### Changed

- Enrollment time interval includes the time again (essentially revert the changes done in `1.4.2` with respect to the enrollment time detection).
- Upgrade `selenium` from `4.1.0` to `4.8.2` and `webdriver-manager` from `3.5.2` to `3.8.5`.

## [1.4.2] - 21.01.23

### Fixed

- Adapt bot to work with the newest ASVZ website. The enrollment time location has changed and some small components were updated (#15).

## [1.4.1] - 03.11.22

### Fixed

- Retry enrollment when a lessons is full, a place gets free and enrollment is tried but some else was faster (#13).

## [1.4.0] - 26.10.22

### Added

- Added PHZH login support (#12).

## [1.3.0] - 11.10.22

### Added

- Added CHANGELOG.md
- Added optional selection filter based on training level from [CyprienHoelzl](https://github.com/CyprienHoelzl)

## [1.2.1] - 27.09.22

### Changed

- Correct name of element on website from [mathinic](https://github.com/mathinic)

## [1.2.0] - 17.03.22

### Added

- Added ASVZ account support for alumni from [abrandemuehl](https://github.com/abrandemuehl)
- Added helpful feedback if a 404 page is hit

## [1.1.1] - 16.12.21

### Added

- Added `Rämistrasse 80` to the available facilities

### Changed

- Make script language independent (and fix UZH name issue) from [mathinic](https://github.com/mathinic)
- Changed deprecated `logging.warn` to `logging.warning`
- Updated various as deprecated marked code
- Only ask for password if it is not supplied already
- Decreased retry intervall on booked out lessons from 60 to 30 seconds
- Improved script stability and UX
- Updated requirements ([selenium](https://github.com/SeleniumHQ/selenium) to `4.1.0` and [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) to `3.5.2`)

### Removed

- Language code that is not accepted by SwitchAAI

## [1.1.0] - 18.06.21

### Added

- Set script encoding
- Password can be passed via CLI argument

## [1.0.0] - 05.06.21

### Added

- Added GPL-3.0 license
- Added credentials check on startup

### Changed

- Rewrote the whole logic
- Corrected README example commands from [lmeinen](https://github.com/lmeinen)

## [0.1.0] - 07.05.21

Initial version

[unreleased]: https://github.com/fbuetler/asvz-bot/compare/v1.4.7...master
[1.4.7]: https://github.com/fbuetler/asvz-bot/compare/v1.4.6...v1.4.7
[1.4.6]: https://github.com/fbuetler/asvz-bot/compare/v1.4.5...v1.4.6
[1.4.5]: https://github.com/fbuetler/asvz-bot/compare/v1.4.4...v1.4.5
[1.4.4]: https://github.com/fbuetler/asvz-bot/compare/v1.4.3...v1.4.4
[1.4.3]: https://github.com/fbuetler/asvz-bot/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/fbuetler/asvz-bot/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/fbuetler/asvz-bot/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/fbuetler/asvz-bot/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/fbuetler/asvz-bot/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/fbuetler/asvz-bot/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/fbuetler/asvz-bot/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/fbuetler/asvz-bot/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/fbuetler/asvz-bot/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/fbuetler/asvz-bot/compare/v0.1...v1.0.0
[0.1.0]: https://github.com/fbuetler/asvz-bot/releases/tag/v0.1
