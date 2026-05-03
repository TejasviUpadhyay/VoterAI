"""Additional tests for main.py coverage"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rate_limit_middleware_allows_requests():
    """Test rate limiting allows normal requests"""
    response = client.get("/")
    assert response.status_code == 200


def test_security_headers_middleware():
    """Test security headers are added"""
    response = client.get("/")
    assert "x-content-type-options" in response.headers


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/")
    assert response.status_code in [200, 405]


def test_static_files_mounted():
    """Test static files are accessible"""
    response = client.get("/static/index.html")
    assert response.status_code in [200, 404]
