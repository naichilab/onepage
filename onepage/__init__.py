from flask import Flask

from onepage.views import login, signup, novel


app = Flask(__name__)

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='<<',
    variable_end_string='>>',
    comment_start_string='<#',
    comment_end_string='#>'
))
app.jinja_options = jinja_options

app.register_blueprint(login.app)
app.register_blueprint(signup.app)
app.register_blueprint(novel.app)

app.config['SECRET_KEY'] = 'temp secret key'
