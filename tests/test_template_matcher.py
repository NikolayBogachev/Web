import pytest
from fastapi import Request
from httpx import QueryParams

from app.db import get_all
from app.utils import find_best_matching_template


@pytest.fixture
def mock_get_all(mocker):
    templates = [
        {
            "name": "Complete Form",
            "fields": {
                "user_email": "email",
                "user_phone": "phone",
                "birth_date": "date",
                "message": "text"
            }
        },
        {
            "name": "Registration Form",
            "fields": {
                "user_email": "email",
                "user_phone": "phone",
                "birth_date": "date"
            }
        },
        {
            "name": "Order Form",
            "fields": {
                "user_email": "email",
                "user_phone": "phone"
            }
        }
    ]

    mocker.patch('app.db.get_all', return_value=templates)


@pytest.mark.asyncio
async def test_find_complete_form(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "birth_date": "1990-01-01",
        "message": "Hello, world!"
    }

    # Преобразуем словарь query_params в список кортежей (ключ, значение)
    params_list = list(query_params.items())

    # Передаём params_list в функцию find_best_matching_template
    matched_template = await find_best_matching_template(params_list)

    assert matched_template is not None
    assert matched_template.get("name") == "Complete Form"


@pytest.mark.asyncio
async def test_find_registration_form(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "birth_date": "1990-01-01"
    }

    params_list = list(query_params.items())

    matched_template = await find_best_matching_template(params_list)

    assert matched_template is not None
    assert matched_template.get("name") == "Registration Form"


@pytest.mark.asyncio
async def test_find_order_form_with_extra_fields(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "extra_field": "extra_value"
    }

    params_list = list(query_params.items())

    matched_template = await find_best_matching_template(params_list)

    assert matched_template is not None
    assert matched_template.get("name") == "Order Form"


@pytest.mark.asyncio
async def test_no_matching_form(mock_get_all):
    query_params = {
        "unknown_field": "unknown_value"
    }

    params_list = list(query_params.items())

    matched_template = await find_best_matching_template(params_list)

    assert matched_template is None

