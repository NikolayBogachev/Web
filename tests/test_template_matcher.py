import pytest
from app.utils import find_best_matching_template

# Мокируем функцию get_all для тестов
@pytest.fixture
def mock_get_all(mocker):
    templates = [
        {
            "name": "template_1",
            "fields": {
                "name": "string",
                "age": "integer"
            }
        },
        {
            "name": "template_2",
            "fields": {
                "email": "string",
                "country": "string"
            }
        },
        {
            "name": "template_3",
            "fields": {
                "city": "string"
            }
        }
    ]

    mocker.patch('app.utils.get_all', return_value=templates)

# Тест на нахождение лучшего совпадения шаблона (асинхронный тест)
@pytest.mark.asyncio
async def test_find_matching_template(mock_get_all):
    params_set = {"name:string", "age:integer"}
    best_template = await find_best_matching_template(params_set)

    assert best_template is not None
    assert best_template["name"] == "template_1"

# Тест на отсутствие подходящих шаблонов
@pytest.mark.asyncio
async def test_no_matching_template(mock_get_all):
    params_set = {"salary:integer", "position:string"}
    best_template = await find_best_matching_template(params_set)

    assert best_template is None

# Тест, где есть несколько совпадений, но нужно выбрать лучшее
@pytest.mark.asyncio
async def test_multiple_matching_templates(mock_get_all):
    params_set = {"email:string", "country:string"}
    best_template = await find_best_matching_template(params_set)

    assert best_template is not None
    assert best_template["name"] == "template_2"

# Тест, когда нет ни одного шаблона
@pytest.mark.asyncio
async def test_empty_templates(mocker):
    mocker.patch('app.utils.get_all', return_value=[])

    params_set = {"name:string"}
    best_template = await find_best_matching_template(params_set)

    assert best_template is None
