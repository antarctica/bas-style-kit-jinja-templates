from flask import Flask, render_template, abort
# noinspection PyPackageRequirements
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader

from bas_style_kit_jinja_templates import BskTemplates

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas_style_kit_jinja_templates'),
})
app.config['bsk_templates'] = BskTemplates()
app.config['bsk_templates'].site_title = 'BAS Style Kit Jinja Templates'
app.config['bsk_templates'].site_description = 'A set of Jinja templates implementing the BAS Style Kit'


@app.route('/layouts/<layout>')
def render_layout(layout: str):
    layouts = [
        'blank',
        'html',
        'bsk_base',
    ]
    if layout not in layouts:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/layouts/{ layout }.j2")



