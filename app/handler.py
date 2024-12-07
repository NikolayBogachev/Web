from fastapi import APIRouter, Request
from utils import identify_field_type, find_best_matching_template

router = APIRouter()


@router.post("/get_form", response_model=None)
async def get_form(request: Request):
    # Преобразуем параметры запроса в множество с форматированием "поле:тип"
    params_set = {f"{key}:{identify_field_type(value)}" for key, value in request.query_params.items()}

    matched_template = await find_best_matching_template(params_set)

    if matched_template:
        return {"template_name": matched_template["name"]}

    return {key: identify_field_type(value) for key, value in request.query_params.items()}

