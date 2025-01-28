import click as click
from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from data.db_session import create_engine_and_session, db_sess
from data.inventory_type import InventoryType
from data.procrument_plan import ProcurementPlan
from data.user import User
from form.procurement_plan_form import ProcurementPlanForm

admin = Blueprint('admin', __name__, url_prefix='/admin/', template_folder='../templates')


@admin.cli.command("addadmin")
@click.argument("name")
@click.argument("password")
def create_admin(name, password):
    # Создание сессии при каждом запуске команды
    db_sess = create_engine_and_session('db/inventory_crm.db')

    user = User(
        username=name,
        full_name=name,
        role='admin',
    )
    user.set_password(password)

    db_sess.add(user)
    db_sess.commit()
    db_sess.close()

    return 'Вы зареганы'
