from flask import Blueprint, render_template
from flask_login import login_required, current_user

from data.db_session import db_sess
from data.user import User



profile_pages = Blueprint('profile_page', __name__, template_folder='../templates', static_folder='static', url_prefix='/profile/')
@profile_pages.route('/user')
@login_required
def user():
    user = db_sess.query(User).filter(User.username == current_user.username).first()

    if current_user.role == 'admin':
        return render_template('admin.html')
    else:
        return render_template('user.html', user=user)
