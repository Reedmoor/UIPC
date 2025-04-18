from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' или 'admin'
    
    configurations = db.relationship('Configuration', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

class Motherboard(db.Model):
    __tablename__ = 'motherboards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    form = db.Column(db.String(50), nullable=False)  # ATX, Micro-ATX и т.д.
    soket = db.Column(db.String(50), nullable=False)
    memory_type = db.Column(db.String(50), nullable=False)  # Тип оперативной памяти
    interface = db.Column(db.String(255), nullable=False)  # JSON или список интерфейсов

class PowerSupply(db.Model):
    __tablename__ = 'power_supplies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    power = db.Column(db.Integer, nullable=False)  # Мощность в ваттах
    type = db.Column(db.String(50), nullable=False)

class Processor(db.Model):
    __tablename__ = 'processors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    soket = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.Float, nullable=False)  # Частота в ГГц
    power_use = db.Column(db.Integer, nullable=False)  # Потребляемая мощность в ваттах

class GraphicsCard(db.Model):
    __tablename__ = 'graphics_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Float, nullable=False)  # Частота в МГц
    soket = db.Column(db.String(255), nullable=False)  # Список доступных разъемов
    power_use = db.Column(db.Integer, nullable=False)  # Потребляемая мощность в ваттах

class Cooler(db.Model):
    __tablename__ = 'coolers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Integer, nullable=False)  # Скорость вращения в об/мин
    power_use = db.Column(db.Integer, nullable=False)  # Потребляемая мощность в ваттах

class RAM(db.Model):
    __tablename__ = 'ram'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)  # Частота в МГц
    memory_type = db.Column(db.String(50), nullable=False)  # DDR4, DDR5 и т.д.
    power_use = db.Column(db.Integer, nullable=False)  # Потребляемая мощность в ваттах
    capacity = db.Column(db.Integer, nullable=False)  # Объем в ГБ

class HardDrive(db.Model):
    __tablename__ = 'hard_drives'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)  # Объем в ГБ
    recording = db.Column(db.Integer, nullable=False)  # Скорость записи в МБ/с
    reading = db.Column(db.Integer, nullable=False)  # Скорость чтения в МБ/с

class Case(db.Model):
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    form = db.Column(db.String(50), nullable=False)  # Размер корпуса

class Configuration(db.Model):
    __tablename__ = 'configurations'
    
    conf_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    motherboard_id = db.Column(db.Integer, db.ForeignKey('motherboards.id'), nullable=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('power_supplies.id'), nullable=True)
    cpu_id = db.Column(db.Integer, db.ForeignKey('processors.id'), nullable=True)
    gpu_id = db.Column(db.Integer, db.ForeignKey('graphics_cards.id'), nullable=True)
    cooler_id = db.Column(db.Integer, db.ForeignKey('coolers.id'), nullable=True)
    ram_id = db.Column(db.Integer, db.ForeignKey('ram.id'), nullable=True)
    hdd_id = db.Column(db.Integer, db.ForeignKey('hard_drives.id'), nullable=True)
    frame_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    
    motherboard = db.relationship('Motherboard', backref='configurations')
    power_supply = db.relationship('PowerSupply', backref='configurations')
    processor = db.relationship('Processor', backref='configurations')
    graphics_card = db.relationship('GraphicsCard', backref='configurations')
    cooler = db.relationship('Cooler', backref='configurations')
    ram = db.relationship('RAM', backref='configurations')
    hard_drive = db.relationship('HardDrive', backref='configurations')
    case = db.relationship('Case', backref='configurations')
    
    def total_price(self):
        """Рассчитывает общую стоимость конфигурации."""
        total = 0
        components = [
            self.motherboard, self.power_supply, self.processor, 
            self.graphics_card, self.cooler, self.ram, 
            self.hard_drive, self.case
        ]
        for component in components:
            if component:
                total += component.price
        return total
    
    def compatibility_check(self):
        """Проверяет совместимость компонентов."""
        issues = []
        
        # Проверка совместимости сокета процессора и материнской платы
        if self.processor and self.motherboard:
            if self.processor.soket != self.motherboard.soket:
                issues.append(f"Несовместимый сокет процессора ({self.processor.soket}) и материнской платы ({self.motherboard.soket})")
        
        # Проверка совместимости типа оперативной памяти и материнской платы
        if self.ram and self.motherboard:
            if self.ram.memory_type != self.motherboard.memory_type:
                issues.append(f"Несовместимый тип памяти ({self.ram.memory_type}) и материнской платы ({self.motherboard.memory_type})")
        
        # Проверка мощности блока питания
        if self.power_supply and (self.processor or self.graphics_card or self.cooler or self.ram):
            total_power = 0
            if self.processor:
                total_power += self.processor.power_use
            if self.graphics_card:
                total_power += self.graphics_card.power_use
            if self.cooler:
                total_power += self.cooler.power_use
            if self.ram:
                total_power += self.ram.power_use
            
            if total_power > (self.power_supply.power * 0.8):  # 80% рекомендуемая загрузка БП
                issues.append(f"Недостаточная мощность блока питания ({self.power_supply.power}Вт) для данной конфигурации (требуется ~{total_power}Вт)")
        
        # Проверка совместимости форм-фактора материнской платы и корпуса
        if self.motherboard and self.case:
            # Упрощенная проверка - в реальности нужна более детальная логика
            if self.motherboard.form not in self.case.form:
                issues.append(f"Форм-фактор материнской платы ({self.motherboard.form}) не поддерживается корпусом ({self.case.form})")
        
        return issues