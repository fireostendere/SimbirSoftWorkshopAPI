import json
import requests

from typing import Any
from requests import Response
from data.model import EntityRequest


class TestServiceAPI:

    DEFAULT_HEADERS_JSON = json.dumps({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    def __init__(self, base_url):
        self.session = requests.Session()
        self.test_service_create_api_url: str = base_url + '/api/create'
        self.test_service_delete_api_url: str = base_url + '/api/delete'
        self.test_service_get_api_url: str = base_url + '/api/get'
        self.test_service_getAll_api_url: str = base_url + '/api/getAll'
        self.test_service_patch_api_url: str = base_url + '/api/patch'

    def get_all(self, headers_json: str = DEFAULT_HEADERS_JSON, **kwargs: Any) -> Response:
        headers = json.loads(headers_json)
        return self.session.get(url=self.test_service_getAll_api_url, headers=headers, **kwargs)

    def create_entity(self, user_data: EntityRequest, headers_json: str = DEFAULT_HEADERS_JSON) -> Response:
        headers = json.loads(headers_json)
        return self.session.post(url=self.test_service_create_api_url, headers=headers,
                                 data=user_data.model_dump_json())

    def patch_entity_by_id(self, entity_id: str, user_data: EntityRequest,
                           headers_json: str = DEFAULT_HEADERS_JSON) -> Response:
        headers = json.loads(headers_json)
        url = f"{self.test_service_patch_api_url}/{entity_id}"
        return self.session.patch(url=url, headers=headers, data=user_data.model_dump_json())

    def delete_entity_by_id(self, entity_id: str, headers_json: str = DEFAULT_HEADERS_JSON,
                            **kwargs: Any) -> Response:
        headers = json.loads(headers_json)
        url = f"{self.test_service_delete_api_url}/{entity_id}"
        return self.session.delete(url=url, headers=headers, **kwargs)

    def get_entity_by_id(self, entity_id: str, headers_json: str = DEFAULT_HEADERS_JSON, **kwargs: Any) -> Response:
        headers = json.loads(headers_json)
        url = f"{self.test_service_get_api_url}/{entity_id}"
        response = self.session.get(url=url, headers=headers, **kwargs)
        return response
