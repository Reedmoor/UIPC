from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
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
from app.utils.price_comparison import run_price_comparison
from functools import wraps
from datetime import datetime
import os
import json
import subprocess
import sys
from app.utils.DNS_parsing import main as dns_parser
import logging

# Настройка логирования
logger = logging.getLogger('admin_panel')

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Добавляем фильтр для получения текущей даты и времени
@admin_bp.app_template_filter('now')
def _jinja2_filter_now():
    return datetime.now()


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

@admin_bp.route('/motherboards/edit/<int:motherboard_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_motherboard(motherboard_id):
    motherboard = Motherboard.query.get_or_404(motherboard_id)
    form = MotherboardForm(obj=motherboard)

    if form.validate_on_submit():
        form.populate_obj(motherboard)
        db.session.commit()
        flash('Материнская плата успешно обновлена!', 'success')
        return redirect(url_for('admin.motherboards'))

    return render_template('admin//components/edit_motherboard.html', form=form, motherboard=motherboard)


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
            base_clock=form.base_clock.data,
            turbo_clock=form.turbo_clock.data,
            cores=form.cores.data,
            threads=form.threads.data,
            power_use=form.power_use.data
        )
        db.session.add(processor)
        db.session.commit()
        flash('Процессор успешно добавлен', 'success')
        return redirect(url_for('admin.processors'))
    return render_template('admin/components/add_processor.html', form=form)

@admin_bp.route('/processors/edit/<int:processor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_processor(processor_id):
    processor = Processor.query.get_or_404(processor_id)
    form = ProcessorForm(obj=processor)
    
    if form.validate_on_submit():
        form.populate_obj(processor)
        db.session.commit()
        flash('Процессор успешно обновлен!', 'success')
        return redirect(url_for('admin.processors'))
    
    return render_template('admin/components/edit_processor.html', form=form, processor=processor)

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
            type=form.type.data,
            certificate=form.certificate.data
        )
        db.session.add(power_supply)
        db.session.commit()
        flash('Блок питания успешно добавлен', 'success')
        return redirect(url_for('admin.power_supplies'))
    return render_template('admin/components/add_power_supply.html', form=form)

@admin_bp.route('/power_supplies/edit/<int:power_supply_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_power_supply(power_supply_id):
    power_supply = PowerSupply.query.get_or_404(power_supply_id)
    form = PowerSupplyForm(obj=power_supply)
    
    if form.validate_on_submit():
        form.populate_obj(power_supply)
        db.session.commit()
        flash('Блок питания успешно обновлен!', 'success')
        return redirect(url_for('admin.power_supplies'))
    
    return render_template('admin/components/edit_power_supply.html', form=form, power_supply=power_supply)

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
    # Get existing parser results if available
    dns_results = []
    citilink_results = []
    env_citilink_category = os.environ.get('CATEGORY', '')
    
    try:
        # Пробуем найти product_data.json для результатов DNS
        dns_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'DNS_parsing', 'product_data.json')
        if os.path.exists(dns_file_path):
            with open(dns_file_path, 'r', encoding='utf-8') as f:
                dns_results = json.load(f)
                # Проверяем и обрабатываем формат данных
                for item in dns_results:
                    # Добавляем поля, если их нет
                    if 'price_discounted' not in item and 'price_original' not in item:
                        if 'price' in item:
                            item['price_original'] = item['price']
                            item['price_discounted'] = item['price']
                    
                    # Проверяем наличие категории
                    if 'categories' not in item or not item['categories']:
                        item['categories'] = []
                        
                    # Логгируем загруженные данные
                    logger.info(f"Загружен продукт DNS: {item.get('name')}")
        else:
            logger.warning(f"Файл результатов DNS парсера не найден по пути: {dns_file_path}")
    except Exception as e:
        logger.error(f'Ошибка чтения результатов DNS парсера: {str(e)}')
        flash(f'Ошибка чтения результатов DNS парсера: {str(e)}', 'warning')
    
    try:
        citilink_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'Citi_parser', 'Товары.json')
        if os.path.exists(citilink_file_path):
            with open(citilink_file_path, 'r', encoding='utf-8') as f:
                try:
                    # Try to load the file directly
                    citilink_results = json.load(f)
                except json.JSONDecodeError:
                    # If that fails, read content and then load
                    f.seek(0)  # Go back to the beginning of the file
                    content = f.read()
                    if content.endswith(',\n]'):
                        content = content.replace(',\n]', '\n]')
                    citilink_results = json.loads(content)
                
                # Debugging information
                logger.info(f"Загружено {len(citilink_results)} товаров Citilink")
                if len(citilink_results) > 0:
                    # Process each item to ensure consistent structure
                    for item in citilink_results:
                        # Make sure required fields exist
                        if 'categories' not in item or not item['categories']:
                            item['categories'] = []
                    
                    logger.info(f"Пример первого товара: {citilink_results[0].get('name')} - {citilink_results[0].get('price')}")
        else:
            logger.warning(f"Файл результатов Citilink парсера не найден по пути: {citilink_file_path}")
    except Exception as e:
        logger.error(f'Ошибка чтения результатов Citilink парсера: {str(e)}')
        flash(f'Ошибка чтения результатов Citilink парсера: {str(e)}', 'warning')
    
    # Try to read category from .env file if not in environment
    if not env_citilink_category:
        try:
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('CATEGORY='):
                            env_citilink_category = line.strip().split('=', 1)[1]
                            break
        except Exception as e:
            logger.error(f"Error reading .env file: {e}")
            print(f"Error reading .env file: {e}")
    
    return render_template('admin/scrape.html', 
                           dns_results=dns_results, 
                           citilink_results=citilink_results,
                           env_citilink_category=env_citilink_category)

@admin_bp.route('/run-dns-parser', methods=['POST'])
@login_required
@admin_required
def run_dns_parser():
    category = request.form.get('dns_category', '')
    max_items = request.form.get('dns_max_items', '20')
    
    try:
        # Get path to DNS parser directory
        dns_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'DNS_parsing')
        
        # Set MAX_ITEMS environment variable
        os.environ['MAX_ITEMS'] = max_items
        
        # Change to DNS parser directory
        current_dir = os.getcwd()
        os.chdir(dns_parser_dir)
        
        # Add the DNS parser directory to Python path
        if dns_parser_dir not in sys.path:
            sys.path.insert(0, dns_parser_dir)
        
        # Run the DNS parser with the selected category
        try:
            # Use the system Python interpreter
            python_executable = sys.executable
            
            if category:
                flash(f'Парсер DNS будет запущен для категории "{category}"', 'info')
                # Run script with category parameter
                subprocess.run([python_executable, 'main.py', category, max_items], check=True, cwd=dns_parser_dir)
            else:
                flash('Парсер DNS будет запущен для всех категорий', 'info')
                # Run script without category parameter
                subprocess.run([python_executable, 'main.py'], check=True, cwd=dns_parser_dir)
        except Exception as e:
            flash(f'Парсер DNS завершился с ошибкой: {str(e)}', 'warning')
        
        # Change back to original directory
        os.chdir(current_dir)
        
        # Read results
        try:
            items_file = os.path.join(dns_parser_dir, 'product_data.json')
            if os.path.exists(items_file):
                with open(items_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                flash(f'Парсер DNS успешно выполнен. Получено {len(results)} товаров.', 'success')
            else:
                flash('Файл с результатами не найден. Проверьте парсер.', 'warning')
        except Exception as f:
            flash(f'Не удалось прочитать результаты парсера DNS: {str(f)}', 'warning')
    except Exception as e:
        flash(f'Ошибка при запуске парсера DNS: {str(e)}', 'danger')
    
    return redirect(url_for('admin.scrape'))

@admin_bp.route('/run-citilink-parser', methods=['POST'])
@login_required
@admin_required
def run_citilink_parser():
    category = request.form.get('citilink_category', '')
    
    if not category:
        flash('Необходимо выбрать категорию для парсинга Citilink', 'warning')
        return redirect(url_for('admin.scrape'))
    
    try:
        # Get path to Citilink parser directory
        citilink_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'Citi_parser')
        
        # Convert short category to full URL path for the parser
        category_map = {
            'videokarty': 'videokarty',
            'protsessory': 'protsessory',
            'materinskie-platy': 'materinskie-platy',
            'operativnaya-pamyat': 'operativnaya-pamyat'
        }
        full_category = category_map.get(category, category)
        
        # Create a command to directly run the PowerShell command to create/update .env file
        # This ensures it is created in the correct directory with proper encoding
        env_setup_cmd = f'Set-Content -Path "{os.path.join(citilink_parser_dir, ".env")}" -Value "CATEGORY={full_category}"'
        subprocess.run(['powershell', '-Command', env_setup_cmd], check=True)
            
        # Run the Citilink parser directly from the main.py file
        main_py_path = os.path.join(citilink_parser_dir, 'main.py')
        
        # Execute the script directly with the correct Python interpreter
        python_executable = sys.executable
        try:
            # Change to the parser directory first
            current_dir = os.getcwd()
            os.chdir(citilink_parser_dir)
            
            # Run the parser
            subprocess.run([python_executable, 'main.py'], check=True)
            
            # Return to original directory
            os.chdir(current_dir)
        except Exception as e:
            flash(f'Парсер Citilink завершился с ошибкой: {str(e)}', 'warning')
        
        # Read results
        try:
            with open(os.path.join(citilink_parser_dir, 'Товары.json'), 'r', encoding='utf-8') as f:
                content = f.read()
                # Handle potential JSON format issues
                if content.endswith(',\n]'):
                    content = content.replace(',\n]', '\n]')
                results = json.loads(content)
            
            flash(f'Парсер Citilink успешно выполнен. Получено {len(results)} товаров.', 'success')
        except Exception as f:
            flash(f'Ошибка при чтении результатов: {str(f)}', 'danger')
    except Exception as e:
        flash(f'Ошибка при запуске парсера Citilink: {str(e)}', 'danger')
    
    return redirect(url_for('admin.scrape'))

@admin_bp.route('/price-comparison', methods=['GET', 'POST'])
@login_required
@admin_required
def price_comparison():
    results = []
    sort_by = request.args.get('sort_by', 'price_diff')  # Default sorting by price difference
    
    if request.method == 'POST':
        category = request.form.get('category')
        sort_by = request.form.get('sort_by', sort_by)
        
        if category:
            try:
                from app.utils.price_comparison import run_price_comparison
                
                # Map category values to DNS category names
                dns_category_mapping = {
                    'videokarty': 'Видеокарты',
                    'protsessory': 'Процессоры',
                    'materinskie-platy': 'Материнские платы',
                    'operativnaya-pamyat': 'Оперативная память',
                    'bloki-pitaniya': 'Блоки питания',
                    'kulery': 'Кулеры',
                    'zhestkie-diski': 'Жесткие диски',
                    'ssd-nakopiteli': 'SSD накопители',
                    'korpusa': 'Корпуса'
                }
                
                # Get the corresponding DNS category name
                dns_category = dns_category_mapping.get(category)
                
                # Run price comparison with selected category for both stores
                results = run_price_comparison(category, dns_category)
                
                # Sort results based on user selection
                if results:
                    if sort_by == 'price_diff':
                        # Sort by absolute price difference (default)
                        results.sort(key=lambda x: abs(x['price_difference']), reverse=True)
                    elif sort_by == 'price_diff_percent':
                        # Sort by percentage price difference
                        results.sort(key=lambda x: abs(x['price_difference_percent']), reverse=True)
                    elif sort_by == 'lowest_price':
                        # Sort by lowest price (from either store)
                        results.sort(key=lambda x: min(x['citilink_price'], x['dns_price']))
                    elif sort_by == 'highest_price':
                        # Sort by highest price (from either store)
                        results.sort(key=lambda x: max(x['citilink_price'], x['dns_price']), reverse=True)
                    elif sort_by == 'rating':
                        # Sort by average rating if available
                        results.sort(key=lambda x: (x['citilink_rating'] + x['dns_rating'])/2 if x['citilink_rating'] and x['dns_rating'] else 0, reverse=True)
                    elif sort_by == 'similarity':
                        # Sort by match confidence/similarity score
                        results.sort(key=lambda x: x['similarity_score'], reverse=True)
                    
                    logger.info(f"Found {len(results)} matching products between Citilink and DNS. Sorted by: {sort_by}")
                    flash(f'Найдено {len(results)} товаров с разницей в цене', 'success')
                else:
                    logger.warning(f"No matching products found for category: {category}")
                    flash('Не найдено товаров с сопоставимыми ценами. Попробуйте другие категории или запустите парсеры заново.', 'warning')
            except Exception as e:
                logger.error(f'Ошибка при сравнении цен: {str(e)}')
                flash(f'Ошибка при сравнении цен: {str(e)}', 'danger')
        else:
            flash('Необходимо указать категорию товаров', 'danger')
    
    return render_template('admin/price_comparison.html', results=results, sort_by=sort_by)

@admin_bp.route('/dns-parser')
@login_required
@admin_required
def dns_parser_status():
    """Страница статуса парсера DNS"""
    # Проверяем, является ли пользователь админом
    if not current_user.is_admin():
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем статус парсера
    status = {}
    status_file = os.path.join(current_app.root_path, 'utils/DNS_parsing/parsing_status.json')
    
    if os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as f:
            try:
                status = json.load(f)
            except json.JSONDecodeError:
                status = {"error": "Invalid status file"}
    else:
        status = {"status": "Парсер еще не запускался"}
    
    # Форматируем даты для отображения
    if 'start_time' in status and status['start_time']:
        try:
            start_time = datetime.fromisoformat(status['start_time'])
            status['start_time_formatted'] = start_time.strftime('%d.%m.%Y %H:%M:%S')
        except:
            status['start_time_formatted'] = status['start_time']
    
    if 'last_updated' in status and status['last_updated']:
        try:
            last_updated = datetime.fromisoformat(status['last_updated'])
            status['last_updated_formatted'] = last_updated.strftime('%d.%m.%Y %H:%M:%S')
            
            # Вычисляем, сколько времени прошло с последнего обновления
            seconds_ago = (datetime.now() - last_updated).total_seconds()
            if seconds_ago < 60:
                status['last_updated_human'] = f"{int(seconds_ago)} сек. назад"
            elif seconds_ago < 3600:
                status['last_updated_human'] = f"{int(seconds_ago / 60)} мин. назад"
            else:
                status['last_updated_human'] = f"{int(seconds_ago / 3600)} ч. назад"
        except:
            status['last_updated_formatted'] = status['last_updated']
    
    return render_template('admin/dns_parser.html', status=status)

@admin_bp.route('/dns-parser/start', methods=['POST'])
@login_required
@admin_required
def start_dns_parser():
    """Запустить парсер DNS"""
    # Проверяем, является ли пользователь админом
    if not current_user.is_admin():
        return jsonify({"error": "У вас нет доступа к этой функции"}), 403
    
    try:
        # Получаем параметры из формы
        limit = int(request.form.get('limit', 5))
        continuous = request.form.get('continuous') == 'on'
        interval = int(request.form.get('interval', 24))
        
        # Добавляем путь к директории с парсером в sys.path
        parser_path = os.path.join(current_app.root_path, 'utils/DNS_parsing')
        if parser_path not in sys.path:
            sys.path.append(parser_path)
        
        # Запускаем парсер асинхронно
        result = dns_parser.start_parsing_async(
            limit_per_category=limit,
            continuous=continuous,
            interval_hours=interval
        )
        
        return jsonify({"success": True, "message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/dns-parser/status', methods=['GET'])
@login_required
@admin_required
def get_dns_parser_status():
    """Получить текущий статус парсера DNS в формате JSON"""
    # Проверяем, является ли пользователь админом
    if not current_user.is_admin():
        return jsonify({"error": "У вас нет доступа к этой функции"}), 403
    
    status_file = os.path.join(current_app.root_path, 'utils/DNS_parsing/parsing_status.json')
    
    if os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as f:
            try:
                status = json.load(f)
                
                # Добавляем время последнего обновления в формате для человека
                if 'last_updated' in status and status['last_updated']:
                    try:
                        last_updated = datetime.fromisoformat(status['last_updated'])
                        seconds_ago = (datetime.now() - last_updated).total_seconds()
                        if seconds_ago < 60:
                            status['last_updated_human'] = f"{int(seconds_ago)} сек. назад"
                        elif seconds_ago < 3600:
                            status['last_updated_human'] = f"{int(seconds_ago / 60)} мин. назад"
                        else:
                            status['last_updated_human'] = f"{int(seconds_ago / 3600)} ч. назад"
                    except:
                        pass
                
                return jsonify(status)
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid status file"}), 500
    else:
        return jsonify({"status": "Парсер еще не запускался"}), 404

@admin_bp.route('/view-logs')
@login_required
@admin_required
def view_logs():
    """API endpoint to retrieve log files content"""
    log_file = request.args.get('file', 'dns_parser.log')
    
    # Validate the log file name to prevent directory traversal
    allowed_logs = ['dns_parser.log', 'price_comparison.log', 'app/utils/Citi_parser/parser.log']
    if log_file not in allowed_logs:
        return jsonify({"error": "Invalid log file requested"}), 400
    
    # Получаем абсолютный путь к корневой директории проекта
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    # For app-relative paths
    if log_file.startswith('app/'):
        log_path = os.path.join(project_root, log_file)
    else:
        log_path = os.path.join(project_root, log_file)
    
    try:
        if os.path.exists(log_path):
            # Read last 100 lines to avoid massive responses
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_lines = lines[-100:] if len(lines) > 100 else lines
                content = ''.join(last_lines)
                
            return jsonify({"content": content})
        else:
            return jsonify({"content": f"Лог файл {log_file} не найден. Путь: {log_path}"})
    except Exception as e:
        return jsonify({"error": f"Ошибка чтения лог файла: {str(e)}"}), 500

@admin_bp.route('/clear-dns-parser-results')
@login_required
@admin_required
def clear_dns_parser_results():
    """Очистить результаты DNS парсера"""
    try:
        # Получаем путь к файлу с результатами
        dns_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'DNS_parsing')
        product_data_file = os.path.join(dns_parser_dir, 'product_data.json')
        urls_file = os.path.join(dns_parser_dir, 'urls.txt')
        
        # Очищаем файл с результатами
        if os.path.exists(product_data_file):
            with open(product_data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            logger.info("Файл с результатами DNS парсера очищен")
            
        # Очищаем файл с URL-адресами
        if os.path.exists(urls_file):
            with open(urls_file, 'w', encoding='utf-8') as f:
                f.write("")
            logger.info("Файл с URL-адресами DNS парсера очищен")
            
        flash('Результаты DNS парсера успешно очищены', 'success')
    except Exception as e:
        logger.error(f"Ошибка при очистке результатов DNS парсера: {e}")
        flash(f'Ошибка при очистке результатов: {str(e)}', 'danger')
        
    return redirect(url_for('admin.scrape'))

@admin_bp.route('/clear-citilink-parser-results')
@login_required
@admin_required
def clear_citilink_parser_results():
    """Очистить результаты Citilink парсера"""
    try:
        # Получаем путь к файлу с результатами
        citilink_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'Citi_parser')
        products_file = os.path.join(citilink_parser_dir, 'Товары.json')
        reviews_file = os.path.join(citilink_parser_dir, 'Отзывы.json')
        
        # Очищаем файлы с результатами
        if os.path.exists(products_file):
            with open(products_file, 'w', encoding='utf-8') as f:
                f.write("[]")
            logger.info("Файл с товарами Citilink парсера очищен")
            
        if os.path.exists(reviews_file):
            with open(reviews_file, 'w', encoding='utf-8') as f:
                f.write("[]")
            logger.info("Файл с отзывами Citilink парсера очищен")
            
        flash('Результаты Citilink парсера успешно очищены', 'success')
    except Exception as e:
        logger.error(f"Ошибка при очистке результатов Citilink парсера: {e}")
        flash(f'Ошибка при очистке результатов: {str(e)}', 'danger')
        
    return redirect(url_for('admin.scrape'))

@admin_bp.route('/run-all-parsers')
@login_required
@admin_required
def run_all_parsers():
    """Запустить оба парсера последовательно"""
    try:
        # Сначала запускаем парсер DNS
        dns_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'DNS_parsing')
        python_executable = sys.executable
        
        # Устанавливаем переменные окружения
        os.environ['MAX_ITEMS'] = '20'  # По умолчанию парсим 20 товаров
        
        # Запускаем DNS парсер
        logger.info("Запуск DNS парсера")
        current_dir = os.getcwd()
        os.chdir(dns_parser_dir)
        
        subprocess.run([python_executable, 'main.py'], check=True, cwd=dns_parser_dir)
        
        os.chdir(current_dir)
        
        # Затем запускаем парсер Citilink
        citilink_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'Citi_parser')
        
        # Создаем .env файл с категорией для Citilink парсера
        env_setup_cmd = f'Set-Content -Path "{os.path.join(citilink_parser_dir, ".env")}" -Value "CATEGORY=videokarty"'
        subprocess.run(['powershell', '-Command', env_setup_cmd], check=True)
        
        logger.info("Запуск Citilink парсера")
        os.chdir(citilink_parser_dir)
        
        subprocess.run([python_executable, 'main.py'], check=True, cwd=citilink_parser_dir)
        
        os.chdir(current_dir)
        
        flash('Оба парсера успешно выполнены', 'success')
    except Exception as e:
        logger.error(f"Ошибка при запуске парсеров: {e}")
        flash(f'Ошибка при запуске парсеров: {str(e)}', 'danger')
        
    return redirect(url_for('admin.scrape')) 