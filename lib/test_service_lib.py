from requests import Response
from data.model import EntitiesResponse, EntityAdd, EntityResponse
from .modules.test_service_module import TestServiceAPI


class TestServiceLib:
    def __init__(self, user_session: TestServiceAPI):
        self.user_session = user_session

    def get_all(self) -> EntitiesResponse:
        response: Response = self.user_session.get_all()
        data = response.json()
        if response.status_code != 200:
            raise ValueError("Не удалось получить все сущности")
        return EntitiesResponse(**data)

    def delete_entity_by_id(self, entity_id: str) -> None:
        response: Response = self.user_session.delete_entity_by_id(entity_id)
        if response.status_code != 204:
            raise ValueError('Не удалось удалить сущность')

    def get_entity_by_id(self, entity_id: str) -> EntityResponse:
        response: Response = self.user_session.get_entity_by_id(entity_id)
        if response.status_code != 200:
            raise ValueError('Не удалось получить сущность по id')
        entity_data = response.json()
        return EntityResponse(**entity_data)

    def create_entity(self, user_data: EntityAdd) -> EntityResponse:
        response: Response = self.user_session.create_entity(user_data=user_data)
        if response.status_code != 200:
            print(response.content)  # print out the response content
            raise ValueError('Не удалось создать сущность')
        entity_id = response.text
        response: Response = self.user_session.get_entity_by_id(entity_id)
        entity_data = response.json()
        return EntityResponse(**entity_data)

    def patch_entity_by_id(self, entity_id: str, user_data: EntityAdd) -> None:
        response: Response = self.user_session.patch_entity_by_id(entity_id, user_data=user_data)
        if response.status_code != 204:
            print(response.content)  # print out the response content
            raise ValueError('Не удалось изменить сущность')