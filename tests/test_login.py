from mock import Mock

from flask import Flask
from flask_testing import TestCase

from onepage.views import login, novel
from onepage.utils import auth


class TestClass(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'TestSecretKey'
        app.register_blueprint(login.app)
        app.register_blueprint(novel.app)
        return app

    def test_login_failed(self):
        auth.can_login = Mock(return_value=False)
        response = self.client.post('/login', data=dict(email='test', password='test'))
        self.assertRedirects(response, '/login')

    def test_login_success(self):
        auth.can_login = Mock(return_value=True)
        response = self.client.post('/login', data=dict(email='test', password='test'))
        self.assertRedirects(response, '/novel/list')
