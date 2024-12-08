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


# Тест нахождения "Complete Form" при полном совпадении.
@pytest.mark.asyncio
async def test_find_complete_form(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "birth_date": "1990-01-01",
        "message": "Hello, world!"
    }

    # Создаём мокированный запрос
    request = Request(scope={
        "type": "http",
        "method": "POST",
        "query_string": b"user_email=test@example.com&user_phone=+7+123+456+78+90&birth_date=1990-01-01&message=Hello,+world!",
        "headers": []
    })
    request._query_params = QueryParams(query_params)
    # Тестируем функцию
    matched_template = await find_best_matching_template(request)

    assert matched_template is not None
    assert matched_template.get("name") == "Complete Form"


# Тест нахождения "Registration Form", если параметры запроса совпадают с шаблоном.
@pytest.mark.asyncio
async def test_find_registration_form(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "birth_date": "1990-01-01"
    }

    request = Request(scope={
        "type": "http",
        "method": "GET",
        "query_string": b"user_email=test@example.com&user_phone=+7+123+456+78+90&birth_date=1990-01-01",
        "headers": []
    })
    request._query_params = QueryParams(query_params)
    matched_template = await find_best_matching_template(request)

    assert matched_template is not None
    assert matched_template.get("name") == "Registration Form"


# Тест нахождения "Order Form", даже если есть дополнительные поля.
@pytest.mark.asyncio
async def test_find_order_form_with_extra_fields(mock_get_all):
    query_params = {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "extra_field": "extra_value"
    }

    request = Request(scope={
        "type": "http",
        "method": "GET",
        "query_string": b"user_email=test@example.com&user_phone=+7+123+456+78+90&extra_field=extra_value",
        "headers": []
    })
    request._query_params = QueryParams(query_params)
    matched_template = await find_best_matching_template(request)
    assert matched_template is not None
    assert matched_template.get("name") == "Order Form"


# Тест, когда недостаточно совпадений для выбора шаблона.
@pytest.mark.asyncio
async def test_no_matching_form(mock_get_all):
    query_params = {
        "unknown_field": "unknown_value"
    }

    request = Request(scope={
        "type": "http",
        "method": "GET",
        "query_string": b"unknown_field=unknown_value",
        "headers": []
    })
    request._query_params = QueryParams(query_params)
    matched_template = await find_best_matching_template(request)
    assert matched_template is None

