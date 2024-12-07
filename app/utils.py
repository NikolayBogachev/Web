import re
from datetime import datetime


# Валидация поля и определение его типа
def identify_field_type(value):

    DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d")

    # Проверка даты (формат DD.MM.YYYY или YYYY-MM-DD)
    for date_format in DATE_FORMATS:
        try:
            datetime.strptime(value, date_format)
            return "date"
        except ValueError:
            pass

    # Проверка телефона (формат +7 XXX XXX XX XX)
    if re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return "phone"

    # Проверка email
    elif re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        return "email"

    return "text"



