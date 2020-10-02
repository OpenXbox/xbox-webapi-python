import os

TEST_PATH = os.path.dirname(__file__)


def get_response(name):
    """Read a response file."""
    with open(f"{TEST_PATH}/data/responses/{name}.json") as f:
        response = f.read()
    return response
