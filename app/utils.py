import re
from datetime import datetime


# Валидация поля и определение его типа
def identify_field_type(value):
    print(value)
    # Проверка email
    if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        return "email"

    # Проверка телефона (формат +7 XXX XXX XX XX)
    elif re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return "phone"

    # Проверка даты (формат DD.MM.YYYY или YYYY-MM-DD)
    else:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return "date"
        except ValueError:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return "date"
            except ValueError:
                return "text"


# Валидация всех полей формы
# def validate_fields(data, template_fields):
#     match_count = 0  # Считаем количество совпадений
#
#     # Проверяем каждый шаблон
#     for field_name, field_type in template_fields.items():
#         if identify_field_type(data[field_name]) == field_type:
#             match_count += 1
#
#     return match_count