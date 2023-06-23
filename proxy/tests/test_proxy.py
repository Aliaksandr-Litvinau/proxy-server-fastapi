import re
from unittest.mock import patch

import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from proxy import router

client = TestClient(router.app)

PATHS = [
    "/",
    "/donate.php",
    "/politica.html",
    "/play.php?",
]


@pytest.mark.parametrize("path", PATHS)
def test_correct_page_returned(path):
    response = client.get(path)
    assert response.status_code == 200
    assert "DOCTYPE html" in response.text


def test_text_replacement_when_phrases_exist():
    html = "<html><body><p>Black Russia <span>black Russia</span></p></body></html>"
    expected_html = "<html><body><p>BlackHub Games <span>BlackHub Games</span></p></body></html>"
    modified_html = re.sub(r"Black(\s*<[^>]+>)?\s*Russia", "BlackHub Games", html, flags=re.IGNORECASE)
    assert modified_html == expected_html


def test_multiple_text_replacement_when_phrases_exist():
    html = "<html><body><p>Black Russia <span>black Russia</span></p></body></html>"
    expected_html = "<html><body><p>BlackHub Games <span>BlackHub Games</span></p></body></html>"
    modified_html = re.sub(r"Black(\s*<[^>]+>)?\s*Russia", "BlackHub Games", html, flags=re.IGNORECASE)
    assert modified_html == expected_html


def test_text_replacement_when_phrases_absent():
    html = "<html><body><p>Just text without any phrases</p></body></html>"
    expected_html = "<html><body><p>Just text without any phrases</p></body></html>"
    modified_html = re.sub(r"Black(\s*<[^>]+>)?\s*Russia", "BlackHub Games", html, flags=re.IGNORECASE)
    assert modified_html == expected_html


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def test_non_get_request_returns_405(method):
    path = "/random_path"
    response = client.request(method, path)
    assert response.status_code == 405


def test_proxy_returns_404():
    with patch.object(AsyncClient, 'get') as mock_get:
        mock_get.return_value.status_code = 404
        response = client.get("/gltogtpgrgtyhsh")

        assert response.status_code == 404
        assert response.json() == {"error": "Not found"}


def test_proxy_raises_exception_on_request_error():
    with patch.object(AsyncClient, 'get') as mock_get:
        mock_get.side_effect = httpx.RequestError("Mocked request error")
        response = client.get("/some/path")

        assert response.status_code == 500
        assert response.json() == {"error": "Internal Server Error"}
