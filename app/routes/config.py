from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.models import (
    Configuration, Motherboard, PowerSupply, Processor, 
    GraphicsCard, Cooler, RAM, HardDrive, Case
)
from app.forms.config import ConfigurationForm

config_bp = Blueprint('config', __name__)

@config_bp.route('/')
@login_required
def my_configs():
    configs = Configuration.query.filter_by(user_id=current_user.id).all()
    return render_template('config/my_configs.html', configs=configs)

@config_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_config():
    form = ConfigurationForm()
    
    form.motherboard_id.choices = [(m.id, f"{m.name} - {m.price} руб.") for m in Motherboard.query.all()]
    form.supply_id.choices = [(p.id, f"{p.name} - {p.price} руб.") for p in PowerSupply.query.all()]
    form.cpu_id.choices = [(c.id, f"{c.name} - {c.price} руб.") for c in Processor.query.all()]
    form.gpu_id.choices = [(g.id, f"{g.name} - {g.price} руб.") for g in GraphicsCard.query.all()]
    form.cooler_id.choices = [(c.id, f"{c.name} - {c.price} руб.") for c in Cooler.query.all()]
    form.ram_id.choices = [(r.id, f"{r.name} - {r.price} руб.") for r in RAM.query.all()]
    form.hdd_id.choices = [(h.id, f"{h.name} - {h.price} руб.") for h in HardDrive.query.all()]
    form.frame_id.choices = [(f.id, f"{f.name} - {f.price} руб.") for f in Case.query.all()]
    
    if form.validate_on_submit():
        config = Configuration(
            name=form.name.data,
            user_id=current_user.id,
            motherboard_id=form.motherboard_id.data if form.motherboard_id.data else None,
            supply_id=form.supply_id.data if form.supply_id.data else None,
            cpu_id=form.cpu_id.data if form.cpu_id.data else None,
            gpu_id=form.gpu_id.data if form.gpu_id.data else None,
            cooler_id=form.cooler_id.data if form.cooler_id.data else None,
            ram_id=form.ram_id.data if form.ram_id.data else None,
            hdd_id=form.hdd_id.data if form.hdd_id.data else None,
            frame_id=form.frame_id.data if form.frame_id.data else None
        )
        
        db.session.add(config)
        db.session.commit()
        
        flash('Конфигурация успешно создана', 'success')
        return redirect(url_for('config.view_config', config_id=config.conf_id))
    
    return render_template('config/new_config.html', form=form)

@config_bp.route('/<int:config_id>')
@login_required
def view_config(config_id):
    config = Configuration.query.get_or_404(config_id)
    # Проверка доступа (только владелец конфигурации может просматривать)
    if config.user_id != current_user.id and not current_user.is_admin():
        flash('У вас нет прав для просмотра этой конфигурации', 'danger')
        return redirect(url_for('config.my_configs'))
    
    compatibility_issues = config.compatibility_check()
    total_price = config.total_price()
    
    return render_template(
        'config/view_config.html', 
        config=config, 
        compatibility_issues=compatibility_issues,
        total_price=total_price
    )

@config_bp.route('/<int:config_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_config(config_id):
    config = Configuration.query.get_or_404(config_id)
    # Проверка прав
    if config.user_id != current_user.id:
        flash('У вас нет прав для редактирования этой конфигурации', 'danger')
        return redirect(url_for('config.my_configs'))
    
    form = ConfigurationForm(obj=config)
    
    form.motherboard_id.choices = [(m.id, f"{m.name} - {m.price} руб.") for m in Motherboard.query.all()]
    form.supply_id.choices = [(p.id, f"{p.name} - {p.price} руб.") for p in PowerSupply.query.all()]
    form.cpu_id.choices = [(c.id, f"{c.name} - {c.price} руб.") for c in Processor.query.all()]
    form.gpu_id.choices = [(g.id, f"{g.name} - {g.price} руб.") for g in GraphicsCard.query.all()]
    form.cooler_id.choices = [(c.id, f"{c.name} - {c.price} руб.") for c in Cooler.query.all()]
    form.ram_id.choices = [(r.id, f"{r.name} - {r.price} руб.") for r in RAM.query.all()]
    form.hdd_id.choices = [(h.id, f"{h.name} - {h.price} руб.") for h in HardDrive.query.all()]
    form.frame_id.choices = [(f.id, f"{f.name} - {f.price} руб.") for f in Case.query.all()]
    
    if form.validate_on_submit():
        config.name = form.name.data
        config.motherboard_id = form.motherboard_id.data if form.motherboard_id.data else None
        config.supply_id = form.supply_id.data if form.supply_id.data else None
        config.cpu_id = form.cpu_id.data if form.cpu_id.data else None
        config.gpu_id = form.gpu_id.data if form.gpu_id.data else None
        config.cooler_id = form.cooler_id.data if form.cooler_id.data else None
        config.ram_id = form.ram_id.data if form.ram_id.data else None
        config.hdd_id = form.hdd_id.data if form.hdd_id.data else None
        config.frame_id = form.frame_id.data if form.frame_id.data else None
        
        db.session.commit()
        
        flash('Конфигурация успешно обновлена', 'success')
        return redirect(url_for('config.view_config', config_id=config.conf_id))
    
    return render_template('config/edit_config.html', form=form, config=config)

@config_bp.route('/<int:config_id>/delete', methods=['POST'])
@login_required
def delete_config(config_id):
    config = Configuration.query.get_or_404(config_id)
    # Проверка прав
    if config.user_id != current_user.id and not current_user.is_admin():
        flash('У вас нет прав для удаления этой конфигурации', 'danger')
        return redirect(url_for('config.my_configs'))
    
    db.session.delete(config)
    db.session.commit()
    
    flash('Конфигурация успешно удалена', 'success')
    return redirect(url_for('config.my_configs'))

@config_bp.route('/filter')
@login_required
def filter_components():
    component_type = request.args.get('type')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    if not component_type:
        return jsonify([])
    
    # Выбор модели в зависимости от типа компонента
    model_map = {
        'motherboard': Motherboard,
        'power_supply': PowerSupply,
        'processor': Processor,
        'graphics_card': GraphicsCard,
        'cooler': Cooler,
        'ram': RAM,
        'hard_drive': HardDrive,
        'case': Case
    }
    
    model = model_map.get(component_type)
    if not model:
        return jsonify([])
    
    query = model.query
    
    if min_price is not None:
        query = query.filter(model.price >= min_price)
    if max_price is not None:
        query = query.filter(model.price <= max_price)
    
    # Дополнительные фильтры в зависимости от типа компонента
    if component_type == 'motherboard':
        form = request.args.get('form')
        soket = request.args.get('soket')
        if form:
            query = query.filter(Motherboard.form == form)
        if soket:
            query = query.filter(Motherboard.soket == soket)
    elif component_type == 'processor':
        soket = request.args.get('soket')
        if soket:
            query = query.filter(Processor.soket == soket)
    
    components = query.all()
    result = [{
        'id': c.id,
        'name': c.name,
        'price': c.price
    } for c in components]
    
    return jsonify(result)

@config_bp.route('/check_compatibility', methods=['POST'])
@login_required
def check_compatibility():
    # Получаем данные компонентов из запроса
    data = request.json
    
    # Создаем временную конфигурацию для проверки совместимости
    temp_config = Configuration(
        name="temp",
        user_id=current_user.id,
        motherboard_id=data.get('motherboard_id'),
        cpu_id=data.get('cpu_id'),
        ram_id=data.get('ram_id'),
        gpu_id=data.get('gpu_id'),
        supply_id=data.get('supply_id'),
        cooler_id=data.get('cooler_id'),
        hdd_id=data.get('hdd_id'),
        frame_id=data.get('frame_id')
    )
    
    # Загружаем связанные объекты, которые могут понадобиться для проверки
    if temp_config.motherboard_id:
        temp_config.motherboard = Motherboard.query.get(temp_config.motherboard_id)
    if temp_config.cpu_id:
        temp_config.processor = Processor.query.get(temp_config.cpu_id)
    if temp_config.ram_id:
        temp_config.ram = RAM.query.get(temp_config.ram_id)
    if temp_config.gpu_id:
        temp_config.graphics_card = GraphicsCard.query.get(temp_config.gpu_id)
    if temp_config.supply_id:
        temp_config.power_supply = PowerSupply.query.get(temp_config.supply_id)
    if temp_config.cooler_id:
        temp_config.cooler = Cooler.query.get(temp_config.cooler_id)
    if temp_config.hdd_id:
        temp_config.hard_drive = HardDrive.query.get(temp_config.hdd_id)
    if temp_config.frame_id:
        temp_config.case = Case.query.get(temp_config.frame_id)
    
    # Проверяем совместимость
    issues = temp_config.compatibility_check()
    
    # Возвращаем результат
    if issues:
        return jsonify({
            'status': 'warning',
            'issues': issues,
            'html': '<i class="fas fa-exclamation-triangle me-2"></i>Обнаружены проблемы совместимости!'
        })
    else:
        return jsonify({
            'status': 'success',
            'issues': [],
            'html': '<i class="fas fa-check-circle me-2"></i>Все компоненты совместимы'
        })

@config_bp.route('/calculate_price', methods=['POST'])
@login_required
def calculate_price():
    # Получаем данные компонентов из запроса
    data = request.json
    
    # Создаем временную конфигурацию для расчета стоимости
    temp_config = Configuration(
        name="temp",
        user_id=current_user.id,
        motherboard_id=data.get('motherboard_id'),
        cpu_id=data.get('cpu_id'),
        ram_id=data.get('ram_id'),
        gpu_id=data.get('gpu_id'),
        supply_id=data.get('supply_id'),
        cooler_id=data.get('cooler_id'),
        hdd_id=data.get('hdd_id'),
        frame_id=data.get('frame_id')
    )
    
    # Загружаем связанные объекты, которые необходимы для расчета цены
    if temp_config.motherboard_id:
        temp_config.motherboard = Motherboard.query.get(temp_config.motherboard_id)
    if temp_config.cpu_id:
        temp_config.processor = Processor.query.get(temp_config.cpu_id)
    if temp_config.ram_id:
        temp_config.ram = RAM.query.get(temp_config.ram_id)
    if temp_config.gpu_id:
        temp_config.graphics_card = GraphicsCard.query.get(temp_config.gpu_id)
    if temp_config.supply_id:
        temp_config.power_supply = PowerSupply.query.get(temp_config.supply_id)
    if temp_config.cooler_id:
        temp_config.cooler = Cooler.query.get(temp_config.cooler_id)
    if temp_config.hdd_id:
        temp_config.hard_drive = HardDrive.query.get(temp_config.hdd_id)
    if temp_config.frame_id:
        temp_config.case = Case.query.get(temp_config.frame_id)
    
    # Рассчитываем общую стоимость
    total_price = temp_config.total_price()
    
    # Возвращаем результат
    return jsonify({
        'total_price': total_price,
        'formatted_price': f"{total_price} ₽"
    }) 