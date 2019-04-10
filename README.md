# BAS Style Kit Jinja Templates

A set of [Jinja2](http://jinja.pocoo.org) templates implementing the [BAS Style Kit](https://style-kit.web.bas.ac.uk).

## Installation

### Pip package

The recommended way to get these templates is installing its PyPi package, `bas-style-kit-jekyll-templates`.

## Usage

### Quickstart

For a typical Flask application add this wherever your Flask application is defined:

```python
from flask import Flask, render_template
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader

from bas_style_kit_jinja_templates import BskTemplates

app = Flask(__name__)
app.jinja_loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas_style_kit_jinja_templates'),
})
app.config['bsk_templates'] = BskTemplates()

# Required/recommended settings
app.config['bsk_templates'].site_title = 'Example service'
app.config['bsk_templates'].site_description = 'Service to act as an example'
app.config['bsk_templates'].bsk_site_nav_brand_text = 'Example service'
app.config['bsk_templates'].bsk_site_development_phase = 'beta'
app.config['bsk_templates'].bsk_site_feedback_href = '/feedback'
app.config['bsk_templates'].bsk_site_footer_policies_cookies_href = '/legal/cookies'
app.config['bsk_templates'].bsk_site_footer_policies_copyright_href = '/legal/copyright'
app.config['bsk_templates'].bsk_site_footer_policies_privacy_href = '/legal/privacy'

# Optional - add a custom CSS file with a relative URL
app.config['bsk_templates'].site_styles.append({'href': '/css/app.css'})
# Optional - add a custom JS file with a SRI value
app.config['bsk_templates'].site_scripts.push({'href': 'https://example.com/js/example.js', 'integrity': 'abc123'})
# Optional - enable Google Analytics
app.config['bsk_templates'].site_analytics['id'] = '1234'
# Optional - choose between the `bsk-container` (used by default) and `bsk-container-fluid` layout container
app.config['bsk_templates'].bsk_container_classes = ['bsk-container']
# Optional - add navigation menu items
app.config['bsk_templates'].bsk_site_nav_primary.push({'title': 'Item', 'href': '#'})
app.config['bsk_templates'].bsk_site_nav_secondary.push({
    'title': 'Dropdown', 
    'items': [
        {'title': 'Sub-item 1', 'href': '#'}
    ]
})
app.config['bsk_templates'].bsk_site_nav_launcher.push({'title': 'Related service', 'href': 'https://example.com'})


@app.route('/')
def index():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/index.j2")
```

Where `app/index.j2` is a template located in `templates/index.j2` which extends an application layout:

```jinja2
{% extends 'app/layouts/app.j2' %}
{% block main_content %}
<p>Index view content...</p>
{% endblock %}
```

Where `app/layouts/app.j2` is a template located in `templates/layouts/app.j2` which extends a layout provided by these
templates:

```jinja2
{% exnteds 'bas_style_kit/layouts/bsk_standard.j2' %}
```

### Using a page pattern

To create a page in an application based on a [page pattern](#page-patterns), such as the 
[page not found](https://style-kit.web.bas.ac.uk/patterns/page-not-found/) pattern, create a template (e.g. 
`templates/errors/404.j2`) with the following:

```jinja2
{% extends 'bas_style_kit/patterns/bsk_page-not-found.j2' %}
```

To use this template as the 404 error handler in a Flask application:

```python
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('app/errors/404.j2'), 404

```

### Using custom CSS/JS

Non-Style Kit CSS an/or JavaScript resources can be included either as references to files, or as inline content.

**Note:** This won't work if you are using the [Blank layout](#layouts).

* CSS resources are outputted in the [styles block](#blocks), at the end of the `<head>` element
* JS resources are outputted in the [scripts block](#blocks), at the end of the `<body>` element

#### Using custom CSS/JS files

* CSS files are added as a resource object to the `site_styles` property of the `BskTemplates` class instance
* JS files are added as a resource object to the `site_scripts` property of the `BskTemplates` class instance

Files will be included after the Style Kit's own resources (where a Style Kit layout is used) to ensure they have 
priority.

Each file reference consists of an object with these properties:

| Property    | Data Type | Required | Allowed Values | Example Value                                         |
| ----------- | --------- | -------- | -------------- | ----------------------------------------------------- |
| `href`      | String    | Yes      | Any URL        | */css/app.css* / *https://example.com/js/app.js*      |
| `integrity` | String    | No       | Any SRI value  | *sha256-ClILH8AIH4CkAybtlKhzqqQUYR4eSDiNTK5LIWfF4qQ=* |

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].site_styles.append({'href': '/css/app.css'})
```

The `integrity` property is used to specify a 
[Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) value for 
a resource. If specified an `integrity` attribute and will be added to the generated markup. A `crossorigin` 
attribute will also be added for 
[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) support with a 
hard-coded, anonymous, value.

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].site_styles.append({'href': 'assets/css/app.css', 'integrity': 'sha256-abc123='})
```

#### Using custom CSS/JS inline content

* CSS content should be appended to the [styles block](#blocks)
* JS content should be appended to the [scripts block](#blocks)
* inline content will be added after any files to ensure they have priority

**Note:** To append to a block use `{{ super() }}`, rather than replacing the contents of a block.
 
For example (using a Jinja template):

```jinja2
{% block scripts %}
    {{ super() }}
    console.log('jQuery version: ' + jQuery.fn.jquery);
{% endblock %}
```

### Navigation menu items

When using the [bsk_standard layout](#layouts), a [navbar](https://style-kit.web.bas.ac.uk/components/navbar/) is 
included as part of the 'standard header', which consists of a cookie banner, navbar and site development phase banner.

This navbar consists of three menus (and other elements, documented elsewhere):

* a primary navigation menu - aligned left, after [brand elements](#navbar-branding)
* a secondary navigation menu - aligned right, before the launcher menu
* a navigation launcher menu - aligned right, after the secondary navigation menu

The navigation launcher is a restricted menu, used to link to other BAS websites and applications. By default it 
contains links to the [BAS public website](https://www.bas.ac.uk) and the [BAS data catalogue](https://data.bas.ac.uk). 
Other websites and applications can be added as well where relevant.

* primary navigation menu items should be added to the `BskTemplates.bsk_site_nav_primary` variable
* secondary navigation menu items should be added to the `BskTemplates.bsk_site_nav_secondary` variable
* navigation launcher menu items should be added to the `BskTemplates.bsk_site_nav_launcher` variable

The primary and secondary navigation menu's support:

* [navbar items](https://style-kit.web.bas.ac.uk/components/navbar/#item)
* [navbar drop-down menus](https://style-kit.web.bas.ac.uk/components/navbar/#drop-down-menus)
* [navbar drop-down menu items](https://style-kit.web.bas.ac.uk/components/navbar/#drop-down-menus)

The navigation launcher menu, which is implemented as a drop-down menu, supports:

* [navbar drop-down menu items](https://style-kit.web.bas.ac.uk/components/navbar/#drop-down-menus)

Menu item objects have the following properties:

| Property    | Data Type | Required | Allowed Values             | Example Value                              | Notes                                 |
| ----------- | --------- | -------- | -------------------------- | ------------------------------------------ | ------------------------------------- |
| `title`     | String    | Yes      | Any string                 | *About*                                    | -                                     |
| `href`      | String    | Yes      | Any URL                    | */about* / *https://www.example.com/about* | Ignored if `items` set                |
| `items`     | Array     | No       | Array of menu item objects | *-*                                        | Ignored for navigation launcher items |

**Note:** The `items` property is only recursed once, deeper objects will be ignored.

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_nav_primary.push({'title': 'Item', 'href': '/about'})
```

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_nav_secondary.push({
    'title': 'Dropdown', 
    'items': [
        {'title': 'Sub-item 1', 'href': 'https://www.example.com'}
    ]
})
```

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_nav_launcher.push({'title': 'Related service', 'href': 'https://example.com'})
```

**Note:** These templates do not support highlighting active navigation items. You will need to add the .bsk-active
class to the currently active menu item, and if relevant, sub-item, manually.

#### Navbar branding

Navbars are used to display the name/identity of a website or application, to remind users where they are. These 
elements are referred to as 'brand' elements within the Style Kit.

Supported brand elements:

* [brand text](https://style-kit.web.bas.ac.uk/components/navbar/#brand-text) - set using the 
`BskTemplates.bsk_site_nav_brand_text` property
* [brand image](https://style-kit.web.bas.ac.uk/components/navbar/#brand-image) - set using the 
`BskTemplates.bsk_site_nav_brand_img_href` property

Brand elements can be used together or individually, with fix classes applied automatically as needed.

Brand elements are linked to a location specified by the `bsk_attributes.site_nav_brand_href` variable, which should be,
and is by default, the index of each website or application (i.e. `/`).

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_nav_brand_text = 'Example service'
```

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_nav_brand_img_href = '/assets/img/navbar-brand-img.png'
```

### Site development phase

The site development phase indicates the stage of development for a website or application, e.g. alpha or live.
Conventional phases are described in the 
[Style Kit documentation](https://style-kit.web.bas.ac.uk/core/colours/#development-phase-colours).

For websites or applications that are not firmly in the 'live' phase, a banner should be shown to inform users and 
request feedback. This forms part of the 'standard header' of cookie banner, navbar and site development phase banner.

In these templates, the `BskTemplates.bsk_site_development_phase` property is used to specify the current phase for a
website or application. When using the [bsk_standard layout](#layouts) the banner will be shown automatically.

To disable this banner, use the `live-stable`. Strictly speaking this isn't a real phase but is recommended by these 
templates to distinguish between a newly released or mature and well-established website or application.

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_development_phase = 'beta'
```

#### Experimental site phase

Where a website or application is in a staging environment, or otherwise used for development/testing activities, the 
site phase can be set to `experimental` to use the conventional 
[experimental phase](https://style-kit.web.bas.ac.uk/core/colours/#variants).

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_development_phase = 'experimental'
```

### Google analytics

To include the Google Analytics universal tracking library (gtag), set the `BskTemplates.bsk_site_analytics['id']` 
property to relevant Google Analytics property ID.

**Note:** When used the anonymise IP option in Google Analytics is enabled by default.

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].bsk_site_analytics['id'] = 'UA-12345678'
```

## Components

All components are located in the `bas_style_kit_jinja_templates` package. Variables are 
defined in `bas_style_kit_jinja_templates/__init__.py`, with all other components defined in 
`bas_style_kit_jinja_templates//templates/`.

Components that are specific to the Style Kit are prefixed with `bsk--` or `bsk_`.

### Jinja setup

These templates requiring a *PrefixLoader* and *PackageLoader* 
[Jinja loader](http://jinja.pocoo.org/docs/2.10/api/#loaders).

```python
loader = PrefixLoader({
    'bas_style_kit': PackageLoader('bas-style-kit-jekyll-templates')
})
```

Typically your application with have its own templates as well, which can be loaded under a different prefix (such as 
`app`) using a relevant loader, such as the default *FileSystemloader*.

```python
loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas-style-kit-jekyll-templates')
})
```

In addition, a `BskTemplates` class instance is needed to define [Variable](#variables) values. This instance should be
available in the Jinja environment as `config.bsk_templates`. For Flask applications this will occur automatically by
adding the class instance to `app.config`, otherwise this instance will need to be passed manually.

For example (using a Flask application):

```python
app.config['bsk_templates'] = BskTemplates()
```

Where a *PrefixeLoader* is used, references to resources should include a prefix and a deliminator (`/` by default).
 
For example an application layout would change from:

```jinja2
{% extends "layouts/base.j2" %}
```

To:

```jinja2
{% extends "app/layouts/base.j2" %}
```

To use a layout from these templates:

```jinja2
{% extends "bas_style_kit/layouts/bsk_base.j2" %}
```

### Layouts

Layouts are 'base' templates from which views or other layouts inherit. Layouts in these templates are hierarchical,
with each layout extending the last in this order:

1. `blank.j2`: lowest level layout, intentionally as minimal as possible and not intended for direct use, unless 
    non-HTML output is needed
2. `html.j2`: defines a minimal, accessible, HTML5 structure with some recommended best practices for cross-platform 
    compatibility
3. `bsk_base.j2`: intentionally implements the BAS Style Kit as minimally as possible and not intended for direct use,
    unless the `bsk_standard.j2` layout is unsuitable
4. `bsk_standard.j2`: defines an opinionated, conventional, page layout with a 'standard' header/footer, recommended as
    a base for application/website layouts

Layouts can be used using the `extend` keyword and defining content in the relevant block:

| Layout            | Content Block  |
| ----------------- | -------------- |
| `blank.j2`        | `content`      |
| `html.j2`         | `main_content` |
| `bsk_base.j2`     | `main_content` |
| `bsk_standard.j2` | `main_content` |

For example:

```jinja2
{% exnteds 'bas_style_kit/layouts/bsk_standard.j2' %}

{% block main_content %}
Layout content
{% endblock %}
```

### Blocks

[Blocks](http://jinja.pocoo.org/docs/2.10/templates/#template-inheritance) are used for template inheritance and provide 
a logical structure/hierarchy.

Blocks are defined in [Layouts](#layouts), typically with default content using [Includes](#includes). Some blocks are 
empty, designed for user content or extensibility.

To implement or override a block, redefine it in a template or view:

```jinja2
{% block example_block %}
content ...
{% endblock %}
```

To append to a block, without overriding its existing content, use the special `{{ super() }}` variable:

```jinja2
{% block example_block %}
{{ super() }}
content ...
{% endblock %}
```

### Includes

[Includes](http://jinja.pocoo.org/docs/2.10/templates/#include) are used for organising content, to make management 
easier, and to allow common elements to be used in multiple places, typically in [Blocks](#blocks).

For example the content needed for [using Google Analytics](#google-analytics) is encapsulated in the 
`body--analytics-script.j2` include.

### Macros

[Macros](http://jinja.pocoo.org/docs/2.10/templates/#macros) are used to provide configurable, reusable, functionality.

For example, primary and secondary [navigation menus](#navigation-menu-items) process navigation items the same way, 
using the `bsk--nav.j2` macro.

### Variables

Various elements in these templates are configurable, such as the name of the application or website, or the CSS/JS 
resources to include. A Python class `BskTemplates` is used to configure these elements and which should be passed to 
the [Jinja environment](#jinja-setup).

These variables should be changed or set for each website or application:

`site_title`
: Name of the application or website

`site_description`
: Description of the application or website

`site_analytics.id`
: Google Analytics property ID

`bsk_site_nav_brand_text`
: Name of the application or website

`bsk_site_nav_primary`
: [Primary navigation menu items](#navigation-menu-items)

`bsk_site_development_phase`
: [Site development phase](#site-development-phase)

`bsk_site_feedback_href`
: URL or `mailto:` value for application or website feedback

`bsk_site_footer_policies_cookies_href`
: URL to application or website cookies policy

`bsk_site_footer_policies_copyright_href`
: URL to application or website copyright notice

`bsk_site_footer_policies_privacy_href`
: URL to application or website privacy policy

These variables may, but don't need to be, changed or set for each website or application:

`site_styles`
: Array of additional CSS files

`site_scripts`
: Array of additional JS files

`container_classes`
: Array of non-Style Kit classes which set the layout of content, including main content and headers/footers which 
  should align the same way

`main_content_classes`
: Array of non-Style Kit classes which should only be applied to main page content

`bsk_container_classes`
: Array of Style Kit classes which should set the layout of content, including main content and headers/footers which 
  should align the same way

`bsk_main_content_classes`
: Array of Style Kit classes which should only be applied to main page content

`bsk_site_favicon`
: Name of the [Favicon](https://style-kit.web.bas.ac.uk/core/favicon) to include (valid options: [`default`])

`bsk_site_nav_secondary`
: [Secondary navigation menu items](#navigation-menu-items)

`bsk_site_nav_brand_img_href`
: URL to [Navbar brand image](#navbar-branding)

`bsk_site_nav_brand_href`
: URL for [Navbar brand elements](#navbar-branding), which should be the index or home of the application or website

`bsk_site_nav_launcher`
: [Navigation launcher items](#navigation-menu-items)

These variables do not normally, and should not, need to be changed or set:

`site_back_to_top_target_id`
: ID of the anchor element representing the top of the current page/view

`site_main_content_target_id`
: ID of the element representing the main content in a page/view (i.e. skipping navigation elements)

`bsk_site_footer_ogl_symbol_a_href`
: URL to the Open Government Licence symbol

`bsk_site_footer_ogl_text_href`
: URL to the Open Government Licence text (i.e. the actual licence)

`bsk_site_footer_ogl_text_version`
: Version of the Open Government Licence used

These variables must not be changed and should be treated as read only:

`templates_version`
: Version of these templates

`bsk_version`
: Version of the Style Kit used by these templates

### Patterns

[Patterns](https://style-kit.web.bas.ac.uk/patterns/) demonstrate preferred ways to ask information from, or 
provide information to, end users for various tasks. 

#### Page patterns

Page patterns define content for common pages such as [*Page not found* (404) pages](#using-a-page-pattern).

These templates implement page patterns as layouts/views, typically without the need to provide additional information.
Where additional information is available, such as contact instructions or details about current maintenance etc., the
`pattern_content` block can be used.

For example:

```jinja2
{% extends 'bas_style_kit/patterns/bsk_service-unavailable.j2' %}

{% block pattern_content %}
Additional information clarifying details or circumstances.
{% endblock %}
```

Some patterns support multiple variants, or can be configured, using variables described in the sub-sections below.

##### Service unavailable

`availability`
: Set to `replaced` for the [replaced](https://style-kit.web.bas.ac.uk/patterns/service-unavailable/#replaced) variant.
  Set to `closed` for the [closed](https://style-kit.web.bas.ac.uk/patterns/service-unavailable/#closed) variant.

For example:

(basic variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_service-unavailable.j2' %}

{% block pattern_content %}
Contact the <a href="mailto:servicedesk.bas.ac.uk">BAS IT Service Desk</a> for more information.
{% endblock %}
```

(closed variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_service-unavailable.j2' %}

{% set availability = 'closed' %}

{% block pattern_content %}
Contact the <a href="mailto:servicedesk.bas.ac.uk">BAS IT Service Desk</a> for more information.
{% endblock %}
```

## Development

A docker container ran through Docker Compose is used as a development environment for this project. It includes 
development only dependencies listed in `requirements.txt` and a local Flask application in `app.py`.

Ensure classes and methods are defined within the `bas_style_kit_jinja_templates` package.

If you have access to the BAS GitLab instance, you pull the Docker image from the BAS Docker Registry:

```shell
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull

# To run the local Flask application using the Flask development server
$ docker-compose up

# To start a shell
$ docker-compose run app ash
```

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Flake8](http://flake8.pycqa.org/) is used to ensure compliance, and is ran on each commit through 
[Continuous Integration](#continuous-integration). 

To check compliance locally:

```shell
$ docker-compose run app flake8 . --ignore=E501
```

### Dependencies

Development Python dependencies should be declared in `requirements.txt` to be included in the development environment.

Runtime Python dependencies should be declared in `requirements.txt` and `setup.py` to also be installed as dependencies 
of this package in other applications.

All dependencies should be periodically reviewed and update as new versions are released.

```shell
$ docker-compose run app ash
$ pip install [dependency]==
# this will display a list of available versions, add the latest to `requirements.txt` and or `setup.py`
$ exit
$ docker-compose down
$ docker-compose build
```

If you have access to the BAS GitLab instance, push the Docker image to the BAS Docker Registry:

```shell
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose push
```

#### Dependency vulnerability scanning

To ensure the security of this API, all dependencies are checked against 
[Snyk](https://app.snyk.io/org/antarctica/project/2c147086-c928-4f0b-9639-2b865db91a60) for vulnerabilities.

**Warning:** Snyk relies on known vulnerabilities and can't check for issues that are not in it's database. 
As with all security tools, Snyk is an aid for spotting common mistakes, not a guarantee of secure code.

Some vulnerabilities have been ignored in this project, see `.snyk` for definitions and the 
[Dependency exceptions](#dependency-vulnerability-exceptions) section for more information.

Through [Continuous Integration](#continuous-integration), on each commit current dependencies are tested and a 
snapshot uploaded to Snyk. This snapshot is then monitored for vulnerabilities.

#### Dependency vulnerability exceptions

This project contains known vulnerabilities that have been ignored for a specific reason.

* [Py-Yaml `yaml.load()` function allows Arbitrary Code Execution](https://snyk.io/vuln/SNYK-PYTHON-PYYAML-42159)
    * currently no known or planned resolution
    * indirect dependency, required through the `bandit` package
    * severity is rated *high*
    * risk judged to be *low* as we don't use the Yaml module in this application
    * ignored for 1 year for re-review

#### Static security scanning

To ensure the security of this API, source code is checked against Bandit for issues such as not sanitising user inputs 
or using weak cryptography.

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the 
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

To check locally:

```shell
$ docker-compose run app bandit -r .
```

## Testing

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

Pip dependencies are also [checked and monitored for vulnerabilities](#dependency-vulnerability-scanning).

## Distribution

Both source and binary versions of the package are build using [SetupTools](https://setuptools.readthedocs.io/), which 
can then be published to the [Python package index](https://pypi.org/project/bas-style-kit-jinja-templates/) for use in 
other applications. Package settings are defined in `setup.py`.

This project is built and published to PyPi automatically through [Continuous Deployment](#continuous-deployment).

To build the source and binary artefacts for this project manually:

```shell
$ docker-compose run app ash
# build package to /build, /dist and /bas_style_kit_jinja_templates.egg-info
$ python setup.py sdist bdist_wheel
$ exit
$ docker-compose down
```

To publish built artefacts for this project manually to [PyPi testing](https://test.pypi.org/):

```shell
$ docker-compose run app ash
$ python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# project then available at: https://test.pypi.org/project/bas-style-kit-jinja-templates/
$ exit
$ docker-compose down
```

To publish manually to [PyPi](https://pypi.org/):

```shell
$ docker-compose run app ash
$ python -m twine upload --repository-url https://pypi.org/legacy/ dist/*
# project then available at: https://pypi.org/project/bas-style-kit-jinja-templates/
$ exit
$ docker-compose down
```

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`. This will:

* build the source and binary artefacts for this project
* publish built artefacts for this project to the relevant PyPi repository

This process will deploy changes to [PyPi testing](https://test.pypi.org/) on all commits to the master branch.

This process will deploy changes to [PyPi](https://pypi.org/) on all tagged commits.

## Release procedure

### At release:

1. create a `release` branch
2. close release in CHANGELOG.md
3. push changes, merge the `release` branch into `master` and tag with version

The project will be built and published to PyPi automatically through [Continuous Deployment](#continuous-deployment).

### After release:

1. create a `next-release` branch
2. push changes and merge the `next-release` branch into `master`

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at: 
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the 
[Issue tracker](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/issues) for more information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2019, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under 
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at
[http://www.nationalarchives.gov.uk/doc/open-government-licence/](http://www.nationalarchives.gov.uk/doc/open-government-licence/)
