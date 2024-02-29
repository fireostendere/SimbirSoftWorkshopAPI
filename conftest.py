import allure
import pytest

from _pytest.config.argparsing import Parser

from data.model import EntitiesResponse
from lib.test_service_lib import get_all, create_entity, TestServiceAPI, delete_entity_by_id
from data.data_generator import generate_data


def pytest_addoption(parser: Parser) -> None:
    """
    Add command line option for selecting some parameters.
    """
    parser.addoption("--base_url", action="store", default="http://localhost:8080")
    parser.addoption('--docleanup', action='store_true', help='Run cleanup after tests')


@pytest.fixture(scope='module')
def do_cleanup(request):
    return request.config.getoption('--docleanup')


@pytest.fixture(scope='module')
def test_service_api(request, do_cleanup):
    base_url = request.config.getoption("--base_url")
    api = TestServiceAPI(base_url)

    if do_cleanup:
        # Получить количество сущностей перед тестом
        initial_count = len(get_all(api).entity)
        yield api
        # Восстановить исходное количество сущностей после теста
        final_count = len(get_all(api).entity)
        difference = final_count - initial_count
        if difference > 0:
            # Если были созданы новые сущности, удалить их
            entities = get_all(api).entity
            for entity in entities[:difference]:
                delete_entity_by_id(api, str(entity.id))
        elif difference < 0:
            # Если были удалены сущности, создать их
            for _ in range(abs(difference)):
                user_data = generate_data()
                create_entity(api, user_data)
    else:
        yield api


@pytest.fixture(scope='module')
def ensure_entities_exist(test_service_api):
    response = get_all(test_service_api)
    entities = response.entity if isinstance(response, EntitiesResponse) else None
    if not entities:
        user_data = generate_data()
        create_entity(test_service_api, user_data)
    yield


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call' and call.excinfo is not None:
        if "api_client" in item.funcargs:
            api_client = item.funcargs["api_client"]
            if api_client.last_request is not None and api_client.last_response is not None:
                allure.attach(
                    body=str(api_client.last_request),
                    name="Last Request",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    body=str(api_client.last_response),
                    name="Last Response",
                    attachment_type=allure.attachment_type.TEXT
                )