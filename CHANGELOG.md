# ...

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
