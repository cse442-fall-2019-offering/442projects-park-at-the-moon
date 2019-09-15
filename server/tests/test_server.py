from app import *
import pytest

@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Set up the socket, client, server etc.
    :return:
    """
    pass

def test_dummy():
    assert True