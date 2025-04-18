from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.models import (
    Motherboard, PowerSupply, Processor, GraphicsCard, 
    Cooler, RAM, HardDrive, Case
)
from app.forms.components import (
    MotherboardForm, PowerSupplyForm, ProcessorForm, GraphicsCardForm,
    CoolerForm, RAMForm, HardDriveForm, CaseForm
)
from app.utils.scraper import scrape_components
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('У вас нет прав администратора для доступа к этой странице', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    motherboards_count = Motherboard.query.count()
    power_supplies_count = PowerSupply.query.count()
    processors_count = Processor.query.count()
    gpus_count = GraphicsCard.query.count()
    coolers_count = Cooler.query.count()
    rams_count = RAM.query.count()
    hdds_count = HardDrive.query.count()
    cases_count = Case.query.count()
    
    return render_template('admin/dashboard.html', 
                          counts={
                              'motherboards': motherboards_count,
                              'power_supplies': power_supplies_count,
                              'processors': processors_count,
                              'gpus': gpus_count,
                              'coolers': coolers_count,
                              'rams': rams_count,
                              'hdds': hdds_count,
                              'cases': cases_count
                          })

# Маршруты для управления компонентами (пример для материнских плат)
@admin_bp.route('/motherboards')
@login_required
@admin_required
def motherboards():
    motherboards = Motherboard.query.all()
    return render_template('admin/components/motherboards.html', motherboards=motherboards)

@admin_bp.route('/motherboards/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_motherboard():
    form = MotherboardForm()
    if form.validate_on_submit():
        motherboard = Motherboard(
            name=form.name.data,
            price=form.price.data,
            form=form.form.data,
            soket=form.soket.data,
            type_member=form.type_member.data,
            interface=form.interface.data
        )
        db.session.add(motherboard)
        db.session.commit()
        flash('Материнская плата успешно добавлена', 'success')
        return redirect(url_for('admin.motherboards'))
    return render_template('admin/components/add_motherboard.html', form=form)

@admin_bp.route('/scrape', methods=['GET', 'POST'])
@login_required
@admin_required
def scrape():
    if request.method == 'POST':
        url = request.form.get('url')
        component_type = request.form.get('component_type')
        
        if url and component_type:
            try:
                results = scrape_components(url, component_type)
                flash(f'Успешно импортировано {len(results)} компонентов типа {component_type}', 'success')
            except Exception as e:
                flash(f'Ошибка при парсинге: {str(e)}', 'danger')
        else:
            flash('Необходимо указать URL и тип компонента', 'danger')
            
    return render_template('admin/scrape.html') 