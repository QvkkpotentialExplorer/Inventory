from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import os

from data.user import User
from form.inventory_repair_form import InventoryRepairForm
from data import db_session
from data.db_session import db_sess
from data.inventory import Inventory
from data.inventory_repair import InventoryRepair
from data.inventory_request import InventoryRequest
from data.inventory_type import InventoryType
from form.inventory_add_form import AddInventoryForm, AddInventoryTypeForm
from form.inventory_request_form import InventoryRequestForm
from form.redact_inventory_form import RedactInventoryForm
from form.redact_inventory_type import RedactInventoryTypeForm
# from form.inventory_report_form import AddReportForm
from data.inventory_report import InventoryReport
from werkzeug.utils import secure_filename

inventory = Blueprint('inventory', __name__, url_prefix='/inventory/', template_folder='../templates')


@inventory.route('/create',methods=['GET', 'POST'])
@login_required
def add_new_inventory():
    if current_user.role == 'admin':
        form = AddInventoryForm()
        if form.validate_on_submit():
            inventory_type = db_sess.query(InventoryType).filter(InventoryType.name==form.inventory_type.data).first()
            for i in range(form.count.data):
                new_inventory = Inventory(inventory_type_id = inventory_type.id)
                new_inventory.name = f'{inventory_type.name}{new_inventory.id}'
                db_sess.add(new_inventory)
                db_sess.commit()
            return render_template('admin.html')

        return render_template('add_new_inventory.html',form = form)

@inventory.route('/create/type',methods=['GET', 'POST'])
@login_required
def add_new_inventory_type():

    if current_user.role == 'admin':
        form = AddInventoryTypeForm()
        if form.validate_on_submit():

            inventory_type = InventoryType(name = form.name.data,description = form.description.data)

            db_sess.add(inventory_type)
            db_sess.commit()
            return redirect(url_for('inventory.add_new_inventory'))
        return render_template('add_new_inventory_type.html',form = form)


@inventory.route('/available')
@login_required
def available_inventory():
    items = db_sess.query(Inventory).all()
    users = db_sess.query(User).all()
    return render_template('available_inventory.html', users = users, items = items)


@inventory.route('/<int:inventory_id>/update_status', methods=['POST'])
@login_required
def update_inventory_status(inventory_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа к этому действию.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    inventory_item = db_sess.query(Inventory).get(inventory_id)
    if not inventory_item:
        flash('Инвентарь не найден.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    new_status = request.form.get('status')
    if new_status in ['used', 'in_use', 'broken']:
        inventory_item.status = new_status
        if new_status == 'used':
            inventory_item.user_id = None
            inventory_item.username = None
        db_sess.commit()
        flash(f'Статус инвентаря "{inventory_item.name}" обновлён.', 'success')
    else:
        flash('Некорректный статус.', 'error')
    return redirect(url_for('inventory.available_inventory'))


@inventory.route('/<int:inventory_id>/delete', methods=['POST'])
@login_required
def delete_inventory(inventory_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    inventory_item = db_sess.query(Inventory).get(inventory_id)
    if not inventory_item:
        flash('Инвентарь не найден.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    db_sess.delete(inventory_item)
    db_sess.commit()
    flash(f'Инвентарь "{inventory_item.name}" успешно удален.', 'success')

    return redirect(url_for('inventory.available_inventory'))


@inventory.route('/<int:inventory_id>/repair', methods=['GET', 'POST'])
@login_required
def create_repair_request(inventory_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    form = InventoryRepairForm()
    if form.validate_on_submit():
        repair = InventoryRepair(
            inventory_id=inventory_id,
            user_id=current_user.id,
            status='pending',
            description=form.description.data
        )
        db_sess.add(repair)
        db_sess.commit()
        flash('Заявка на ремонт инвентаря успешно создана!', 'success')
        return redirect(url_for('inventory.available_inventory'))

    return render_template('create_repair_request.html', form=form)


@inventory.route('/repairs', methods=['GET'])
@login_required
def repairs():
    # Получаем статус из параметров URL (если он есть)
    status_filter = request.args.get('status', None)

    # Если фильтр по статусу задан
    if status_filter:
        repair_requests = db_sess.query(InventoryRepair).filter_by(status=status_filter).all()
    else:
        repair_requests = db_sess.query(InventoryRepair).all()

    if current_user.role == 'admin':
        return render_template('repairs.html', repair_requests=repair_requests)

    user_repairs = db_sess.query(InventoryRepair).filter_by(user_id=current_user.id).all()
    return render_template('repairs.html', repair_requests=user_repairs)


@inventory.route('/<int:inventory_id>/update_user', methods=['POST'])
@login_required
def update_inventory_user(inventory_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    inventory_item = db_sess.query(Inventory).get(inventory_id)
    if not inventory_item:
        flash('Инвентарь не найден.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    new_user_id = request.form.get('user_id')
    if new_user_id:
        user = db_sess.query(User).get(new_user_id)
        if user:
            inventory_item.user_id = new_user_id
            inventory_item.username = user.username
            db_sess.commit()
            flash(f'Пользователь инвентаря "{inventory_item.name}" обновлён.', 'success')
        else:
            flash('Пользователь не найден.', 'error')
    else:
        flash('Некорректный пользователь.', 'error')
    return redirect(url_for('inventory.available_inventory'))