import json

import requests

from typing import Dict, Optional, Any
from requests import Response
from data.model import EntityAdd


class TestServiceAPI:

    def __init__(self, base_url):
        self.test_service_create_api_url: str = base_url + '/api/create'
        self.test_service_delete_api_url: str = base_url + '/api/delete'
        self.test_service_get_api_url: str = base_url + '/api/get'
        self.test_service_getAll_api_url: str = base_url + '/api/getAll'
        self.test_service_patch_api_url: str = base_url + '/api/patch'

    @property
    def get_default_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_all(self, headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response:
        headers = headers or self.get_default_headers
        return requests.get(url=self.test_service_getAll_api_url, headers=headers, **kwargs)

    def create_entity(self, user_data: EntityAdd, headers: Optional[Dict[str, str]] = None) -> Response:
        headers = headers or self.get_default_headers
        return requests.post(url=self.test_service_create_api_url, headers=headers,
                             data=json.dumps(user_data.model_dump()))

    def patch_entity_by_id(self, entity_id: str, user_data: EntityAdd,
                           headers: Optional[Dict[str, str]] = None) -> Response:
        headers = headers or self.get_default_headers
        url = f"{self.test_service_patch_api_url}/{entity_id}"
        return requests.patch(url=url, headers=headers, data=json.dumps(user_data.model_dump()))

    def delete_entity_by_id(self, entity_id: str, headers: Optional[Dict[str, str]] = None,
                            **kwargs: Any) -> Response:
        headers = headers or self.get_default_headers
        url = f"{self.test_service_delete_api_url}/{entity_id}"
        return requests.delete(url=url, headers=headers, **kwargs)

    def get_entity_by_id(self, entity_id: str, headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response:
        headers = headers or self.get_default_headers
        url = f"{self.test_service_get_api_url}/{entity_id}"
        response = requests.get(url=url, headers=headers, **kwargs)
        return response
