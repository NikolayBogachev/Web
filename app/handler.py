from fastapi import APIRouter, Request
from utils import identify_field_type, find_best_matching_template

router = APIRouter()


@router.post("/get_form", response_model=None)
async def get_form(request: Request):
    """
        Обрабатывает POST-запрос на поиск соответствующего шаблона или возвращает типы переданных параметров.

        :param request: Объект запроса FastAPI, содержащий параметры запроса.
        :return: Словарь с именем шаблона, если найден, или словарь с определенными типами для каждого параметра.
    """

    matched_template = await find_best_matching_template(request)

    if matched_template:
        return {"template_name": matched_template["name"]}

    return {key: identify_field_type(value) for key, value in request.query_params.items()}

