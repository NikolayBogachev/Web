import re
from datetime import datetime
from typing import Optional, Dict, Any, Literal
from app.db import get_all

DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d")


def identify_field_type(value) -> Literal["date", "phone", "email", "text"]:
    """
        Определяет тип переданного значения.

        :param value: Строка для анализа
        :return: Один из типов: "date", "phone", "email" или "text"
    """

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
    if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        return "email"

    return "text"


async def find_best_matching_template(request) -> Optional[Dict[str, Any]]:
    """
        Находит шаблон, который наиболее соответствует параметрам запроса.

        :param request: Объект запроса FastAPI
        :return: Шаблон, соответствующий запросу, или None, если подходящий шаблон не найден
    """

    # Преобразуем параметры запроса в множество с форматированием "поле:тип"
    params_set = {f"{key}:{identify_field_type(value)}" for key, value in request.query_params.items()}
    templates = get_all()

    matched_template = None
    max_matched_fields_count = 0

    for template in templates:
        template_set = {f"{field_name}:{field_type}" for field_name, field_type in template["fields"].items()}
        matched_fields_count = len(params_set & template_set)

        if matched_fields_count == len(template_set) and matched_fields_count > max_matched_fields_count:
            matched_template = template
            max_matched_fields_count = matched_fields_count

    return matched_template
