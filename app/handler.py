from fastapi import APIRouter, Request
from app.utils import identify_field_type
from app.db import get_all

router = APIRouter()


@router.post("/get_form", response_model=None)
async def get_form(request: Request):
    # Преобразуем параметры запроса в множество с форматированием "поле:тип"
    params_set = {f"{key}:{identify_field_type(value)}" for key, value in request.query_params.items()}

    matched_template = None
    max_matched_fields_count = 0

    templates = get_all()

    for template in templates:
        # Преобразуем шаблонные поля в множество с таким же форматированием
        template_set = {f"{field_name}:{field_type}" for field_name, field_type in template["fields"].items()}

        # Находим пересечение множеств
        matched_fields_count = len(params_set & template_set)

        # Проверяем на полное совпадение с текущим шаблоном
        if matched_fields_count == len(template_set) and matched_fields_count > max_matched_fields_count:
            matched_template = template
            max_matched_fields_count = matched_fields_count

    # Возвращаем имя подходящего шаблона, если найден
    if matched_template is not None:
        return {"template_name": matched_template["name"]}

    # Если подходящего шаблона нет, возвращаем описание полученных параметров
    return {key: identify_field_type(value) for key, value in request.query_params.items()}
