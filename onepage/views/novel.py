from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import session
from flask import abort

from onepage.models import Novel
from onepage.models import User
from onepage.utils.auth import required_login
from onepage.utils.auth import only_author

app = Blueprint('novel', __name__, template_folder='templates', url_prefix='/novel')


@app.route('/list', methods=['get'])
@app.route('/list/<int:page>', methods=['get'])
def get_list(page=1):
    count = Novel.page_count()
    if (count > 0 and page > count) or page <= 0:
        abort(404)

    novels = Novel.pagenation(int(page)) if count > 0 else []
    return render_template('novel/list.html', page_count=count, novels=novels)


@app.route('/<int:novel_id>', methods=['get'])
def get_detail(novel_id):
    novel = Novel.find(novel_id)
    if novel is not None:
        return render_template('novel/detail.html', novel=novel)
    else:
        # TODO: change custom error page
        abort(404)


@app.route('/write', methods=['get'])
@required_login
def get_write():
    return render_template('novel/write.html', novel=None)


@app.route('/write', methods=['post'])
@required_login
def post_write():
    novel_title = request.form['title']
    novel_text = request.form['text']

    novel = Novel()
    novel.title = novel_title
    novel.text = novel_text
    novel.user().associate(User.find_by_email(session['logged_in']))
    novel.save()

    return redirect(url_for('novel.get_detail', novel_id=novel.id))


@app.route('/edit/<int:novel_id>', methods=['get'])
@required_login
@only_author
def get_edit(novel_id):
    novel = Novel.find(novel_id)
    if novel is not None:
        return render_template('novel/write.html', novel=novel)
    else:
        # TODO: change custom error page
        abort(404)


@app.route('/edit/<int:novel_id>', methods=['post'])
@required_login
@only_author
def post_edit(novel_id):
    novel = Novel.find(novel_id)
    if novel is not None:
        novel.title = request.form.get('title')
        novel.text = request.form.get('text')
        novel.save()
        return redirect(url_for('novel.get_detail', novel_id=novel.id))
    else:
        abort(400)
