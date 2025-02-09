from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import os

from data.inventory_replacement import InventoryReplacement
from data.user import User
from form.inventory_repair_form import InventoryRepairForm
from data import db_session
from data.db_session import db_sess
from data.inventory import Inventory
from data.inventory_repair import InventoryRepair
from data.inventory_request import InventoryRequest
from data.inventory_type import InventoryType
from data.procrument_plan import ProcurementPlan
from form.inventory_add_form import AddInventoryForm, AddInventoryTypeForm, InventoryTypeRedactForm
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
        form.inventory_type.choices= form.get_inventory_type()
        if form.validate_on_submit():
            inventory_type = db_sess.query(InventoryType).filter(InventoryType.name==form.inventory_type.data).first()
            for i in range(form.count.data):
                new_inventory = Inventory(inventory_type_id = inventory_type.id)
                new_inventory.name = f'{inventory_type.name}{new_inventory.id}'
                db_sess.add(new_inventory)
                db_sess.commit()
            return redirect(url_for('inventory.available_inventory'))

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

    if current_user.role == 'admin':
        items = (
            db_sess.query(Inventory, InventoryType.name, User.username)
            .join(InventoryType, Inventory.inventory_type_id == InventoryType.id)
            .outerjoin(User, Inventory.user_id == User.id)  # LEFT JOIN с User
            .all()

        )
        users = db_sess.query(User).all()
    else:
        items = db_sess.query(Inventory,InventoryType.name).join(InventoryType, Inventory.inventory_type_id == InventoryType.id).filter(Inventory.user_id == current_user.id).all()
        users =[]
        users =[]
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
        flash(f'Статус инвентаря "{inventory_item.id}" обновлён.', 'success')
    else:
        flash('Некорректный статус.', 'error')
    return redirect(url_for('inventory.available_inventory'))


@inventory.route('/inventory/<int:inventory_id>/delete', methods=['POST'])
@login_required
def delete_inventory(inventory_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    inventory_item = db_sess.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_item:
        flash('Инвентарь не найден.', 'error')
        return redirect(url_for('inventory.available_inventory'))

    # Удаляем связанные данные (ремонты, отчеты и замены)
    db_sess.query(InventoryRepair).filter(InventoryRepair.inventory_id == inventory_item.id).delete()
    db_sess.query(InventoryReport).filter(InventoryReport.inventory_id == inventory_item.id).delete()
    db_sess.query(InventoryReplacement).filter(InventoryReplacement.inventory_id == inventory_item.id).delete()

    # Удаляем инвентарь
    db_sess.delete(inventory_item)
    db_sess.commit()

    flash(f'Инвентарь с номером {inventory_item.id} был успешно удалён.', 'success')
    return redirect(url_for('inventory.available_inventory'))



@inventory.route('/type/<int:inventory_type_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_inventory_type(inventory_type_id):
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.view_inventory_type'))

    inventory_type = db_sess.query(InventoryType).filter(InventoryType.id == inventory_type_id).first()
    if not inventory_type:
        flash('Тип инвентаря не найден.', 'error')
        return redirect(url_for('inventory.view_inventory_type'))

    # Проверяем, если есть связанные инвентари
    inventory_items = db_sess.query(Inventory).filter(Inventory.inventory_type_id == inventory_type.id).all()

    # Если форма отправлена методом POST
    if request.method == 'POST':
        # Удаляем связанные заявки
        db_sess.query(InventoryRequest).filter(InventoryRequest.inventory_type_id == inventory_type.id).delete()
        db_sess.query(ProcurementPlan).filter(ProcurementPlan.inventory_type_id == inventory_type.id).delete()
        # Удаляем все инвентари с этим типом
        for inventory_item in inventory_items:
            # Удаляем связанные ремонты, отчеты и замены
            db_sess.query(InventoryRepair).filter(InventoryRepair.inventory_id == inventory_item.id).delete()
            db_sess.query(InventoryReport).filter(InventoryReport.inventory_id == inventory_item.id).delete()
            db_sess.query(InventoryReplacement).filter(InventoryReplacement.inventory_id == inventory_item.id).delete()
            db_sess.delete(inventory_item)

        # Удаляем тип инвентаря
        db_sess.delete(inventory_type)
        db_sess.commit()

        flash(f'Тип инвентаря "{inventory_type.name}" и все связанные данные удалены.', 'success')
        return redirect(url_for('inventory.view_inventory_type'))

    # Если нет связанных инвентарей, удаляем тип инвентаря сразу
    if not inventory_items:
        db_sess.delete(inventory_type)
        db_sess.commit()
        flash(f'Тип инвентаря "{inventory_type.name}" удален.', 'success')
        return redirect(url_for('inventory.view_inventory_type'))

    # Если есть связанные инвентари, показываем страницу с подтверждением
    return render_template('confirm_delete_inventory_type.html', inventory_type=inventory_type,
                           inventory_items=inventory_items)

@inventory.route('/<int:inventory_id>/repair', methods=['GET', 'POST'])
@login_required
def create_repair_request(inventory_id):
    if current_user.role != 'user':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('inventory.available_inventory'))
    inventory = db_sess.query(Inventory).filter(Inventory.id == inventory_id, Inventory.user_id == current_user.id)
    if not inventory:
        flash('Вы не имеете доступа к своей матери','danger')

    inventory_replacement = db_sess.query(InventoryReplacement).filter( InventoryReplacement.inventory_id == int(inventory_id), InventoryReplacement.status == 'pending').first()
    inventory_repair = db_sess.query(InventoryRepair).filter(InventoryRepair.status == 'pending', InventoryRepair.inventory_id == int(inventory_id)).first()

    if inventory_repair:
        flash('Заявка на ремонт уже подана','danger')
        return redirect(url_for('inventory.repairs'))
    if inventory_replacement:
        flash('Нельзя подать заявку на ремонт, так как до этого была подана заявка на замену','danger')
        return redirect(url_for('application.view_replacement_requests'))

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
        repair_requests = (
            db_sess.query(InventoryRepair, User.username, InventoryType.name, Inventory.id)
            .join(User, InventoryRepair.user_id == User.id)  # Join InventoryRequest with User
            .join(Inventory,
                  Inventory.id == InventoryRepair.inventory_id)
            .join(InventoryType,
                  InventoryType.id == Inventory.inventory_type_id)  # Join InventoryRequest with InventoryType
            .filter(InventoryRepair.status == "pending")  # Filter requests for the current user
                .all()[::-1]
        )
    else:
        repair_requests = (
            db_sess.query(InventoryRepair, User.username, InventoryType.name, Inventory.id)
            .join(User, InventoryRepair.user_id == User.id)  # Join InventoryRequest with User
            .join(Inventory,
                  Inventory.id == InventoryRepair.inventory_id)
            .join(InventoryType,
                  InventoryType.id == Inventory.inventory_type_id)  # Join InventoryRequest with InventoryType
            .filter(InventoryRepair.status == "pending")  # Filter requests for the current user
            .all()
        )[::-1]

    if current_user.role == 'admin':
        return render_template('repairs.html', requests=repair_requests)

    user_repairs = (
        db_sess.query(InventoryRepair, User.username, InventoryType.name, Inventory.id)
        .join(User, InventoryRepair.user_id == User.id)  # Join InventoryRequest with User
        .join(Inventory,
              Inventory.id == InventoryRepair.inventory_id)
        .join(InventoryType,
              InventoryType.id == Inventory.inventory_type_id)  # Join InventoryRequest with InventoryType
        .filter(
                InventoryRepair.user_id == current_user.id)  # Filter requests for the current user
        .all()[::-1]
    )
    return render_template('repairs.html', requests = user_repairs)


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
            flash(f'Пользователь инвентаря "{inventory_item.id}" обновлён.', 'success')
        else:
            flash('Пользователь не найден.', 'error')
    else:
        flash('Некорректный пользователь.', 'error')
    return redirect(url_for('inventory.available_inventory'))


@inventory.route('/type', methods=['GET','POST'])
@login_required
def view_inventory_type():
    inventory_type = db_sess.query(InventoryType).all()
    inventory_types = []
    for inventory in inventory_type:
        inventory_types.append(
            (inventory, len(list(db_sess.query(Inventory).filter(Inventory.inventory_type_id == inventory.id)))))
    return render_template('view_inventory_type.html',inventory_types = inventory_types)


@inventory.route('/type/<int:inventory_type_id>', methods=['GET', 'POST'])
@login_required
def redact_inventory_type(inventory_type_id):
    inventory_type = db_sess.query(InventoryType).filter(InventoryType.id == inventory_type_id).first()
    if not inventory_type:
        abort(404)

    form = InventoryTypeRedactForm()

    if form.validate_on_submit():
        inventory_type.name = form.name.data
        inventory_type.description = form.description.data
        db_sess.commit()
        return redirect(url_for('inventory.view_inventory_type'))
    return render_template('edit_inventory_type.html', form=form, inventory_type=inventory_type)


@inventory.route('repair/approve/<int:inventory_repair_id>', methods = ['POST'])
@login_required
def approve_repair(inventory_repair_id):
    if current_user.role == 'admin':
        inventory_repair = db_sess.query(InventoryRepair).filter(InventoryRepair.id == inventory_repair_id, InventoryRepair.status == 'pending').first()
        inventory_item = db_sess.query(Inventory).filter(Inventory.id == inventory_repair.inventory_id).first()
        if not inventory_repair:
            return abort(401)
        inventory_repair.status='approved'
        inventory_item.status = 'broken'
        db_sess.commit()
        flash('Заявка успешно одобрена','success')
        return redirect(url_for('inventory.repairs'))
    else:
        return flash('Вы не имеет доступа к этому методу')

@inventory.route('repair/reject/<int:inventory_repair_id>', methods = ['POST'])
@login_required
def reject_repair(inventory_repair_id):
    if current_user.role == 'admin':
        inventory_repair = db_sess.query(InventoryRepair).filter(InventoryRepair.id == inventory_repair_id,
InventoryRepair.status == 'pending').first()
        if not inventory_repair:
            return abort(401)
        inventory_repair.status = 'rejected'
        db_sess.commit()
        flash('Заявка успешно отклонена', 'danger')
        return redirect(url_for('inventory.repairs'))
    else:
        return flash('Вы не имеет доступа к этому методу')
