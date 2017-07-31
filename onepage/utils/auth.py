from flask import session
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
    return email is not None and password is not None and pen_name is not None


def activate_session(email):
    session[email] = True


def inactivate_session(email):
    session.pop(email, None)


def is_authenticated(email):
    return email in session


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
