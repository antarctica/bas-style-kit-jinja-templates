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

To create a page in an application based on a 
[page design pattern](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-pug-templates/tree/master#page-patterns), 
such as the [page not found](https://style-kit.web.bas.ac.uk/patterns/page-not-found/) pattern, create a template (e.g. 
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

CSS an/or JavaScript resources other than the Style Kit, such as application or website specific styling or 
interactivity can be included either as references to files, or as inline content.

This support is available providing a layout which inherit from the [HTML]() layout is used.

File resources will be included after the Style Kit's own resources (where a Style Kit layout is used) to ensure it has
priority. 

Inline content can be added after any files.

* CSS resources are outputted in the [styles]() block, at the end of the `<head>` element
* JS resources are outputted in the [scripts]() block, at the end of the `<body>` element

For files:

* CSS files are added as a resource object to the `site_styles` property of the `BskTemplates` class instance
* JS files are added as a resource object to the `site_scripts` property of the `BskTemplates` class instance

For inline content:

* CSS content should be appended to the [styles]() block
* JS content should be appended to the [scripts]() block

**Note:** Ensure to use `{{ super() }}` to append, rather than replacing the contents of a block. For example:

```jinja2
{% block scripts %}
    {{ super() }}
    console.log('jQuery version: ' + jQuery.fn.jquery);
{% endblock %}
```

