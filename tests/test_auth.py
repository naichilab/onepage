from passlib.hash import argon2

from onepage.utils import auth
from onepage.models import User


def test_can_login(monkeypatch):
    TARGET_EMAIL = 'test@test.co.jp'
    TARGET_PASSWORD = 'test'
    OTHER_EMAIL = 'other@test.co.jp'
    OTHER_PASSWORD = 'other'

    def get_mock_user(arg):
        user = User()
        user.email = TARGET_EMAIL
        user.password_hash = argon2.hash(TARGET_PASSWORD)
        return user

    monkeypatch.setattr(User, 'find_by_email', get_mock_user)
    assert auth.can_login(TARGET_EMAIL, TARGET_PASSWORD) is True
    assert auth.can_login(TARGET_EMAIL, OTHER_PASSWORD) is False
    assert auth.can_login(OTHER_EMAIL, OTHER_PASSWORD) is False

    monkeypatch.setattr(User, 'find_by_email', lambda x: None)
    assert auth.can_login("missing@test.co.jp", TARGET_PASSWORD) is False


def test_can_signup():
    assert auth.can_signup(None, None, None) is False
