from flask import Flask, render_template, abort

# noinspection PyPackageRequirements
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader

from bas_style_kit_jinja_templates import BskTemplates

app = Flask(__name__)
app.jinja_loader = PrefixLoader(
    {"app": FileSystemLoader("templates"), "bas_style_kit": PackageLoader("bas_style_kit_jinja_templates"),}
)
app.config["BSK_TEMPLATES"] = BskTemplates()
app.config["BSK_TEMPLATES"].site_title = "BAS Style Kit Jinja Templates"
app.config["BSK_TEMPLATES"].bsk_site_nav_brand_text = "BAS Style Kit Jinja Templates"
app.config["BSK_TEMPLATES"].site_description = "A set of Jinja templates implementing the BAS Style Kit"

app.config["BSK_TEMPLATES"].site_styles.append(
    {
        "href": "https://cdn.web.bas.ac.uk/libs/font-awesome-pro/5.13.0/css/all.min.css",
        "integrity": "sha256-DjbUjEiuM4tczO997cVF1zbf91BC9OzycscGGk/ZKks=",
    }
)
app.config["BSK_TEMPLATES"].bsk_site_nav_primary.append(
    {
        "value": "Layouts",
        "items": [
            {"value": "Blank", "href": "/layouts/blank"},
            {"value": "HTML", "href": "/layouts/html"},
            {"value": "BSK Base", "href": "/layouts/bsk_base"},
            {"value": "BSK Standard", "href": "/layouts/bsk_standard"},
        ],
    }
)
app.config["BSK_TEMPLATES"].bsk_site_nav_primary.append(
    {
        "value": "Patterns",
        "items": [
            {"value": "Page not found", "href": "/patterns/page-not-found"},
            {"value": "Problem with this service (basic)", "href": "/patterns/problem-with-service-basic"},
            {"value": "Problem with this service (alternative)", "href": "/patterns/problem-with-service-alternative"},
            {"value": "Service unavailable (basic)", "href": "/patterns/service-unavailable-basic"},
            {"value": "Service unavailable (alternative)", "href": "/patterns/service-unavailable-alternative"},
            {"value": "Service unavailable (availability)", "href": "/patterns/service-unavailable-availability"},
            {"value": "Service unavailable (closed)", "href": "/patterns/service-unavailable-closed"},
            {"value": "Service unavailable (partly closed)", "href": "/patterns/service-unavailable-partly-closed"},
            {"value": "Service unavailable (replace)", "href": "/patterns/service-unavailable-replaced"},
            {"value": "Start (basic)", "href": "/patterns/start-basic"},
            {"value": "Start (more information)", "href": "/patterns/start-info"},
            {"value": "Start (sign-in, Microsoft)", "href": "/patterns/start-sign-in-microsoft"},
            {"value": "Sign-in (Microsoft)", "href": "/patterns/sign-in-microsoft"},
            {"value": "ORCID iD", "href": "/patterns/orcid"},
            {"value": "Item type header", "href": "/patterns/item-type-header"},
        ],
    }
)
app.config["BSK_TEMPLATES"].bsk_site_nav_primary.append(
    {
        "value": "Features",
        "items": [
            {"value": "Active nav item", "href": "/features/active-nav-item/123abc"},
            {"value": "Analytics", "href": "/features/analytics"},
        ],
    }
)
app.config["BSK_TEMPLATES"].bsk_site_nav_primary.append({"value": "Item", "href": "#"})
app.config["BSK_TEMPLATES"].bsk_site_nav_secondary.append({"value": "Another Item", "href": "#", "target": "_blank"})
app.config["BSK_TEMPLATES"].bsk_site_nav_launcher.append({"value": "Launcher Item", "href": "#"})
app.config["BSK_TEMPLATES"].site_analytics["id"] = "UA-64130716-44"


@app.route("/")
def index():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/index.j2")


@app.route("/layouts/<layout>")
def render_layout(layout: str):
    layouts = ["blank", "html", "bsk_base", "bsk_standard"]
    if layout not in layouts:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/layouts/{ layout }.j2")


@app.route("/patterns/<pattern>")
def render_pattern(pattern: str):
    patterns = [
        "page-not-found",
        "problem-with-service-basic",
        "problem-with-service-alternative",
        "service-unavailable-basic",
        "service-unavailable-alternative",
        "service-unavailable-availability",
        "service-unavailable-closed",
        "service-unavailable-partly-closed",
        "service-unavailable-replaced",
        "start-basic",
        "start-info",
        "start-sign-in-microsoft",
        "sign-in-microsoft",
        "orcid",
        'item-type-header',
    ]
    if pattern not in patterns:
        abort(404)

    # noinspection PyUnresolvedReferences
    return render_template(f"app/patterns/bsk_{ pattern }.j2")


@app.route("/features/active-nav-item/<dynamic_value>")
def render_feature_active_nav_item(dynamic_value: str):
    # noinspection PyUnresolvedReferences
    return render_template(
        f"app/features/active_nav_item.j2", value=dynamic_value, active_nav_item="/features/active-nav-item/123abc"
    )


@app.route("/features/analytics")
def render_feature_analytics():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/features/analytics.j2")
