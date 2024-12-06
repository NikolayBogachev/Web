from fastapi import APIRouter, Request
from utils import identify_field_type
from db import get_all

router = APIRouter()


@router.post("/get_form", response_model=None)
async def get_form(request: Request):
    query_params = dict(request.query_params)

    templates = get_all()

    best_match_template = None
    max_matches = 0
    input_field_types = {key: identify_field_type(value) for key, value in query_params.items()}
    print(input_field_types)
    best_match_template = None
    best_match_score = -1  # Оценка для выбора лучшего шаблона

    for template in templates:
        template_field_types = template["fields"]

        # Сравниваем входные данные с шаблоном
        exact_matches = 0
        missing_fields = 0
        extra_fields = 0

        # Проверка совпадающих и отсутствующих полей
        for field_name, field_type in template_field_types.items():
            if field_type in input_field_types.values():
                exact_matches += 1
            else:
                missing_fields += 1

        # Поля, которых нет в шаблоне, но есть во входных данных
        for field_name, field_type in input_field_types.items():
            if field_type not in template_field_types.values():
                extra_fields += 1

        # Оценка: больше совпадений и меньше расхождений -> лучше
        match_score = exact_matches - (missing_fields + extra_fields)

        # Выбираем лучший шаблон по максимальной оценке
        if match_score > best_match_score:
            best_match_score = match_score
            best_match_template = template

    if best_match_template:
        return {"template_name": best_match_template["name"]}

    return {field_name: field_type for field_name, field_type in input_field_types.items()}