from flask import Blueprint, request, redirect, render_template, url_for

from onepage.utils import auth

app = Blueprint('login', __name__, template_folder='templates')


@app.route('/login', methods=['get'])
def get_login():
    return render_template('login/login.html')


@app.route('/login', methods=['post'])
def post_login():
    if auth.can_login(request.form['email'], request.form['password']):
        auth.activate_session(request.form['email'])
        return redirect(url_for('novel.get_list'))
    else:
        return redirect(url_for('login.get_login'))


@app.route('/logout', methods=['post'])
def logout():
    auth.inactivate_session()
    return redirect(url_for('login.get_login'))
