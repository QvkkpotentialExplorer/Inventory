from flask import Blueprint, Flask, render_template, redirect, request, abort, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.db_session import db_sess
from data.inventory import Inventory
from data.inventory_repair import InventoryRepair
from data.inventory_replacement import InventoryReplacement
from data.inventory_report import InventoryReport
from data.inventory_type import InventoryType
from data.user import User
from form.inventory_replacement_form import AddInventoryReplacementForm
from form.inventory_report_form import InventoryReportForm
from form.inventory_request_form import InventoryRequestForm
from data.inventory_request import InventoryRequest

application = Blueprint('application', __name__, url_prefix='/application/', template_folder='../templates')





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






@application.route('/reports', methods=['GET'])
@login_required
def view_reports():
    if current_user.role == 'admin':
        reports = db_sess.query(InventoryReport,User.username).outerjoin(User,User.id == InventoryReport.user_id).all()
    else:
        flash('У вас нет доступа к этому действию', 'danger')
        return redirect('/')

    return render_template('view_reports.html', reports=reports)



@application.route('/reports/add_report/<int:inventory_id>', methods=['GET', 'POST'])
@login_required
def add_report(inventory_id):
    if inventory_id is None:
        flash('Не указан инвентарь для отчета.', 'error')
        return redirect(url_for('application.view_reports'))
    form = InventoryReportForm()
    form.user.choices = [user.username for user in db_sess.query(User).all()]
    form.inventory_id.data = inventory_id  # Предзаполняем ID инвентаря
    inventory = db_sess.query(Inventory).filter(Inventory.id == inventory_id)
    if not inventory:
        flash('Некорректный идентификатор инвентаря', 'error')
        return redirect(url_for('application.view_reports'))

    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.username == form.user.data).first()

        report = InventoryReport(
            user_id=user.id,
            inventory_id=inventory_id,
            condition_before=form.condition_before.data,
            condition_after=form.condition_after.data,
            photo=form.photo.data,
            description = form.description.data
        )
        db_sess.add(report)
        db_sess.commit()
        flash('Отчёт успешно добавлен!', 'success')
        return redirect(url_for('application.view_reports'))
    return render_template('add_report.html', form=form)
@application.route('/requests/add_request', methods=['GET', 'POST'])
@login_required
def request_inventory():
    if current_user.role == 'user':
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
    else:
        return abort(401)
@application.route('/reject/inventory/<int:request_id>', methods=['GET', 'POST'])
@login_required
def reject_request_inventory(request_id):
    if current_user.role == 'admin':
        inventory_request = db_sess.query(InventoryRequest).filter(InventoryRequest.id == request_id).first()
        inventory_request.status ='rejected'
        db_sess.commit()
    else:
        return abort(401)
    return redirect(url_for('application.view_requests'))
@application.route('/approve/inventory/<int:request_id>/', methods=['GET', 'POST'])
@login_required
def approve_request_inventory(request_id):
    if current_user.role == "admin":
        inventory_request = db_sess.query(InventoryRequest).filter(InventoryRequest.id == request_id).first()

        inventories = db_sess.query(Inventory).filter(Inventory.inventory_type_id == inventory_request.inventory_type_id,Inventory.status=="new").all()
        count = len(inventories)

        if count<inventory_request.count:
            print('Я здесь')
            flash('Недостаточно свободно инвентаря данного типа, для одобрения заявки', 'danger')
        else:
            for inventory in inventories[0:inventory_request.count]:
                inventory.user_id = inventory_request.user_id
                inventory.status = 'in_use'
                db_sess.commit()
            inventory_request.status = 'approved'
            db_sess.commit()
            flash('Успешное одобрение заявки', 'success')
    else:
        return abort(401)
    return redirect(url_for('application.view_requests'))
@application.route('/requests', methods=['GET'])
@login_required
def view_requests():
    if current_user.role == 'admin':
        requests = (
            db_sess.query(InventoryRequest, User.username, InventoryType.name)
            .join(User, InventoryRequest.user_id == User.id)  # Join InventoryRequest with User
            .join(InventoryType,
                  InventoryRequest.inventory_type_id == InventoryType.id)  # Join InventoryRequest with InventoryType
            .filter(InventoryRequest.status == "pending")  # Filter requests for the current user
            .all()
        )
    else:
        requests = (
            db_sess.query(InventoryRequest, User.username, InventoryType.name)
            .join(User, InventoryRequest.user_id == User.id)  # Join InventoryRequest with User
            .join(InventoryType,
                  InventoryRequest.inventory_type_id == InventoryType.id)  # Join InventoryRequest with InventoryType
            .filter(InventoryRequest.user_id == current_user.id)  # Filter requests for the current user
            .all()
        )

        print(requests)
    return render_template('view_requests.html', requests=requests)



@application.route('/replacement/<int:inventory_id>', methods = ['GET','POST'])
@login_required
def replacement_inventory_request(inventory_id):
    if current_user.role == 'user':
        inventory = db_sess.query(Inventory).filter(Inventory.user_id == current_user.id, Inventory.status == 'in_use', Inventory.id == inventory_id).first()
        print(inventory)
        if not inventory:
            return abort(401)
        inventory_replacement = db_sess.query(InventoryReplacement).filter(
            InventoryReplacement.inventory_id == int(inventory_id), InventoryReplacement.status == 'pending').first()
        inventory_repair = db_sess.query(InventoryRepair).filter(InventoryRepair.status == 'pending',InventoryRepair.inventory_id == int(inventory_id)).first()

        if inventory_repair:
            flash('Была подана заявка на ремонт','danger')
            return redirect(url_for('inventory.repairs'))
        if inventory_replacement:
            flash('Заявка на замену уже подана','danger')
            return redirect(url_for('application.view_replacement_requests'))
        form = AddInventoryReplacementForm()
        form.inventory_id.data = inventory.id


        if form.validate_on_submit():
            print(inventory.id)
            inventory_replacement = InventoryReplacement(user_id = current_user.id,status = 'pending',inventory_id = inventory.id,reason_description = form.reason_description.data)
            db_sess.add(inventory_replacement)
            db_sess.commit()
            flash('Заявка успешно создана!', 'success')
            return redirect(url_for('application.view_replacement_requests'))

        return render_template('inventory_replacement.html',form= form)
    else:
        return abort(401)




@application.route('replacement/requests/',methods = ['GET','POST'])
@login_required
def view_replacement_requests():
    if current_user.role == 'admin':
        requests = (
            db_sess.query(InventoryReplacement, User.username, InventoryType.name,Inventory.id)
            .join(User, InventoryReplacement.user_id == User.id)  # Join InventoryRequest with User
            .join(Inventory,
                  Inventory.id == InventoryReplacement.inventory_id)
            .join(InventoryType,InventoryType.id == Inventory.inventory_type_id)# Join InventoryRequest with InventoryType
            .filter(InventoryReplacement.status == "pending")  # Filter requests for the current user
            .all()
        )
        return render_template('view_replacement_requests.html', requests = requests,  current_user = current_user)
    else:
        requests = (
            db_sess.query(InventoryReplacement, User.username, InventoryType.name, Inventory.id)
            .join(User, InventoryReplacement.user_id == User.id)  # Join InventoryRequest with User
            .join(Inventory,
                  Inventory.id== InventoryReplacement.inventory_id)
            .join(InventoryType,
                  InventoryType.id == Inventory.inventory_type_id)  # Join InventoryRequest with InventoryType
            .filter(InventoryReplacement.status == "pending", InventoryReplacement.user_id == current_user.id)  # Filter requests for the current user
            .all()
        )
        return render_template('view_replacement_requests.html', requests = requests, current_user = current_user)
@application.route('replacement/approve/<int:inventory_replacement_id>',methods = ['GET','POST'])
@login_required
def replacement_request_approve(inventory_replacement_id):
    if current_user.role == 'admin':
        inventory_replacement_request = db_sess.query(InventoryReplacement).filter(InventoryReplacement.id == inventory_replacement_id).first()
        if not inventory_replacement_request:
            return abort(404)
        inventory = db_sess.query(Inventory).filter(Inventory.id == inventory_replacement_request.inventory_id).first()
        inventories = db_sess.query(Inventory).filter(
            Inventory.inventory_type_id == inventory.inventory_type_id, Inventory.status == "new").all()
        count = len(inventories)
        if count <1:
            flash('Недостаточно свободно инвентаря данного типа, для одобрения заявки', 'danger')
        else:
            inventory_replacement_request.status = 'approved'
            inventory.status = 'used'
            inventory.user_id = None
            inventories[0].user_id = current_user.id
            inventories[0].status = 'in_use'
            db_sess.commit()
            flash('Заявка одобрена!', 'success')
            return redirect(url_for('application.view_replacement_requests'))
    else:
        return abort(401)
@application.route('replacement/reject/<int:inventory_replacement_id>',methods = ['GET','POST'])
@login_required
def replacement_reject_request(inventory_replacement_id):
    if current_user.role == 'admin':
        inventory_replacement_request = db_sess.query(InventoryReplacement).filter(
            InventoryReplacement.id == inventory_replacement_id).first()
        if not inventory_replacement_request:
            return abort(402)
        inventory_replacement_request.status = 'rejected'
        db_sess.commit()
        flash('Заявка отклонена', 'danger')
        return redirect(url_for('view_replacement_requests.html'))