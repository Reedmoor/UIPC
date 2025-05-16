from app import create_app, db
from sqlalchemy import text

# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def debug_database_url():
    """Debugging функция для анализа строки подключения к БД"""
    # Загружаем переменные окружения
    load_dotenv()

    # Получаем URL базы данных
    database_url = os.getenv('DATABASE_URL')
    print(f"Длина строки URL: {len(database_url)}")

    # Печатаем каждый символ и его код
    print("Анализ символов в строке подключения:")
    for i, char in enumerate(database_url):
        code = ord(char)
        char_display = char if code >= 32 and code <= 126 else '?'
        print(f"Позиция {i}: '{char_display}' (код: {code} / hex: {hex(code)})")

    # Проверяем конкретную позицию с ошибкой
    if len(database_url) > 61:
        problem_char = database_url[61]
        code = ord(problem_char)
        print(f"\nПроблемный символ в позиции 61: '{problem_char}' (код: {code} / hex: {hex(code)})")

    # Создаем очищенную строку
    clean_url = ''.join(c for c in database_url if ord(c) < 128)
    print(f"\nОчищенная строка URL: {clean_url}")

    return clean_url


def test_connection_with_clean_url():
    """Тестирует подключение с очищенной строкой URL"""
    clean_url = debug_database_url()

    try:
        # Создаем движок с очищенной строкой
        engine = create_engine(clean_url)

        # Пробуем подключиться
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            print(f"\nПодключение успешно! Результат запроса: {result}")
            return True
    except Exception as e:
        print(f"\nОшибка подключения: {e}")
        return False


if __name__ == "__main__":
    test_connection_with_clean_url()