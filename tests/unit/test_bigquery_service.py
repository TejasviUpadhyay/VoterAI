"""Unit tests for BigQuery service"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.bigquery_service import BigQueryService, get_bigquery_service


class TestBigQueryService:
    """Tests for BigQuery service"""

    def test_initialization_disabled_without_k_service(self, monkeypatch):
        """Test that BigQuery is disabled when not on Cloud Run"""
        monkeypatch.delenv("K_SERVICE", raising=False)
        service = BigQueryService()
        result = service.initialize()
        assert result is False
        assert service.enabled is False

    def test_initialization_disabled_without_library(self, monkeypatch):
        """Test graceful degradation when library not available"""
        monkeypatch.setenv("K_SERVICE", "test-service")
        with patch("app.services.bigquery_service.BIGQUERY_AVAILABLE", False):
            service = BigQueryService()
            result = service.initialize()
            assert result is False
            assert service.enabled is False

    def test_log_query_when_disabled(self):
        """Test that log_query does nothing when disabled"""
        service = BigQueryService()
        service.enabled = False
        # Should not raise exception
        service.log_query("test", "intent", "high", 5, 100.0, "sheets")

    def test_log_query_when_enabled(self, monkeypatch):
        """Test query logging when enabled"""
        monkeypatch.setenv("K_SERVICE", "test-service")
        
        service = BigQueryService()
        service.client = Mock()
        service.client.project = "test-project"
        service.client.insert_rows_json.return_value = []
        service.enabled = True
        
        service.log_query(
            "How do I register?",
            "registration",
            "high",
            3,
            250.5,
            "sheets"
        )
        
        assert service.client.insert_rows_json.called

    def test_get_intent_distribution_when_disabled(self):
        """Test intent distribution returns empty when disabled"""
        service = BigQueryService()
        service.enabled = False
        result = service.get_intent_distribution()
        assert result == {}

    def test_get_average_response_time_when_disabled(self):
        """Test average response time returns 0 when disabled"""
        service = BigQueryService()
        service.enabled = False
        result = service.get_average_response_time()
        assert result == 0.0

    def test_is_enabled(self):
        """Test is_enabled method"""
        service = BigQueryService()
        assert service.is_enabled() is False
        service.enabled = True
        assert service.is_enabled() is True

    def test_singleton_pattern(self):
        """Test that get_bigquery_service returns singleton"""
        service1 = get_bigquery_service()
        service2 = get_bigquery_service()
        assert service1 is service2
