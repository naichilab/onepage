from functools import wraps

from flask import session, redirect, url_for
from passlib.hash import argon2
from orator.exceptions.query import QueryException

from onepage.models import User


def can_login(email, password):
    """Validation login parameter(email, password) with rules.
        return validation result True/False.
    """

    login_user = User.find_by_email(email)
    return login_user is not None and argon2.verify(password, login_user.password_hash)


def can_signup(email, password, pen_name):
    """Validation signup parameter(email, password, pen_name) with rules.
        return validation result True/False.
    """

    # TODO validate detail rule
    return email != '' and password != '' and pen_name != ''


def activate_session(email):
    session['logged_in'] = email


def inactivate_session():
    session.pop('logged_in', None)


def required_login(func):
    """Decorator for check login state
        if not logged in, redirect to login page.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login.get_login'))

    return wrapper


def create_user(email, password, pen_name):
    """Creating a unique user
        return created new user. If failed creating new user, return None.
    """

    signup_user = User()
    signup_user.email = email
    signup_user.password_hash = argon2.hash(password)
    signup_user.pen_name = pen_name

    try:
        signup_user.save()
        return signup_user
    except QueryException:
        return None
