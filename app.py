from flask_login import LoginManager, login_required, current_user
import os
from sqlalchemy.orm import Session
from blueprints.admin.admin import admin
from blueprints.auth.auth import auth_pages
from blueprints.inventory.inventory import inventory
from blueprints.profile.profile import profile_pages
from blueprints.purchase.purchase import purchase
from blueprints.application.application import application
from data import db_session
from data.db_session import create_engine_and_session
from flask import Flask, render_template, request, redirect, url_for
from data.user import User
# from form.inventory_report_form import AddReportForm
from data.inventory_report import InventoryReport
from werkzeug.utils import secure_filename
db_sess = db_session.create_engine_and_session('./db/inventory_crm.db')
UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'lJihdIUh12eIHUI34'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 8
app.config['UPLOAD_FOLDER'] = './forms'
app.template_folder = './templates'

app.register_blueprint(admin)
app.register_blueprint(auth_pages)
app.register_blueprint(profile_pages)
app.register_blueprint(inventory)
app.register_blueprint(purchase)
app.register_blueprint(application)
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page.user'))
    return render_template('main.html')


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.query(User).get(user_id)
    return user

# @app.route('/inv_report', methods=['GET', 'POST'])
# @login_required
# def add_report():
#     form = AddReportForm()
#     if form.validate_on_submit():
#         report = InventoryReport()
#         report.condition_before = form.condition_before.data
#         report.condition_after = form.condition_after.data
#         report.photo = form.photo.data
#         return render_template('admin.html')
#     return render_template('add_report.html', title='Добавление отчета', form=form)

if __name__ == '__main__':
    app.run()
