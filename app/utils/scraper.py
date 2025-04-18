import requests
from bs4 import BeautifulSoup
import re
from app import db
from app.models.models import (
    Motherboard, PowerSupply, Processor, GraphicsCard, 
    Cooler, RAM, HardDrive, Case
)

def scrape_components(url, component_type):
    """
    Парсит комплектующие с указанного URL.
    
    Args:
        url (str): URL страницы для парсинга
        component_type (str): Тип компонента ('motherboard', 'power_supply', и т.д.)
        
    Returns:
        list: Список добавленных компонентов
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Здесь будет специфичный для сайта парсинг
        # Ниже - упрощенный пример логики парсинга
        
        component_data = []
        
        # Пример: Парсинг карточек товаров
        product_cards = soup.select('.product-card')  # CSS-селектор для карточек товаров (адаптировать под целевой сайт)
        
        for card in product_cards:
            name = card.select_one('.product-name').text.strip()
            price_text = card.select_one('.product-price').text.strip()
            price = float(re.sub(r'[^\d.]', '', price_text))
            
            # Дополнительные характеристики (зависят от типа компонента)
            specs = {}
            spec_items = card.select('.product-spec-item')
            for item in spec_items:
                key = item.select_one('.spec-name').text.strip().lower()
                value = item.select_one('.spec-value').text.strip()
                specs[key] = value
            
            component = create_component(component_type, name, price, specs)
            if component:
                component_data.append(component)
        
        return component_data
        
    except Exception as e:
        print(f"Ошибка при парсинге: {str(e)}")
        raise

def create_component(component_type, name, price, specs):
    """
    Создает и сохраняет компонент в базе данных на основе типа и характеристик.
    
    Args:
        component_type (str): Тип компонента
        name (str): Название компонента
        price (float): Цена компонента
        specs (dict): Словарь с характеристиками компонента
        
    Returns:
        object: Созданный объект компонента
    """
    try:
        component = None
        
        if component_type == 'motherboard':
            component = Motherboard(
                name=name,
                price=price,
                form=specs.get('form', 'ATX'),
                soket=specs.get('soket', 'AM4'),  # Значение по умолчанию
                type_member=specs.get('type_member', 'DDR4'),
                interface=specs.get('interface', 'PCIe 3.0')
            )
        
        elif component_type == 'power_supply':
            component = PowerSupply(
                name=name,
                price=price,
                power=int(specs.get('power', 500)),
                type=specs.get('type', 'ATX')
            )
        
        elif component_type == 'processor':
            component = Processor(
                name=name,
                price=price,
                soket=specs.get('soket', 'AM4'),
                frequancy=float(specs.get('frequancy', 3.5)),
                power_use=int(specs.get('power_use', 65))
            )
        
        elif component_type == 'graphics_card':
            component = GraphicsCard(
                name=name,
                price=price,
                frequancy=float(specs.get('frequancy', 1500)),
                soket=specs.get('soket', 'PCIe 3.0'),
                power_use=int(specs.get('power_use', 150))
            )
        
        elif component_type == 'cooler':
            component = Cooler(
                name=name,
                price=price,
                speed=int(specs.get('speed', 1500)),
                power_use=int(specs.get('power_use', 5))
            )
        
        elif component_type == 'ram':
            component = RAM(
                name=name,
                price=price,
                frequancy=int(specs.get('frequancy', 3200)),
                type_member=specs.get('type_member', 'DDR4'),
                power_use=int(specs.get('power_use', 10))
            )
        
        elif component_type == 'hard_drive':
            component = HardDrive(
                name=name,
                price=price,
                capacity=int(specs.get('capacity', 1000)),
                recording=int(specs.get('recording', 150)),
                reading=int(specs.get('reading', 200))
            )
        
        elif component_type == 'case':
            component = Case(
                name=name,
                price=price,
                form=specs.get('form', 'ATX, Micro-ATX')
            )
        
        if component:
            db.session.add(component)
            db.session.commit()
            return component
        
        return None
    
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при создании компонента: {str(e)}")
        return None 