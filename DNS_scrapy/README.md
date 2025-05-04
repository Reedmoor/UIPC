# DNS Scrapy Parser

Парсер для сайта DNS-Shop, созданный с использованием фреймворка Scrapy.

## Требования

- Python 3.8 или новее
- Scrapy 2.8.0 или новее
- itemadapter

## Установка

```bash
pip install scrapy itemadapter
```

## Структура проекта

```
DNS_scrapy/
├── DNS/                 # Основной пакет Scrapy проекта
│   ├── spiders/         # Директория с пауками
│   │   ├── __init__.py
│   │   └── dns_products.py  # Основной паук для парсинга товаров
│   ├── __init__.py
│   ├── items.py         # Определение структуры данных
│   ├── middlewares.py   # Middlewares для Scrapy
│   ├── pipelines.py     # Pipelines для обработки и сохранения данных
│   └── settings.py      # Настройки Scrapy проекта
├── categories.json      # JSON файл с категориями для парсинга
├── main.py              # Основной скрипт для запуска парсера
├── run.py               # Утилита для запуска паука
└── scrapy.cfg           # Конфигурационный файл Scrapy
```

## Использование

### Параметры запуска

- `CATEGORY` - название или часть URL категории для парсинга (опционально)
- `MAX_ITEMS` - максимальное количество товаров для сбора (по умолчанию 50)

### Запуск через main.py

```bash
CATEGORY=videokarty MAX_ITEMS=100 python main.py
```

### Запуск через run.py (с параметрами)

```bash
python run.py videokarty 100
```

### Запуск через Scrapy напрямую

```bash
scrapy crawl dns_products -a category=videokarty -a max_items=100
```

## Категории товаров

Категории определяются в файле `categories.json`. Если нужно добавить новую категорию, просто добавьте запись в этот файл в формате:

```json
{
  "name": "Имя категории",
  "url": "/catalog/ID_категории/название-категории/",
  "id": "ID_категории"
}
```

## Выходные данные

Данные сохраняются в файл `items.json` в корне проекта в следующем формате:

```json
[
  {
    "name": "Название товара",
    "url": "URL товара",
    "product_id": "ID товара",
    "category": "Категория",
    "price_original": 10000,
    "price_discounted": 9000,
    "availability": "In Stock",
    "rating": 4.5,
    "review_count": 120,
    "image_url": "URL изображения",
    "brand": "Бренд",
    "specifications": {
      "Спецификация 1": "Значение 1",
      "Спецификация 2": "Значение 2"
    },
    "description": "Описание товара",
    "date_scraped": "2023-10-15T12:30:45.123456"
  },
  // ... другие товары
]
``` 