from mock import Mock
from flask_testing import TestCase

from onepage.utils import auth
import onepage


class TestLogin(TestCase):
    def create_app(self):
        app = onepage.app
        app.config['TESTING'] = True
        return app

    def test_login_failed(self):
        auth.can_login = Mock(return_value=False)
        self.client.post('/login', data=dict(email='test', password='test'))
        self.assertTemplateUsed('login/login.html')

    def test_login_success(self):
        auth.can_login = Mock(return_value=True)
        response = self.client.post('/login', data=dict(email='test', password='test'))
        self.assertRedirects(response, '/novel/list')
