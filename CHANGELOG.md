# BAS Style Kit Jinja Templates - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

* Typo in back to top target include
  [#35](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth/-/issues/35)

## [0.7.0] - 2022-01-20 [BREAKING!]

### Changed [BREAKING!]

* Jinja2 3.x required (for compatibility with Flask 2.0)
  [#34](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth/-/issues/34)
* Relicensing project under the MIT licence (from the UK Open Government Licence)
  [#30](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth/-/issues/30)

### Added

* Flake8 linting
  [#33](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/-/issues/33)
* Updating dependencies (notably Jinja)
  [#34](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/-/issues/34)

### Changed

* Updating CI/CD configuration
  [#32](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/-/issues/32)
* Switching to `src/` directory layout for package
  [#31](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/-/issues/31)
* Using Poetry for local development environments
  [#29](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/-/issues/29)

## [0.6.0] - 2021-03-17

### Added

* Example of using a Jinja package loader for application templates
* Updated Python dependencies
* Updated to jQuery 3.6.0
* Updated to BAS Style Kit 0.6.1

## [0.5.0] - 2020-06-30

### Changed [BREAKING!]

* Config class changed from `bsk_templates` to `BSK_TEMPLATES` for compatibility with Flask

### Added

* Item type header component pattern
* ORCID component pattern
* Including contact information to all page patterns
* Missing 'problem with this service' and 'service unavailable' page pattern examples
* Missing Google Analytics feature test
* Updating to Style Kit 0.6.0-beta
* Updating to jQuery 3.5.1
* Updating to JSCookie 2.2.1
* Updating to Font Awesome 5.13
* Updating to Python 3.8

### Fixed

* Availability options in 'service unavailable' page pattern template
* Typo in experimental label name in development phase notice
* Typo in README example
* Google Analytics support
* Adding missing steps to release process (bumping version in setup.py)
* Fixing project dependencies to only depend on Jinja2 package, all others moved to developer dependencies

### Changed

* Feedback links set to open in a new tab/window
* Changing from Flake8 to Black for Pep8 conformance and code formatting
* Changing from Pip, Twine and SetupTools to Poetry for packaging and distribution

## [0.4.0] - 2019-04-26 [BREAKING!]

### Added

* 'Sign-in' page pattern
* 'Start' page pattern
* `bsk_footer_classes` config option for adding extra classes to standard page footer

### Fixed

* Corrected use of deprecated CDN locations
* Wrong change log heading

### Changed

* README tweaks
* Updating internal Flask app dependencies

## [0.3.0] - 2019-04-26 [BREAKING!]

### Changed [BREAKING!]

* 'title' property in navigation item objects changed to 'value'

### Added

* Navigation item objects now support arbitrary attribute/value key/values
* Automatic active navigation item support for absolute URL matches
* Manual active navigation item support for dynamic URL matches

### Fixed

* Correcting formatting of footer governance links
* Secondary navigation menu support

### Changed

* Improved documentation on including custom CSS files in a Flask application

## [0.2.0] - 2019-04-26

### Added

* Footer content block to allow custom footer content to be added

### Fixed

* Correcting usage instructions in README
* Navigation menu macro were called incorrectly
* Correcting the order Style Kit and custom styles and scripts are included to ensure custom resources take priority
* Pinning `urllib3` dependency to later version to mitigate https://app.snyk.io/vuln/SNYK-PYTHON-URLLIB3-174464

## [0.1.0] - 2019-04-10

### Added

* Initial version based on other themes/templates using version 0.5.0 of the Style Kit
