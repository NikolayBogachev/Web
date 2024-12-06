import aiohttp
import asyncio

# URL приложения
base_url = "http://localhost:8000/get_form"

# Список тестовых данных
test_requests = [
    # Полный набор полей для "Complete Form"
    {
        "f_name1": "test@example.com",
        "f_name2": "+7 123 456 78 90",
        "f_name3": "1990-01-01",
        "f_name4": "This is a complete test message."
    },
    # Поля для "Registration Form"
    {
        "f_name1": "user@example.com",
        "f_name2": "+7 987 654 32 10",
        "f_name3": "2000-12-25"
    },
    # Поля для "Order Form"
    {
        "f_name1": "order@example.com",
        "f_name2": "+7 111 222 33 44"
    },
    # Только текстовые поля
    {
        "f_name1": "Hello, how are you?",
        "f_name2": "This is another text field.",
        "f_name3": "Yet another field with text."
    },
    # Только email
    {
        "f_name1": "single@example.com"
    },
    # Только телефонные номера
    {
        "f_name1": "+1 800 555 0199",
        "f_name2": "+44 20 7946 0958",
        "f_name3": "+91 98765 43210"
    },
    # Смешанные данные, но с отсутствующими обязательными полями
    {
        "f_name1": "+7 555 123 4567",
        "f_name2": "random text message"
    },
    # Данные, которые не подходят ни к одному шаблону
    {
        "f_name1": "invalid_field",
        "f_name2": "another_invalid_field"
    },
    # Минимальные совпадения с шаблоном
    {
        "f_name1": "test@example.com",
        "f_name2": "+7 999 888 77 66",
        "f_name3": "Invalid date",
        "f_name4": "Random text"
    },
    # Все поля, но с некорректными значениями
    {
        "f_name1": "not_an_email",
        "f_name2": "not_a_phone",
        "f_name3": "not_a_date",
        "f_name4": "Some invalid text"
    }
]


# Асинхронная функция для отправки запросов
async def send_requests():
    async with aiohttp.ClientSession() as session:
        for i, params in enumerate(test_requests, 1):
            print(f"Sending request {i}: {params}")
            async with session.post(base_url, params=params) as response:
                response_data = await response.json()
                print(f"Response {i}: {response_data}")
                print("-" * 80)

# Запуск тестирования
asyncio.run(send_requests())
