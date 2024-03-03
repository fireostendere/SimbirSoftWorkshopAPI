from faker import Faker
from data.model import EntityRequest, AdditionRequest


def generate_entity_creation_data(min_number=0, max_number=9999, min_list_size=1, max_list_size=99) -> EntityRequest:
    fake = Faker()
    return EntityRequest(
        addition=AdditionRequest(
            additional_info=fake.text(),  # Генерируем случайный текст
            additional_number=fake.random_int(min=min_number, max=max_number)  # Генерируем случайное число
        ),
        important_numbers=[fake.random_int(min=0, max=99) for _ in range(fake.random_int(min=min_list_size, max=max_list_size))],
        title=fake.sentence(),  # Генерируем случайное предложение
        verified=fake.boolean()  # Генерируем случайное булево значение
    )