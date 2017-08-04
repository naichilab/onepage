from flask import Flask

from onepage.views import login, novel


app = Flask(__name__)
app.register_blueprint(login.app)
app.register_blueprint(novel.app)

app.config['SECRET_KEY'] = 'temp secret key'
