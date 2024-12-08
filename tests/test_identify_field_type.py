import pytest

from app.utils import identify_field_type

# Импортируем функцию для тестирования
DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d")


# Тестовые случаи
@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        # Тесты на даты
        ("12.04.2023", "date"),  # Формат DD.MM.YYYY
        ("2023-04-12", "date"),  # Формат YYYY-MM-DD
        ("31.12.1999", "date"),  # Граничный случай
        ("1999-12-31", "date"),  # Граничный случай
        ("12.04.23", "text"),    # Некорректный формат даты
        ("2023/04/12", "text"),  # Некорректный формат даты

        # Тесты на телефон
        ("+7 123 456 78 90", "phone"),  # Корректный формат
        ("+7 987 654 32 10", "phone"),  # Другой корректный пример
        ("7 123 456 78 90", "text"),    # Пропущен "+"
        ("+71234567890", "text"),       # Нет пробелов

        # Тесты на email
        ("example@example.com", "email"),  # Корректный email
        ("user.name+tag+sorting@example.com", "email"),  # Допустимый формат
        ("invalidemail.com", "text"),      # Отсутствует '@'
        ("@nouser.com", "text"),           # Отсутствует локальная часть
        ("user@.com", "text"),             # Некорректный домен

        # Тесты на текст
        ("hello world", "text"),           # Простой текст
        ("12345", "text"),                 # Число в виде текста
        ("", "text"),                      # Пустая строка
        ("!@#$%^&*()", "text"),            # Специальные символы
    ]
)
def test_identify_field_type(input_value, expected_output):
    assert identify_field_type(input_value) == expected_output
