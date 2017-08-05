from flask import Flask

from onepage.views import login, signup, novel


app = Flask(__name__)
app.register_blueprint(login.app)
app.register_blueprint(signup.app)
app.register_blueprint(novel.app)

app.config['SECRET_KEY'] = 'temp secret key'
