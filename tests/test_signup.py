from mock import Mock
from flask_testing import TestCase

from onepage.utils import auth
from onepage.models import User
import onepage


class TestSignup(TestCase):
    def create_app(self):
        app = onepage.app
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'TestSecretKey'
        return app

    def test_signup_failed_empty_value(self):
        self.client.post('/signup', data=dict(email='', password='', pen_name=''))
        self.assertTemplateUsed('login/signup.html')

    def test_signup_failed_no_request(self):
        self.client.post('/signup')
        self.assertTemplateUsed('login/signup.html')

    def test_signup_success(self):
        auth.can_signup = Mock(return_value=True)
        auth.create_user = Mock(return_value=User())
        response = self.client.post('/signup', data=dict(email='test', password='test', pen_name='test'))
        self.assertRedirects(response, '/novel/list')
