# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

## [0.1] - 07.05.21

Initial version

[unreleased]: https://github.com/fbuetler/asvz-bot/compare/v1.3.0...master
[1.3.0]: https://github.com/fbuetler/asvz-bot/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/fbuetler/asvz-bot/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/fbuetler/asvz-bot/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/fbuetler/asvz-bot/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/fbuetler/asvz-bot/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/fbuetler/asvz-bot/compare/v0.1...v1.0.0
[0.1]: https://github.com/fbuetler/asvz-bot/releases/tag/v0.1
