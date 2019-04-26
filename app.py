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
app.config['bsk_templates'].bsk_site_nav_primary.append({
    'title': 'Item',
    'href': '#'
})
app.config['bsk_templates'].bsk_site_nav_secondary.append({
    'title': 'Another Item',
    'items': [
        {
            'title': 'Sub-Item',
            'href': '#'
        }
    ]
})
app.config['bsk_templates'].bsk_site_nav_launcher.append({
    'title': 'Launcher Item',
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
        'service-unavailable'
    ]
    if pattern not in patterns:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/patterns/bsk_{ pattern }.j2")
