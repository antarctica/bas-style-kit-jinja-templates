from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/')
def hello_world():
    return render_template('index.j2')
