# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!--
GitHub MD Syntax:
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Highlighting:
https://docs.github.com/assets/cb-41128/mw-1440/images/help/writing/alerts-rendered.webp

> [!NOTE]
> Highlights information that users should take into account, even when skimming.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention due to potential risks.
-->

## [In Development] - Unreleased

<!--
Section Order:

### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security
-->

### Changed

- Templatetag code improved

## [2.3.0] - 2025-02-06

### Changed

- Use `django-sri` for Subresource Integrity hashes
- Minimum requirements
  - Alliance Auth >= 4.6.0
- Make ajax call URLs an internal URLs
- Set own user agent for dhooks-lite

## [2.2.2] - 2024-12-14

### Added

- Python 3.13 to the test matrix

### Changed

- Translations updated

## [2.2.1] - 2024-11-01

### Changed

- Italian translation improved
- Ukrainian translation improved

## [2.2.0] - 2024-09-16

### Changed

- Dependencies updated
  - `allianceauth`>=4.3.1
- Japanese translation improved
- Lingua codes updated to match Alliance Auth v4.3.1

## [2.1.0] - 2024-07-27

### Added

- Prepared Czech translation for when Alliance Auth supports it

### Changed

- Chinese translation improved
- French translation improved
- Japanese translation improved

### Removed

- Support for Python 3.8 and Python 3.9

## [2.0.2] - 2024-06-03

### Changed

- Chinese translations updated

## [2.0.1] - 2024-05-16

### Changed

- Translations updated

## [2.0.0] - 2024-03-16

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Fixed

- Grammar in some translatable strings

### Removed

- Compatibility to Alliance Auth v3

## [2.0.0-beta.1] - 2024-02-18

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0b1!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Fixed

- Grammar in some translatable strings

### Removed

- Compatibility to Alliance Auth v3

## [1.4.2] - 2023-09-26

> [!NOTE]
>
> **This is the last version compatible with Alliance Auth v3.**

### Fixed

- Capitalization of translatable strings

### Changed

- Translations improved and updated
- Test suite updated

## [1.4.1] - 2023-09-02

### Changed

- Korean translation improved

## [1.4.0] - 2023-08-29

### Added

- Korean translation

## [1.3.0] - 2023-08-15

### Added

- Spanish translation

## [1.2.4] - 2023-08-13

### Fixed

- Bootstrap CSS fix

### Changed

- Translations updated

## [1.2.3] - 2023-07-30

### Added

- Bootstrap CSS fix
- Footer to promote help with the app translation

### Changed

- Ukrainian translation improved

## [1.2.2] - 2023-07-16

### Added

- Hint for Discord Markdown formatting in announcement text field re-added, this
  time it is translatable

### Removed

- Pseudo plural from help texts in the models

## [1.2.1] - 2023-06-19

### Added

- Translations to Django Admin Backend

### Changed

- English grammar improved
- Translations improved

### Removed

- Non-translatable string from the announcement form

## [1.2.0] - 2023-04-24

### Changed

- Russian translation updated
- Moved the build process to PEP 621 / pyproject.toml

## [1.1.0] - 2023-04-16

### Added

- Russian translation

## [1.0.0] - 2023-04-13

### Added

- German translation

## [0.0.2] - 2022-09-18

### Added

- Hint text to the "Announcement Text" field with a link to Discord Markdown

### Removed

- Deprecated attributes from `style` and `script` tags

## [0.0.1] - 2022-08-08

### Added

- First public version
