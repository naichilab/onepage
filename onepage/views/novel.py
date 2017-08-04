from flask import Blueprint, render_template

from onepage.utils.auth import required_login

app = Blueprint('novel', __name__, template_folder='templates', url_prefix='/novel')


@app.route('/list', methods=['get'])
@required_login
def get_list():
    return render_template('novel/list.html')
