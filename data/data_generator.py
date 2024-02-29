from faker import Faker
from data.model import EntityAdd


def generate_data() -> EntityAdd:
    fake = Faker()
    return EntityAdd(custom_properties={
        "addition": {
            "additional_info": fake.text(),  # Генерируем случайный текст
            "additional_number": fake.random_int(min=0, max=9999)  # Генерируем случайное число
        },
        "important_numbers": [fake.random_int(min=0, max=99) for _ in range(fake.random_int(min=1, max=99))],
        "title": fake.sentence(),  # Генерируем случайное предложение
        "verified": fake.boolean()  # Генерируем случайное булево значение
    })
