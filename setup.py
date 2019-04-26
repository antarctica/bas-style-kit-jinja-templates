import os

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.2.0'

# If a tagged commit, don't make a pre-release
if 'CI_COMMIT_TAG' not in os.environ:
    version = f"{ version }.dev{ os.getenv('CI_PIPELINE_ID') or None }"

setup(
    name="bas-style-kit-jinja-templates",
    version=version,
    author="British Antarctic Survey",
    author_email="webapps@bas.ac.uk",
    description="A set of Jinja2 templates implementing the BAS Style Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antarctica/bas-style-kit-jinja-templates",
    license='Open Government Licence v3.0',
    packages=['bas_style_kit_jinja_templates'],
    package_data={'bas_style_kit_jinja_templates': ['templates/**/*.j2']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
)
