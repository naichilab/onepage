from flask import Blueprint, request, url_for, redirect, render_template

from onepage.utils import auth


app = Blueprint("signup", __name__, template_folder="templates")


@app.route("/signup", methods=['get'])
def get_signup():
        return render_template('login/signup.html')


@app.route("/signup", methods=['post'])
def post_signup():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    pen_name = request.form.get('pen_name', '')

    if auth.can_signup(email, password, pen_name):
        if auth.create_user(email, password, pen_name):
            auth.activate_session(request.form["email"])
            return redirect(url_for('novel.get_list'))

    return render_template('login/signup.html')
