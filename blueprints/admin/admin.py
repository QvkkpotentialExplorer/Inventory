import click as click
from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from data.db_session import create_engine_and_session, db_sess
from data.inventory_type import InventoryType
from data.procrument_plan import ProcurementPlan
from data.user import User
from form.add_user_form import AddUserForm
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

@admin.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    users = db_sess.query(User).all()
    return render_template('users.html', users=users)


@admin.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        full_name = form.fullname.data


        user = User(username=username, role=role, full_name=full_name)
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()
        flash('Пользователь добавлен успешно!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('add_user.html', form = form)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    user = db_sess.query(User).get(user_id)
    if not user:
        flash('Пользователь не найден.', 'error')
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        email = request.form.get('email')

        if username:
            user.username = username
        if password:
            user.set_password(password)
        if role:
            user.role = role
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email

        db_sess.commit()
        flash('Пользователь изменен успешно!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('edit_user.html', user=user)

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    user = db_sess.query(User).get(user_id)
    if not user:
        flash('Пользователь не найден.', 'error')
        return redirect(url_for('admin.users'))

    db_sess.delete(user)
    db_sess.commit()
    flash('Пользователь удален успешно!', 'success')
    return redirect(url_for('admin.users'))
