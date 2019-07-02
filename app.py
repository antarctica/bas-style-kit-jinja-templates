from flask import Flask, render_template, abort
# noinspection PyPackageRequirements
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader

from bas_style_kit_jinja_templates import BskTemplates

app = Flask(__name__)
app.jinja_loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas_style_kit_jinja_templates'),
})
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].site_title = 'BAS Style Kit Jinja Templates'
app.config['bsk_templates'].bsk_site_nav_brand_text = 'BAS Style Kit Jinja Templates'
app.config['bsk_templates'].site_description = 'A set of Jinja templates implementing the BAS Style Kit'
app.config['bsk_templates'].site_styles.append({
    'href': 'https://cdn.web.bas.ac.uk/libs/font-awesome-pro/5.9.0/css/all.min.css',
    'integrity': 'sha256-kanXop/o8YI8mee6ao6HKghRywSQiUisB6pXb6HRsWk='
})
app.config['bsk_templates'].bsk_site_nav_primary.append({
    'value': 'Layouts',
    'items': [
        {
            'value': 'Blank',
            'href': '/layouts/blank'
        },
        {
            'value': 'HTML',
            'href': '/layouts/html'
        },
        {
            'value': 'BSK Base',
            'href': '/layouts/bsk_base'
        },
        {
            'value': 'BSK Standard',
            'href': '/layouts/bsk_standard'
        }
    ]
})
app.config['bsk_templates'].bsk_site_nav_primary.append({
    'value': 'Patterns',
    'items': [
        {
            'value': 'Page not found',
            'href': '/patterns/page-not-found'
        },
        {
            'value': 'Problem with this service (basic)',
            'href': '/patterns/problem-with-service'
        },
        {
            'value': 'Service unavailable (basic)',
            'href': '/patterns/service-unavailable'
        },
        {
            'value': 'Start (basic)',
            'href': '/patterns/start-basic'
        },
        {
            'value': 'Start (more information)',
            'href': '/patterns/start-info'
        },
        {
            'value': 'Start (sign-in, Microsoft)',
            'href': '/patterns/start-sign-in-microsoft'
        },
        {
            'value': 'Sign-in (Microsoft)',
            'href': '/patterns/sign-in-microsoft'
        }
    ]
})
app.config['bsk_templates'].bsk_site_nav_primary.append({
    'value': 'Features',
    'items': [
        {
            'value': 'Active nav item',
            'href': '/features/active-nav-item/123abc'
        }
    ]
})
app.config['bsk_templates'].bsk_site_nav_primary.append({
    'value': 'Item',
    'href': '#'
})
app.config['bsk_templates'].bsk_site_nav_secondary.append({
    'value': 'Another Item',
    'href': '#',
    'target': '_blank'
})
app.config['bsk_templates'].bsk_site_nav_launcher.append({
    'value': 'Launcher Item',
    'href': '#'
})


@app.route('/')
def index():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/index.j2")


@app.route('/layouts/<layout>')
def render_layout(layout: str):
    layouts = [
        'blank',
        'html',
        'bsk_base',
        'bsk_standard'
    ]
    if layout not in layouts:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/layouts/{ layout }.j2")


@app.route('/patterns/<pattern>')
def render_pattern(pattern: str):
    patterns = [
        'page-not-found',
        'problem-with-service',
        'service-unavailable',
        'start-basic',
        'start-info',
        'start-sign-in-microsoft',
        'sign-in-microsoft'
    ]
    if pattern not in patterns:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/patterns/bsk_{ pattern }.j2")


@app.route('/features/active-nav-item/<dynamic_value>')
def render_feature_active_nav_item(dynamic_value: str):
    # noinspection PyUnresolvedReferences
    return render_template(
        f"app/features/active_nav_item.j2",
        value=dynamic_value,
        active_nav_item='/features/active-nav-item/123abc'
    )
