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

# Маршруты для материнских плат
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
            memory_type=form.memory_type.data,
            interface=form.interface.data
        )
        db.session.add(motherboard)
        db.session.commit()
        flash('Материнская плата успешно добавлена', 'success')
        return redirect(url_for('admin.motherboards'))
    return render_template('admin/components/add_motherboard.html', form=form)

@admin_bp.route('/motherboards/delete/<int:motherboard_id>', methods=['POST'])
@login_required
@admin_required
def delete_motherboard(motherboard_id):
    motherboard = Motherboard.query.get_or_404(motherboard_id)
    db.session.delete(motherboard)
    db.session.commit()
    flash('Материнская плата успешно удалена', 'success')
    return redirect(url_for('admin.motherboards'))

# Маршруты для процессоров
@admin_bp.route('/processors')
@login_required
@admin_required
def processors():
    processors = Processor.query.all()
    return render_template('admin/components/processors.html', processors=processors)

@admin_bp.route('/processors/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_processor():
    form = ProcessorForm()
    if form.validate_on_submit():
        processor = Processor(
            name=form.name.data,
            price=form.price.data,
            soket=form.soket.data,
            frequency=form.frequency.data,
            power_use=form.power_use.data
        )
        db.session.add(processor)
        db.session.commit()
        flash('Процессор успешно добавлен', 'success')
        return redirect(url_for('admin.processors'))
    return render_template('admin/components/add_processor.html', form=form)

@admin_bp.route('/processors/delete/<int:processor_id>', methods=['POST'])
@login_required
@admin_required
def delete_processor(processor_id):
    processor = Processor.query.get_or_404(processor_id)
    db.session.delete(processor)
    db.session.commit()
    flash('Процессор успешно удален', 'success')
    return redirect(url_for('admin.processors'))

# Маршруты для видеокарт
@admin_bp.route('/graphics_cards')
@login_required
@admin_required
def graphics_cards():
    graphics_cards = GraphicsCard.query.all()
    return render_template('admin/components/graphics_cards.html', graphics_cards=graphics_cards)

@admin_bp.route('/graphics_cards/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_graphics_card():
    form = GraphicsCardForm()
    if form.validate_on_submit():
        graphics_card = GraphicsCard(
            name=form.name.data,
            price=form.price.data,
            frequency=form.frequency.data,
            soket=form.soket.data,
            power_use=form.power_use.data
        )
        db.session.add(graphics_card)
        db.session.commit()
        flash('Видеокарта успешно добавлена', 'success')
        return redirect(url_for('admin.graphics_cards'))
    return render_template('admin/components/add_graphics_card.html', form=form)

@admin_bp.route('/graphics_cards/delete/<int:graphics_card_id>', methods=['POST'])
@login_required
@admin_required
def delete_graphics_card(graphics_card_id):
    graphics_card = GraphicsCard.query.get_or_404(graphics_card_id)
    db.session.delete(graphics_card)
    db.session.commit()
    flash('Видеокарта успешно удалена', 'success')
    return redirect(url_for('admin.graphics_cards'))

# Маршруты для оперативной памяти
@admin_bp.route('/rams')
@login_required
@admin_required
def rams():
    rams = RAM.query.all()
    return render_template('admin/components/rams.html', rams=rams)

@admin_bp.route('/rams/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_ram():
    form = RAMForm()
    if form.validate_on_submit():
        ram = RAM(
            name=form.name.data,
            price=form.price.data,
            frequency=form.frequency.data,
            memory_type=form.memory_type.data,
            power_use=form.power_use.data,
            capacity=form.capacity.data
        )
        db.session.add(ram)
        db.session.commit()
        flash('Оперативная память успешно добавлена', 'success')
        return redirect(url_for('admin.rams'))
    return render_template('admin/components/add_ram.html', form=form)

@admin_bp.route('/rams/delete/<int:ram_id>', methods=['POST'])
@login_required
@admin_required
def delete_ram(ram_id):
    ram = RAM.query.get_or_404(ram_id)
    db.session.delete(ram)
    db.session.commit()
    flash('Оперативная память успешно удалена', 'success')
    return redirect(url_for('admin.rams'))

# Маршруты для жестких дисков
@admin_bp.route('/hard_drives')
@login_required
@admin_required
def hard_drives():
    hard_drives = HardDrive.query.all()
    return render_template('admin/components/hard_drives.html', hard_drives=hard_drives)

@admin_bp.route('/hard_drives/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_hard_drive():
    form = HardDriveForm()
    if form.validate_on_submit():
        hard_drive = HardDrive(
            name=form.name.data,
            price=form.price.data,
            capacity=form.capacity.data,
            recording=form.recording.data,
            reading=form.reading.data
        )
        db.session.add(hard_drive)
        db.session.commit()
        flash('Жесткий диск успешно добавлен', 'success')
        return redirect(url_for('admin.hard_drives'))
    return render_template('admin/components/add_hard_drive.html', form=form)

@admin_bp.route('/hard_drives/delete/<int:hard_drive_id>', methods=['POST'])
@login_required
@admin_required
def delete_hard_drive(hard_drive_id):
    hard_drive = HardDrive.query.get_or_404(hard_drive_id)
    db.session.delete(hard_drive)
    db.session.commit()
    flash('Жесткий диск успешно удален', 'success')
    return redirect(url_for('admin.hard_drives'))

# Маршруты для блоков питания
@admin_bp.route('/power_supplies')
@login_required
@admin_required
def power_supplies():
    power_supplies = PowerSupply.query.all()
    return render_template('admin/components/power_supplies.html', power_supplies=power_supplies)

@admin_bp.route('/power_supplies/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_power_supply():
    form = PowerSupplyForm()
    if form.validate_on_submit():
        power_supply = PowerSupply(
            name=form.name.data,
            price=form.price.data,
            power=form.power.data,
            type=form.type.data
        )
        db.session.add(power_supply)
        db.session.commit()
        flash('Блок питания успешно добавлен', 'success')
        return redirect(url_for('admin.power_supplies'))
    return render_template('admin/components/add_power_supply.html', form=form)

@admin_bp.route('/power_supplies/delete/<int:power_supply_id>', methods=['POST'])
@login_required
@admin_required
def delete_power_supply(power_supply_id):
    power_supply = PowerSupply.query.get_or_404(power_supply_id)
    db.session.delete(power_supply)
    db.session.commit()
    flash('Блок питания успешно удален', 'success')
    return redirect(url_for('admin.power_supplies'))

# Маршруты для кулеров
@admin_bp.route('/coolers')
@login_required
@admin_required
def coolers():
    coolers = Cooler.query.all()
    return render_template('admin/components/coolers.html', coolers=coolers)

@admin_bp.route('/coolers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_cooler():
    form = CoolerForm()
    if form.validate_on_submit():
        cooler = Cooler(
            name=form.name.data,
            price=form.price.data,
            speed=form.speed.data,
            power_use=form.power_use.data
        )
        db.session.add(cooler)
        db.session.commit()
        flash('Кулер успешно добавлен', 'success')
        return redirect(url_for('admin.coolers'))
    return render_template('admin/components/add_cooler.html', form=form)

@admin_bp.route('/coolers/delete/<int:cooler_id>', methods=['POST'])
@login_required
@admin_required
def delete_cooler(cooler_id):
    cooler = Cooler.query.get_or_404(cooler_id)
    db.session.delete(cooler)
    db.session.commit()
    flash('Кулер успешно удален', 'success')
    return redirect(url_for('admin.coolers'))

# Маршруты для корпусов
@admin_bp.route('/cases')
@login_required
@admin_required
def cases():
    cases = Case.query.all()
    return render_template('admin/components/cases.html', cases=cases)

@admin_bp.route('/cases/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_case():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(
            name=form.name.data,
            price=form.price.data,
            form=form.form.data
        )
        db.session.add(case)
        db.session.commit()
        flash('Корпус успешно добавлен', 'success')
        return redirect(url_for('admin.cases'))
    return render_template('admin/components/add_case.html', form=form)

@admin_bp.route('/cases/delete/<int:case_id>', methods=['POST'])
@login_required
@admin_required
def delete_case(case_id):
    case = Case.query.get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash('Корпус успешно удален', 'success')
    return redirect(url_for('admin.cases'))

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