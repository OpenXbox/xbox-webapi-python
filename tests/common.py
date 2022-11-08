import json
import os

TEST_PATH = os.path.dirname(__file__)


def get_response(name):
    """Read a response file."""
    with open(f"{TEST_PATH}/data/responses/{name}.json", encoding="utf8") as f:
        return f.read()


def get_response_json(name):
    """Read a response file and return json dict."""
    text = get_response(name)
    return json.loads(text)
