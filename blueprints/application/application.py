from flask import Blueprint, Flask, render_template, redirect, request, abort, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.db_session import db_sess
from data.inventory import Inventory
from data.inventory_report import InventoryReport
from data.inventory_type import InventoryType
from data.user import User
from form.inventory_report_form import InventoryReportForm
from form.inventory_request_form import InventoryRequestForm
from data.inventory_request import InventoryRequest

application = Blueprint('application', __name__, url_prefix='/application/', template_folder='../templates')


@application.route('/requests/add_request', methods=['GET', 'POST'])
@login_required
def request_inventory():
    form = InventoryRequestForm()
    if form.validate_on_submit():
        request_item = InventoryRequest(
            user_id=current_user.id,
            inventory_type_id=form.inventory_type_id.data,
            count=form.count.data,
            status='pending'
        )
        db_sess.add(request_item)
        db_sess.commit()
        flash('Заявка успешно создана!', 'success')
        return redirect(url_for('application.view_requests'))
    return render_template('inventory_request.html', form=form)


@application.route('/requests/<int:request_id>/update', methods=['POST'])
@login_required
def update_request_status(request_id):
    global inventory_type_item
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('application.view_requests'))

    request_item = db_sess.query(InventoryRequest).get(request_id)
    if not request_item:
        flash('Заявка не найдена.', 'error')
        return redirect(url_for('application.view_requests'))

    new_status = request.form.get('status')
    if new_status in ['pending', 'approved', 'rejected']:
        request_item.status = new_status

        if new_status == 'approved':
            inventory_type_item = db_sess.query(InventoryType).get(request_item.inventory_type_id)
            inventory_items = db_sess.query(Inventory).filter(
                Inventory.inventory_type_id == request_item.inventory_type_id,
                (Inventory.user_id == None) | (Inventory.user_id == ""),
                (Inventory.username == None) | (Inventory.username == "")
            ).all()
            user_item = db_sess.query(User).get(request_item.user_id)
            count_item = request_item.count

            if count_item <= len(inventory_items):
                for i in range(count_item):
                    inventory_items[i].user_id = user_item.id
                    inventory_items[i].username = user_item.username
                    inventory_items[i].status = 'in_use'
            else:
                flash("Не достаточно инвентаря", "error")

        db_sess.commit()
        flash(f'Статус заявки обновлён на "{new_status}".', 'success')

        # Уведомляем пользователя о статусе
        user = db_sess.query(User).get(request_item.user_id)
        flash(f'Вашу заявку на инвентарь "{inventory_type_item.name}" обновили до статуса "{new_status}".', 'info')

    else:
        flash('Некорректный статус.', 'error')

    return redirect(url_for('application.view_requests'))



@application.route('/requests', methods=['GET'])
@login_required
def view_requests():
    if current_user.role == 'admin':
        requests = db_sess.query(InventoryRequest).all()
    else:
        requests = db_sess.query(InventoryRequest).filter_by(user_id=current_user.id).all()
    return render_template('view_requests.html', requests=requests)


@application.route('/reports', methods=['GET'])
@login_required
def view_reports():
    if current_user.role == 'admin':
        reports = db_sess.query(InventoryReport).all()
    else:
        flash('У вас нет доступа к этому действию', 'error')
        return redirect('/')

    return render_template('view_reports.html', reports=reports)



@application.route('/reports/add_report/<int:inventory_id>', methods=['GET', 'POST'])
@login_required
def add_report(inventory_id):
    if inventory_id is None:
        flash('Не указан инвентарь для отчета.', 'error')
        return redirect(url_for('application.view_reports'))
    form = InventoryReportForm()
    form.inventory_id.data = inventory_id  # Предзаполняем ID инвентаря
    if form.validate_on_submit():
        report = InventoryReport(
            user_id=current_user.id,
            inventory_id=inventory_id,
            condition_before=form.condition_before.data,
            condition_after=form.condition_after.data,
            photo=form.photo.data
        )
        db_sess.add(report)
        db_sess.commit()
        flash('Отчёт успешно добавлен!', 'success')
        return redirect(url_for('application.view_reports'))
    return render_template('add_report.html', form=form)

