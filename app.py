from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/basic')
def basic_layout():
    return render_template('basic.j2')


@app.route('/html')
def html_layout():
    return render_template('html.j2')
