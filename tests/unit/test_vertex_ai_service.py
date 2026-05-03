"""Unit tests for Vertex AI service"""

import pytest
from unittest.mock import Mock, patch
from app.services.vertex_ai_service import VertexAIService, get_vertex_ai_service


class TestVertexAIService:
    """Tests for Vertex AI service"""

    def test_initialization_disabled_without_k_service(self, monkeypatch):
        """Test that Vertex AI is disabled when not on Cloud Run"""
        monkeypatch.delenv("K_SERVICE", raising=False)
        service = VertexAIService()
        result = service.initialize()
        assert result is False
        assert service.enabled is False

    def test_initialization_disabled_without_library(self, monkeypatch):
        """Test graceful degradation when library not available"""
        monkeypatch.setenv("K_SERVICE", "test-service")
        with patch("app.services.vertex_ai_service.VERTEX_AI_AVAILABLE", False):
            service = VertexAIService()
            result = service.initialize()
            assert result is False
            assert service.enabled is False

    def test_initialization_disabled_without_project(self, monkeypatch):
        """Test that initialization fails without project ID"""
        monkeypatch.setenv("K_SERVICE", "test-service")
        monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
        with patch("app.services.vertex_ai_service.VERTEX_AI_AVAILABLE", True):
            service = VertexAIService()
            result = service.initialize()
            assert result is False

    def test_validate_intent_when_disabled(self):
        """Test validate_intent returns unavailable when disabled"""
        service = VertexAIService()
        service.enabled = False
        result = service.validate_intent("test question", "registration", "high")
        assert result["ai_validation"] == "unavailable"
        assert result["ai_confidence"] == "high"

    def test_enhance_response_when_disabled(self):
        """Test enhance_response returns None when disabled"""
        service = VertexAIService()
        service.enabled = False
        result = service.enhance_response("test", "intent", "response")
        assert result is None

    def test_is_enabled(self):
        """Test is_enabled method"""
        service = VertexAIService()
        assert service.is_enabled() is False
        service.enabled = True
        assert service.is_enabled() is True

    def test_singleton_pattern(self):
        """Test that get_vertex_ai_service returns singleton"""
        service1 = get_vertex_ai_service()
        service2 = get_vertex_ai_service()
        assert service1 is service2
