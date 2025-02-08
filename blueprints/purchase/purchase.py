import click as click
from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from data.db_session import create_engine_and_session, db_sess
from data.inventory_type import InventoryType
from data.procrument_plan import ProcurementPlan
from data.user import User
from form.procurement_plan_form import ProcurementPlanForm
from flask import Blueprint
import requests

purchase = Blueprint('purchase', __name__, url_prefix='/purchase/', template_folder='../templates')


@purchase.route('/', methods=['GET', 'POST'])
@login_required
def add_procurement_plan():
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('index'))

    form = ProcurementPlanForm()
    form.inventory_type.choices = form.get_inventory_type()
    if form.validate_on_submit():
        inventory_type = db_sess.query(InventoryType).filter(InventoryType.name == form.inventory_type.data).first()
        if not inventory_type:
            flash('Указанный тип инвентаря не найден.', 'error')
            return redirect(request.url)

        plan = ProcurementPlan(
            inventory_type_id=inventory_type.id,
            quantity=form.quantity.data,
            price=form.price.data,
            supplier=form.supplier.data,
            planned_date=form.planned_date.data,
        )
        db_sess.add(plan)
        db_sess.commit()
        flash('План закупок успешно добавлен!', 'success')
        return redirect(url_for('purchase.view_procurement_plans'))
    return render_template('add_procurement_plan.html', form=form)

@purchase.route('/plans', methods=['GET'])
@login_required
def view_procurement_plans():
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('index'))
    plans = db_sess.query(ProcurementPlan).all()
    return render_template('view_procurement_plans.html', plans=plans)


@purchase.route('/import', methods=['GET'])
@login_required
def import_procurement_data():
    if current_user.role != 'admin':
        flash('У вас нет доступа для выполнения этого действия.', 'error')
        return redirect(url_for('index'))

    # Пример запроса к внешнему API
    response = requests.get('https://external-api.com/procurement_data')

    if response.status_code == 200:
        data = response.json()
        for item in data:
            inventory_type = db_sess.query(InventoryType).filter(InventoryType.name == item['inventory_type']).first()
            if inventory_type:
                plan = ProcurementPlan(
                    inventory_type_id=inventory_type.id,
                    quantity=item['quantity'],
                    price=item['price'],
                    supplier=item['supplier'],
                    planned_date=item['planned_date']
                )
                db_sess.add(plan)
        db_sess.commit()
        flash('Данные о закупках успешно импортированы.', 'success')
    else:
        flash('Ошибка при импортировании данных о закупках.', 'error')

    return redirect(url_for('purchase.view_procurement_plans'))
