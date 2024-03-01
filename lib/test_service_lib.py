from requests import Response

from data.model import EntitiesResponse, EntityAdd, Entity
from .modules.test_service_module import TestServiceAPI


def get_all(user_session: TestServiceAPI) -> EntitiesResponse:
    response: Response = user_session.get_all()
    data = response.json()
    assert response.status_code == 200, "Не удалось получить все сущности"
    return EntitiesResponse(**data)


def delete_entity_by_id(user_session: TestServiceAPI, entity_id: str) -> None:
    response: Response = user_session.delete_entity_by_id(entity_id)
    assert response.status_code == 204, 'Не удалось удалить сущность'


def get_entity_by_id(user_session: TestServiceAPI, entity_id: str) -> Entity:
    response: Response = user_session.get_entity_by_id(entity_id)
    assert response.status_code == 200, 'Не удалось получить сущность по id'
    entity_data = response.json()
    return Entity(**entity_data)


def create_entity(user_session: TestServiceAPI, user_data: EntityAdd) -> Entity:
    response: Response = user_session.create_entity(user_data=user_data.custom_properties)
    assert response.status_code == 200, 'Не удалось создать сущность'
    entity_id = response.json()
    entity_data = user_session.get_entity_by_id(entity_id).json()
    return Entity(**entity_data)


def patch_entity_by_id(user_session: TestServiceAPI, entity_id: str, user_data: EntityAdd) -> None:
    response: Response = user_session.patch_entity_by_id(entity_id, user_data=user_data.custom_properties)
    assert response.status_code == 204, 'Не удалось изменить сущность'
