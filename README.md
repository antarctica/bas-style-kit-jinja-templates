# BAS Style Kit Jinja Templates

A set of [Jinja2](http://jinja.pocoo.org) templates implementing the [BAS Style Kit](https://style-kit.web.bas.ac.uk).

## Installation

### Pip package

The recommended way to install these templates is via its PyPi package,
[`bas-style-kit-jekyll-templates`](https://pypi.org/project/bas-style-kit-jinja-templates/).

**Note:** Since version 0.7.0, this package requires Jinja 3.0 or greater for compatibility with Flask 2.0.

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
app.config['BSK_TEMPLATES'] = BskTemplates()

# Required/recommended settings
app.config['BSK_TEMPLATES'].site_title = 'Example service'
app.config['BSK_TEMPLATES'].site_description = 'Service to act as an example'
app.config['BSK_TEMPLATES'].bsk_site_nav_brand_text = 'Example service'
app.config['BSK_TEMPLATES'].bsk_site_development_phase = 'beta'
app.config['BSK_TEMPLATES'].bsk_site_feedback_href = '/feedback'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_cookies_href = '/legal/cookies'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_copyright_href = '/legal/copyright'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_privacy_href = '/legal/privacy'

# Optional - add a custom CSS file with a relative URL
app.config['BSK_TEMPLATES'].site_styles.append({'href': '/css/app.css'})
# Optional - add a custom JS file with a SRI value
app.config['BSK_TEMPLATES'].site_scripts.append({'href': 'https://example.com/js/example.js', 'integrity': 'abc123'})
# Optional - enable Google Analytics
app.config['BSK_TEMPLATES'].site_analytics['id'] = '1234'
# Optional - choose between the `bsk-container` (used by default) and `bsk-container-fluid` layout container
app.config['BSK_TEMPLATES'].bsk_container_classes = ['bsk-container']
# Optional - add navigation menu items
app.config['BSK_TEMPLATES'].bsk_site_nav_primary.append({'value': 'Item', 'href': '#'})
app.config['BSK_TEMPLATES'].bsk_site_nav_secondary.append({
    'value': 'Dropdown',
    'items': [
        {'value': 'Sub-item 1', 'href': '#', 'target': '_blank'}
    ]
})
app.config['BSK_TEMPLATES'].bsk_site_nav_launcher.append({'value': 'Related service', 'href': 'https://example.com'})


@app.route('/')
def index():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/index.j2")
```

See the [Jinja setup](#jinja-setup) section for other ways of loading templates.

Where `app/index.j2` is a view located in `templates/index.j2` which extends an application layout:

```jinja2
{% extends 'app/layouts/app.j2' %}
{% block main_content %}
<p>Index view content...</p>
{% endblock %}
```

This layout in turn extends a layout provided by this package:

```jinja2
{% extends 'bas_style_kit/layouts/bsk_standard.j2' %}
```

### Using a page pattern

To create a page in an application based on a [Page pattern](#page-patterns), such as the
[page not found](https://style-kit.web.bas.ac.uk/patterns/page-not-found/) pattern, create a template (e.g.
`templates/errors/404.j2`) with the following:

```jinja2
{% extends 'bas_style_kit/patterns/bsk_page-not-found.j2' %}
```

To use this template as the 404 error handler in a Flask application for example:

```python
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('app/errors/404.j2'), 404
```

### Using a component pattern

To use a [Component pattern](#component-pattern), such as the
[ORCID iD](https://style-kit-testing.web.bas.ac.uk/patterns/orcid-id/) pattern, import and call the relevant Macro:

```jinja2
{% from "bas_style_kit/macros/bsk_pattern_orcid_id.j2" import pattern_orcid_id %}

<p>{{ pattern_orcid_id('https://sandbox.orcid.org/0000-0001-8373-6934') }}</p>
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

For example (using a Flask application with a `css/app.css` file with the default
[static files route](http://flask.pocoo.org/docs/1.0/tutorial/static/)):

```python
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].site_styles.append({'href': '/static/css/app.css'})
```

The `integrity` property is used to specify a
[Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) value for
a resource. If specified an `integrity` attribute and will be added to the generated markup. A `crossorigin`
attribute will also be added for
[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) support with a
hard-coded, anonymous, value.

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
| `value`     | String    | Yes      | Any string                 | *About*                                    | -                                     |
| `href`      | String    | Yes      | Any URL                    | */about* / *https://www.example.com/about* | Ignored if `items` set                |
| `items`     | Array     | No       | Array of menu item objects | -                                          | Ignored for navigation launcher items |
| *Any*       | String    | No       | As per attribute           | -                                          | Arbitrary attribute/value key/values  |

**Note:** The `items` property is only recursed once, deeper objects will be ignored.

For example (using a Flask application):

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_primary.push({'value': 'Item', 'href': '/about'})
app.config['BSK_TEMPLATES'].bsk_site_nav_primary.push({'value': 'Another Item', 'href': '#', 'target': '_blank'})
```

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_secondary.push({
    'value': 'Dropdown',
    'items': [
        {'value': 'Sub-item 1', 'href': 'https://www.example.com'}
    ]
})
```

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_launcher.push({'value': 'Related service', 'href': 'https://example.com'})
```

#### Active navigation items

These templates will automatically add the `.bsk-active` class to the relevant navigation item, and if relevant,
sub-item, where its `href` attribute exactly matches the current URL given by `{{ request.path }}`.

For example for a navigation item `{'value': 'About', 'href': '/about'}`, when visiting `https://www.example/about`,
the about navigation item will be made active, as the current path `/about` matches the `href` attribute.

This support doesn't support URL patterns, such as `/foo/{id}` where `{id}` is a dynamic value. In these cases the
`active_nav_item` variable can be set to the `href` value of a navigation item to make it active explicitly.

For example (using flask application):

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_primary.push({'value': 'Foo', 'href': '/foo'})

@app.route('/foo/<foo_id>')
def foo_details(foo_id: str):
    foo = get_foo(foo_id)

    return render_template(f"app/views/foo-details.j2", foo=foo, active_nav_item='/foo')
```

### Navbar branding

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
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_brand_text = 'Example service'
```

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_nav_brand_img_href = '/assets/img/navbar-brand-img.png'
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
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_development_phase = 'beta'
```

#### Experimental site phase

Where a website or application is in a staging environment, or otherwise used for development/testing activities, the
site phase can be set to `experimental` to use the conventional
[experimental phase](https://style-kit.web.bas.ac.uk/core/colours/#variants).

For example (using a Flask application):

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_development_phase = 'experimental'
```

### Google Analytics

To include the Google Analytics universal tracking library (gtag), set the `BskTemplates.bsk_site_analytics['id']`
property to relevant Google Analytics property ID.

**Note:** When used the anonymise IP option in Google Analytics is enabled by default.

For example (using a Flask application):

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].bsk_site_analytics['id'] = 'UA-12345678'
```

### Footer content

Add custom footer content to the `footer_content` block. It will be shown between the
[divider](https://style-kit.web.bas.ac.uk/components/footer/#divider) and
[Governance](https://style-kit.web.bas.ac.uk/components/footer/#governance) footer components.

It is recommended to include a [spacer](https://style-kit.web.bas.ac.uk/components/footer/#spacer) component after any
footer content to balance the whitespace within the footer.

For example:

```jinja2
{% block footer_content %}
<div>Footer content</div>
<div role="separator" class="bsk-footer-spacer"></div>
{% endblock %}
```

You can also set custom classes on the footer element by appending to the `bsk_footer_classes` list, or replacing all
classes by overriding the list.

### Patterns

[Patterns](https://style-kit.web.bas.ac.uk/patterns/) demonstrate preferred ways to ask information from, or
provide information to, end users for various tasks.

There are two types of pattern used in the Style Kit and these templates:

* [Pages](#page-patterns) - standalone pages designed to be used with or without customisation
* [Components](#component-patterns) - inline elements designed to be used without customisation using [Macros](#macros)

#### Page patterns

Page patterns define content for common pages such as [*Page not found* (404) pages](#using-a-page-pattern).

These templates implement page patterns as layouts/views. Blocks can be used to provide required or additional
information as needed.

##### Page not found pattern

For example:

(basic variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_page-not-found.j2' %}
```

##### Problem with this service pattern

Blocks:

`pattern_content`
: General content, including contact information.

For example:

(basic variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_problem-with-service.j2' %}

{% block pattern_content %}
<p>Contact the <a href="mailto:team@example.com">Example team</a> for more information.</p>
{% endblock %}
```

##### Service unavailable pattern

Variables:

`availability`
: Set to `replaced` for the [replaced](https://style-kit.web.bas.ac.uk/patterns/service-unavailable/#replaced) variant.
  Set to `closed` for the [closed](https://style-kit.web.bas.ac.uk/patterns/service-unavailable/#closed) variant.

Blocks:

`pattern_content`
: General content, including contact information.

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

##### Start pattern

Variables:

`call_to_action_url`
: Set to the href the call to action button should go to

`call_to_action_variant`
: Set to `default` for a standard 'start now' call to action button
  Set to `sign-in-microsoft` for a combined 'sign-in to continue' and 'start now' button

Blocks:

`pattern_content_uses`
: Set to an unordered list of items for the 'use this service to:' list

`pattern_content`
: General content, including 'more information' for contact information and 'before you begin' section if needed

For example:

(basic variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_start.j2' %}

{% set call_to_action_url = '#' %}

{% block pattern_content_uses %}
<ul>
    <li>A task</li>
    <li>Another task</li>
</ul>
{% endblock %}

{% block pattern_content %}
    <section class="bsk-before-you-start">
        <h2 class="bsk-h3">Before you start</h2>
        <p>Before you start information</p>
    </section>
    <section class="bsk-more-information">
        <h2 class="bsk-h3">More information</h2>
        <p>Contact the <a href="mailto:servicedesk.bas.ac.uk">BAS IT Service Desk</a> for more information.</p>
    </section>
{% endblock %}
```

(more information variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_start.j2' %}

{% set call_to_action_url = '#' %}
{% set call_to_action_variant = 'sign-in-microsoft' %}

{% block pattern_content_uses %}
    <ul>
        <li>A task</li>
        <li>Another task</li>
    </ul>
{% endblock %}

{% block pattern_content %}
    <section class="bsk-before-you-start">
        <h2 class="bsk-h3">Before you start</h2>
        <p>Before you start information</p>
    </section>
    <section class="bsk-more-information">
        <h2 class="bsk-h3">More information</h2>
        <p>Contact the <a href="mailto:servicedesk.bas.ac.uk">BAS IT Service Desk</a> for more information.</p>
        <p>More information</p>
    </section>
{% endblock %}
```

##### Sign-in (Microsoft) pattern

Variables:

`call_to_action_url`
: Set to the href the call to action button should go to

Blocks:

`pattern_content`
: Additional, optional, content if needed

For example:

(basic variant)

```jinja2
{% extends 'bas_style_kit/patterns/bsk_sign-in-microsoft.j2' %}

{% set call_to_action_url = '#' %}
```

#### Component patterns

These templates include macros for all component patterns. Macro parameters are used for customising each instance of
the component.

**Note:** Macro parameters are positional, meaning you need to ensure values are provided in the right order to work.
See the [Style Kit documentation](https://style-kit.web.bas.ac.uk/) for general information on using these patterns.

##### Item type header pattern

Parameters:

`item_type`
: The type or kind of thing the item is, e.g. if the item is a person, it's type is 'person'.

`item_title`
: A label specific to the item, e.g. if the item is a person their name.

```jinja2
{{ pattern_item_type_header('Item type', 'Item title') }}
```

For example:

```jinja2
{{ pattern_item_type_header('Person', 'Connie Watson') }}
```

##### ORCID ID pattern

Parameters:

`orcid_id`
: The ORCID iD of an individual as a URL

```jinja2
{{ pattern_orcid_id('orcid_id') }}
```

For example:

```jinja2
{{ pattern_orcid_id('https://sandbox.orcid.org/0000-0001-8373-6934') }}
```

## Components

All components are located in the `bas_style_kit_jinja_templates` package. Variables are
defined in `bas_style_kit_jinja_templates/__init__.py`, with all other components defined in
`bas_style_kit_jinja_templates//templates/`.

Components that are specific to the Style Kit are prefixed with `bsk--` or `bsk_`.

### Jinja setup

These templates require a *PrefixLoader* and *PackageLoader*
[Jinja loader](http://jinja.pocoo.org/docs/2.10/api/#loaders) to be loaded into an application:

```python
loader = PrefixLoader({
    'bas_style_kit': PackageLoader('bas-style-kit-jekyll-templates')
})
```

To set [Variable](#variables) values used in these templates, a `BskTemplates` class instance is needed. These templates
assume this instance will be available in Jinja's environment as `config.BSK_TEMPLATES`

For Flask applications this will occur automatically by adding the class instance to the
[Flask config object](https://flask.palletsprojects.com/en/1.1.x/config/):

```python
app.config['BSK_TEMPLATES'] = BskTemplates()
```

Typically applications have their own templates too, which can be loaded under a different prefix (such as `app`) using
a relevant loader, such as the default *FileSystemloader*.

```python
loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas-style-kit-jekyll-templates')
})
```

Or a *PackageLoader* (this assumes there is a package named `foo` and that has a module conventionally named
`templates`:

```python
loader = PrefixLoader({
    'app': PackageLoader('foo'),
    'bas_style_kit': PackageLoader('bas-style-kit-jekyll-templates')
})
```

In either case, use of a *PrefixLoader* means references to resources should include a prefix and a deliminator
(`/` by default).

For example calling an application layout would change from:

```jinja2
{% extends "layouts/base.j2" %}
```

To:

```jinja2
{% extends "app/layouts/base.j2" %}
```

Or to use a layout from these templates:

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
{% extends 'bas_style_kit/layouts/bsk_standard.j2' %}

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

They are used within other components, such as the [navigation menus](#navigation-menu-items) macro for processing
primary and secondary navigation menus the same way, and to implement [Component patterns](#component-patterns).

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

`bsk_footer_classes`
: Array of Style Kit classes which should be applied to the standard footer element

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

## Development

These templates are developed as a Python library `bas_style_kit_jinja_templates`. A bundled Flask application 
(`app.py`) is used to simulate its usage.

### Development environment

Git and [Poetry](https://python-poetry.org) are required to set up a local development environment of this application.

**Note:** If you use [Pyenv](https://github.com/pyenv/pyenv), this project sets a local Python version for consistency.

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk):

```shell
# clone from the BAS GitLab instance if possible
$ git clone https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates.git

# alternatively, clone from the GitHub mirror
$ git clone https://github.com/antarctica/bas-style-kit-jinja-templates.git

# setup virtual environment
$ cd bas-style-kit-jinja2-templates
$ poetry install
```

To run the bundled Flask app:

```shell
$ poetry run flask run
```

Then visit: [localhost:5000](http://localhost:5000).

### Code Style

PEP-8 style and formatting guidelines must be used for this project, except the 80 character line limit.
[Black](https://github.com/psf/black) is used for formatting, configured in `pyproject.toml` and enforced as part of
[Python code linting](#code-linting-python).

Black can be integrated with a range of editors, such as
[PyCharm](https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea), to apply formatting
automatically when saving files.

To apply formatting manually:

```shell
$ poetry run black src/ app.py
```

### Code Linting

[Flake8](https://flake8.pycqa.org) and various extensions are used to lint Python files. Specific checks, and any 
configuration options, are documented in the `./.flake8` config file.

To check files manually:

```shell
$ poetry run flake8 src/
```

Checks are run automatically in [Continuous Integration](#continuous-integration).

### Dependencies

Python dependencies for this project are managed with [Poetry](https://python-poetry.org) in `pyproject.toml`.

Non-code files, such as static files, can also be included in the [Python package](#python-package) using the
`include` key in `pyproject.toml`.

#### Adding new dependencies

To add a new (development) dependency:

```shell
$ poetry add (--dev) [dependency]
```

Then update the Docker image used for CI/CD builds and push to the BAS Docker Registry (which is provided by GitLab):

```shell
$ docker build -f gitlab-ci.Dockerfile -t docker-registry.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates:latest .
$ docker push docker-registry.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates:latest
```

#### Updating dependencies

```shell
$ poetry update
```

See the instructions above to update the Docker image used in CI/CD.

#### Dependency vulnerability checks

The [Safety](https://pypi.org/project/safety/) package is used to check dependencies against known vulnerabilities.

**IMPORTANT!** As with all security tools, Safety is an aid for spotting common mistakes, not a guarantee of secure
code. In particular this is using the free vulnerability database, which is updated less frequently than paid options.

This is a good tool for spotting low-hanging fruit in terms of vulnerabilities. It isn't a substitute for proper
vetting of dependencies, or a proper audit of potential issues by security professionals. If in any doubt you MUST seek
proper advice.

Checks are run automatically in [Continuous Integration](#continuous-integration).

To check locally:

```shell
$ poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin
```

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit)
and enforced as part of [Python code linting](#code-linting-python).

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

To check manually:

```shell
$ poetry run bandit -r src/ app.py
```

Checks are run automatically in [Continuous Integration](#continuous-integration).

## Testing

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

Pip dependencies are also [checked and monitored for vulnerabilities](#dependency-vulnerability-scanning).

## Distribution

This project is distributed as a Python package, hosted in 
[PyPi](https://pypi.org/project/bas-style-kit-jinja-templates/).

Source and binary packages are built and published automatically using
[Poetry](https://python-poetry.org) in [Continuous Deployment](#continuous-deployment).

**Note:** Except for tagged releases, Python packages built in CD will use `0.0.0` as a version to indicate they are
not formal releases.

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`.

## Release procedure

### At release:

1. create a `release` branch
2. close release in CHANGELOG.md
3. bump the package version as needed in `pyproject.toml`
4. push changes, merge the `release` branch into `main` and tag with version

The project will be built and published to PyPi automatically through [Continuous Deployment](#continuous-deployment).

### After release:

1. create a `next-release` branch
2. bump `templates_version` variable in `bas_style_kit_jinja_templates/__init__.py`
4. push changes and merge the `next-release` branch into `master`

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at:
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the
[Issue tracker](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-jinja2-templates/issues) for more information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

# Licence

Copyright (c) 2019-2024 UK Research and Innovation (UKRI), British Antarctic Survey (BAS).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
