import allure
import pytest
import random

from data.data_generator import generate_data
from data.model import Entity
from lib.test_service_lib import get_entity_by_id, get_all, delete_entity_by_id, create_entity, patch_entity_by_id


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Добавление новой сущности")
@allure.description("""
Цель: Проверить добавление новой сущности

Шаги:
1. Создать новую сущность
2. Получить ID созданной сущности
3. Получить список сущностей

Ожидаемый результат:
- Новая сущность присутствует в списке
""")
@pytest.mark.parametrize("iteration", range(1))  # Параметризация для повторения теста, удобно
# использовать для заполнения базы
def test_add_new_entity(test_service_api, iteration):
    with allure.step('Создать новую сущность'):
        user_data = generate_data()
        created_entity = create_entity(test_service_api, user_data)

    with allure.step('Проверить, что сущность была создана'):
        fetched_entity = get_entity_by_id(test_service_api, str(created_entity.id))
        assert fetched_entity.model_dump() == created_entity.model_dump(), "Созданная сущность не найдена"


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
@pytest.mark.usefixtures('ensure_entities_exist')
def test_patch_entity_by_id(test_service_api):
    with allure.step('Получить все сущности'):
        entities_response = get_all(test_service_api)

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)

    with allure.step('Сгенерировать новые данные для сущности'):
        user_data = generate_data()

    with allure.step('Обновить сущность новыми данными'):
        patch_entity_by_id(test_service_api, str(entity.id), user_data)

    with allure.step('Получить обновленную сущность'):
        updated_entity = get_entity_by_id(test_service_api, str(entity.id))

    with allure.step("Проверить, что данные сущности были обновлены"):
        updated_entity_model_dump = updated_entity.model_dump()
        updated_entity_model_dump.pop('id', None)
        updated_entity_model_dump['addition'].pop('id', None)
        assert updated_entity_model_dump == user_data.custom_properties, "Данные не были обновлены"


@allure.feature('Cервис API')
@allure.story('API')
@allure.title("Получение сущности по ID")
@allure.description("""
Цель: Проверить получение сущности по ID

Шаги:
1. Получить все сущности
2. Выбрать случайную сущность из списка
3. Получить сущность по ID

Ожидаемый результат:
- Проверить что по ID получена правильная сущность
""")
@pytest.mark.usefixtures('ensure_entities_exist')
def test_get_entity_by_id(test_service_api):
    with allure.step('Получить все сущности'):
        entities_response = get_all(test_service_api)

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)
    with allure.step('Получить сущность по ID'):
        fetched_entity = get_entity_by_id(test_service_api, str(entity.id))

    with allure.step("Проверить, что полученная сущность имеет правильный ID"):
        assert fetched_entity.id == entity.id, "Полученная сущность имеет неверный ID"


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
def test_get_all_entity(test_service_api):
    with allure.step('Получить все сущности'):
        response = get_all(test_service_api)
        entities = [Entity(**entity_data.model_dump()) for entity_data in response.entity]

    with allure.step("Проверить, что ответ содержит список сущностей"):
        assert all(isinstance(entity, Entity) for entity in entities), "Ответ не содержит список сущностей"


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
@pytest.mark.usefixtures('ensure_entities_exist')
def test_patch_entity_by_id(test_service_api):
    with allure.step('Получить все сущности'):
        entities_response = get_all(test_service_api)

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)

    with allure.step('Сгенерировать новые данные для сущности'):
        user_data = generate_data()

    with allure.step('Обновить сущность новыми данными'):
        patch_entity_by_id(test_service_api, str(entity.id), user_data)

    with allure.step('Получить обновленную сущность'):
        updated_entity = get_entity_by_id(test_service_api, str(entity.id))

    with allure.step("Проверить, что данные сущности были обновлены"):
        updated_entity_dict = updated_entity.model_dump()
        updated_entity_dict.pop('id', None)
        updated_entity_dict['addition'].pop('id', None)
        assert updated_entity_dict == user_data.custom_properties, "Данные не были обновлены"


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
@pytest.mark.parametrize("iteration", range(1))  # Параметризация для повторения теста, удобно
# использовать для отчистки базы
@pytest.mark.usefixtures('ensure_entities_exist')
def test_del_entity_by_id(test_service_api, iteration):
    with allure.step('Получить все сущности'):
        entities_response = get_all(test_service_api)

    # Выбрать случайную сущность из списка
    entity = random.choice(entities_response.entity)
    with allure.step('Удалить сущность по ID'):
        delete_entity_by_id(test_service_api, str(entity.id))

    with allure.step('Получить все сущности после удаления'):
        entities_after_deletion = get_all(test_service_api)

    with allure.step("Проверить, что удаленная сущность больше не присутствует в списке"):
        assert not any(e.id == entity.id for e in
                       entities_after_deletion.entity), "Удаленная сущность все еще присутствует в списке"
