from datetime import datetime
from mock import Mock

from flask_testing import TestCase

from onepage.utils import auth
from onepage.models import Novel
from onepage.models import User
import onepage


class TestNovel(TestCase):
    def create_app(self):
        app = onepage.app
        app.config['TESTING'] = True
        return app

    def _create_mock_novel(self):
        mock_novel = Novel()
        mock_novel.id = 1
        mock_novel.user = User()
        mock_novel.created_at = datetime.now()
        mock_novel.updated_at = datetime.now()
        return mock_novel

    def test_get_novel_list(self):
        Novel.page_count = Mock(return_value=1)
        Novel.pagenation = Mock(return_value=[self._create_mock_novel()])
        self.client.get('/novel/list')
        self.assertTemplateUsed('novel/list.html')

    def test_get_novel_list_no_page_count(self):
        Novel.page_count = Mock(return_value=0)
        Novel.pagenation = Mock(return_value=[])
        self.client.get('/novel/list')
        self.assertTemplateUsed('novel/list.html')

    def test_get_novel_list_specified_page(self):
        Novel.page_count = Mock(return_value=1)
        Novel.pagenation = Mock(return_value=[self._create_mock_novel()])
        self.client.get('/novel/list/1')
        self.assertTemplateUsed('novel/list.html')

    def test_get_novel_list_not_found_page(self):
        self.assert404(self.client.get('/novel/list/-1'))
        self.assert404(self.client.get('/novel/list/0'))

    def test_get_novel_detail(self):
        Novel.find = Mock(return_value=self._create_mock_novel())
        self.client.get('/novel/1')
        self.assertTemplateUsed('novel/detail.html')

    def test_get_novel_detail_not_found(self):
        Novel.find = Mock(return_value=None)
        self.assert404(self.client.get('/novel/1'))

    def test_get_novel_write(self):
        auth.check_session = Mock(return_value=True)
        self.client.get('/novel/write')
        self.assertTemplateUsed('novel/write.html')

    def test_get_novel_write_not_login(self):
        auth.check_session = Mock(return_value=False)
        self.assertRedirects(self.client.get('/novel/write'), '/login')

    def test_get_novel_edit(self):
        auth.check_session = Mock(return_value=True)
        auth.check_author = Mock(return_value=True)
        Novel.find = Mock(return_value=self._create_mock_novel())
        self.client.get('/novel/edit/1')
        self.assertTemplateUsed('novel/write.html')

    def test_get_novel_edit_not_exist(self):
        auth.check_session = Mock(return_value=True)
        auth.check_author = Mock(return_value=True)
        Novel.find = Mock(return_value=None)
        self.assert404(self.client.get('/novel/edit/1'))

    def test_get_novel_edit_not_author(self):
        auth.check_session = Mock(return_value=True)
        auth.check_author = Mock(return_value=False)
        Novel.find = Mock(return_value=self._create_mock_novel())
        self.assert404(self.client.get('/novel/edit/aaa'))
