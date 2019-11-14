import pytest
import sys, os
from app import App


@pytest.fixture
def app():
    app = App().create_app()
    return app
