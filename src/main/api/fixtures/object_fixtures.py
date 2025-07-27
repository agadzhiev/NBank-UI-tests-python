import pytest
from typing import List, Any

from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.classes.api_manager import ApiManager


@pytest.fixture
def created_objects():
    objects: List[Any] = []
    yield objects

    cleanup_objects(objects)


def cleanup_objects(objects: List[Any]):
    api = ApiManager(objects)
    for obj in objects:
        if isinstance(obj, CreateUserResponse):
            api.admin_steps.delete_user(obj.id)