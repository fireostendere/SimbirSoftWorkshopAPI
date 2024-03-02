import allure
import pytest
import random

from data.data_generator import generate_data
from data.model import EntityResponse


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Добавление новой сущности")
@allure.description("""
Цель: Проверить добавление новой сущности

Шаги:
1. Создать новую сущность
2. Получить список всех сущностей
3. Проверить, что новая сущность присутствует в списке

Ожидаемый результат:
- Новая сущность присутствует в списке
""")
@pytest.mark.parametrize("iteration", range(1))  # Параметризация для повторения теста
def test_add_new_entity(test_service_lib, iteration):
    with allure.step('Создать новую сущность'):
        user_data = generate_data()
        created_entity = test_service_lib.create_entity(user_data)

    with allure.step('Получить список всех сущностей'):
        entities_response = test_service_lib.get_all()

    with allure.step('Проверить, что новая сущность присутствует в списке'):
        assert any(entity.id == created_entity.id for
                   entity in entities_response.entity), "Созданная сущность не найдена в списке"


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Изменение сущности по ID")
@allure.description("""
Цель: Проверить изменение сущности по ID

Шаги:
1. Получить все сущности
2. Выбрать случайную сущность из списка
3. Сгенерировать новые данные для сущности
4. Обновить сущность новыми данными
5. Получить обновленную сущность

Ожидаемый результат:
- Данные сущности были обновлены
""")
def test_patch_entity_by_id(test_service_lib, ensure_entities_exist):
    with allure.step('Получить все сущности'):
        entities_response = test_service_lib.get_all()

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)

    with allure.step('Сгенерировать новые данные для сущности'):
        user_data = generate_data()

    with allure.step('Обновить сущность новыми данными'):
        test_service_lib.patch_entity_by_id(str(entity.id), user_data)

    with allure.step('Получить обновленную сущность'):
        updated_entity = test_service_lib.get_entity_by_id(str(entity.id))

    with allure.step("Проверить, что данные сущности были обновлены"):
        expected_entity_data = EntityResponse.model_validate({**user_data.model_dump(),
                                                              "id": updated_entity.id, "addition": {
                "id": updated_entity.addition.id, **user_data.addition.model_dump()}})
        assert updated_entity == expected_entity_data, "Данные не были обновлены"


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Получение сущности по ID")
@allure.description("""
Цель: Проверить получение сущности по ID

Шаги:
1. Создать новую сущность
2. Получить ID созданной сущности
3. Получить сущность по ID

Ожидаемый результат:
- Проверить что по ID получена правильная сущность
""")
def test_get_entity_by_id(test_service_lib):
    with allure.step('Создать новую сущность'):
        user_data = generate_data()
        created_entity = test_service_lib.create_entity(user_data)

    with allure.step('Получить сущность по ID'):
        fetched_entity = test_service_lib.get_entity_by_id(str(created_entity.id))

    with allure.step("Проверить, что полученная сущность имеет правильные данные"):
        assert fetched_entity == created_entity, "Полученная сущность имеет неверные данные"


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Получение списка сущностей")
@allure.description("""
Цель: Проверить получение списка сущностей

Шаги:
1. Получить все сущности

Ожидаемый результат:
- Получен список сущностей
""")
def test_get_all_entity(test_service_lib, ensure_entities_exist):
    with allure.step('Создать новую сущность'):
        user_data = generate_data()
        created_entity = test_service_lib.create_entity(user_data)

    with allure.step('Получить все сущности'):
        response = test_service_lib.get_all()
        entities = [EntityResponse(**entity_data.model_dump()) for entity_data in response.entity]

    with allure.step("Проверить, что ответ содержит созданную сущность"):
        assert any(entity.id == created_entity.id for entity in entities), "Созданная сущность не найдена в списке"


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Удаление сущности по ID")
@allure.description("""
Цель: Проверить удаление сущности по ID

Шаги:
1. Получить все сущности
2. Выбрать случайную сущность из списка
3. Удалить сущность по ID
4. Получить все сущности после удаления

Ожидаемый результат:
- Сущность больше не присутствует в списке
""")
@pytest.mark.parametrize("iteration", range(1))  # Параметризация для повторения теста
def test_del_entity_by_id(test_service_lib, ensure_entities_exist, iteration):
    with allure.step('Получить все сущности'):
        entities_response = test_service_lib.get_all()

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)
    with allure.step('Удалить сущность по ID'):
        test_service_lib.delete_entity_by_id(str(entity.id))

    with allure.step('Получить все сущности после удаления'):
        entities_after_deletion = test_service_lib.get_all()

        with allure.step("Проверить, что удаленная сущность больше не присутствует в списке"):
            assert entity not in entities_after_deletion.entity, "Удаленная сущность все еще присутствует в списке"
