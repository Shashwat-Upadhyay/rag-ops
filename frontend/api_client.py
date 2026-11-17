"""Shared HTTP transport for the Streamlit pages."""
import os
from urllib.parse import quote

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
RequestException = requests.RequestException


def request(method, url, **kwargs):
    kwargs.setdefault("timeout", 10)
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response


def get(url, **kwargs):
    return request("GET", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)


def delete(url, **kwargs):
    return request("DELETE", url, **kwargs)


def document_url(name):
    return f"{API_URL}/admin/documents/{quote(name, safe='')}"
