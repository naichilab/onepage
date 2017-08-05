from unittest import TestCase

from mock import Mock
from passlib.hash import argon2

from onepage.utils import auth
from onepage.models import User

TARGET_EMAIL = 'test@test.co.jp'
TARGET_PASSWORD = 'test'
OTHER_EMAIL = 'other@test.co.jp'
OTHER_PASSWORD = 'other'


class TestAuth(TestCase):
    def _get_mock_user(self):
        user = User()
        user.email = TARGET_EMAIL
        user.password_hash = argon2.hash(TARGET_PASSWORD)
        return user

    def test_can_login_failed(self):
        User.find_by_email = Mock(return_value=self._get_mock_user())
        assert auth.can_login(TARGET_EMAIL, OTHER_PASSWORD) is False
        assert auth.can_login(OTHER_EMAIL, OTHER_PASSWORD) is False

    def test_can_login_missing_user(self):
        User.find_by_email = Mock(return_value=None)
        assert auth.can_login("missing@test.co.jp", TARGET_PASSWORD) is False

    def test_can_login_success(self):
        User.find_by_email = Mock(return_value=self._get_mock_user())
        assert auth.can_login(TARGET_EMAIL, TARGET_PASSWORD) is True

    def test_can_signup(self):
        assert auth.can_signup('', '', '') is False
