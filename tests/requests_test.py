import aiohttp
import asyncio
import argparse

# Список тестовых данных
test_requests = [
    # Полный набор полей для "Complete Form"
    {
        "user_email": "test@example.com",
        "user_phone": "+7 123 456 78 90",
        "birth_date": "1990-01-01",
        "message": "This is a complete test message."
    },
    # Поля для "Registration Form"
    {
        "user_email": "user@example.com",
        "user_phone": "+7 987 654 32 10",
        "birth_date": "2000-12-25"
    },
    # Поля для "Order Form"
    {
        "user_email": "order@example.com",
        "user_phone": "+7 111 222 33 44"
    },
    # Только текстовые поля (должен не подходить ни к одному шаблону)
    {
        "message": "Hello, how are you?",
        "additional_field1": "This is another text field.",
        "additional_field2": "Yet another field with text."
    },
    # Только email (должен не подходить ни к одному шаблону)
    {
        "user_email": "single@example.com"
    },
    # Только телефонные номера (должен не подходить ни к одному шаблону)
    {
        "user_phone1": "+1 800 555 0199",
        "user_phone2": "+44 20 7946 0958",
        "user_phone3": "+91 98765 43210"
    },
    # Смешанные данные, но с отсутствующими обязательными полями
    {
        "user_phone": "+7 555 123 4567",
        "additional_field": "random text message"
    },
    # Данные, которые не подходят ни к одному шаблону
    {
        "random_field1": "invalid_field",
        "random_field2": "another_invalid_field"
    },
    # Минимальные совпадения с шаблоном (неполный "Complete Form")
    {
        "user_email": "test@example.com",
        "user_phone": "+7 999 888 77 66",
        "birth_date": "Invalid date",
        "message": "Random text"
    },
    # Все поля, но с некорректными значениями
    {
        "user_email": "not_an_email",
        "user_phone": "not_a_phone",
        "birth_date": "not_a_date",
        "message": "Some invalid text"
    }
]


async def send_requests(base_url):
    async with aiohttp.ClientSession() as session:
        for i, params in enumerate(test_requests, 1):
            print(f"Sending request {i}: {params}")
            async with session.post(base_url, params=params) as response:
                try:
                    response_data = await response.json()
                    print(f"Response {i}: {response_data}")
                except aiohttp.ContentTypeError:
                    text_data = await response.text()
                    print(f"Response {i} (non-JSON): {text_data}")
                print("-" * 80)


def main():
    parser = argparse.ArgumentParser(description="Send test requests to a server.")
    parser.add_argument("--url", type=str, default="http://localhost:8000/get_form",
                        help="URL to send POST requests to (default: http://localhost:8000/get_form)")

    args = parser.parse_args()

    asyncio.run(send_requests(args.url))


if __name__ == "__main__":
    main()
