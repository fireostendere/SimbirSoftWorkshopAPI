import allure
import pytest

from _pytest.config.argparsing import Parser

from data.model import EntitiesResponse
from lib.test_service_lib import TestServiceLib, TestServiceAPI
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
def test_service_api(request):
    base_url = request.config.getoption("--base_url")
    return TestServiceAPI(base_url)


@pytest.fixture(scope='module')
def test_service_lib(request, test_service_api, do_cleanup):
    lib = TestServiceLib(test_service_api)

    if do_cleanup:
        # Получить количество сущностей перед тестом
        initial_count = len(lib.get_all().entity)
        yield lib
        # Восстановить исходное количество сущностей после теста
        final_count = len(lib.get_all().entity)
        difference = final_count - initial_count
        if difference > 0:
            # Если были созданы новые сущности, удалить их
            entities = lib.get_all().entity
            for entity in entities[:difference]:
                lib.delete_entity_by_id(str(entity.id))
        elif difference < 0:
            # Если были удалены сущности, создать их
            for _ in range(abs(difference)):
                user_data = generate_data()
                lib.create_entity(user_data)
    else:
        yield lib


@pytest.fixture(scope='module')
def ensure_entities_exist(test_service_lib):
    response = test_service_lib.get_all()
    entities = response.entity if isinstance(response, EntitiesResponse) else None
    if not entities:
        user_data = generate_data()
        test_service_lib.create_entity(user_data)
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
