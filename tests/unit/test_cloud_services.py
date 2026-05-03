"""Unit tests for Cloud Logging, Monitoring, and Firestore services"""

import pytest
from unittest.mock import Mock, patch
from app.services.cloud_logging_service import (
    CloudLoggingService,
    get_cloud_logging_service
)
from app.services.cloud_monitoring_service import (
    CloudMonitoringService,
    get_cloud_monitoring_service
)
from app.services.firestore_service import (
    FirestoreService,
    get_firestore_service
)


class TestCloudLoggingService:
    """Tests for Cloud Logging service"""

    def test_initialization_disabled_without_k_service(self, monkeypatch):
        """Test disabled when not on Cloud Run"""
        monkeypatch.delenv("K_SERVICE", raising=False)
        service = CloudLoggingService()
        result = service.initialize()
        assert result is False

    def test_is_enabled(self):
        """Test is_enabled method"""
        service = CloudLoggingService()
        assert service.is_enabled() is False
        service.enabled = True
        assert service.is_enabled() is True

    def test_singleton_pattern(self):
        """Test singleton"""
        service1 = get_cloud_logging_service()
        service2 = get_cloud_logging_service()
        assert service1 is service2


class TestCloudMonitoringService:
    """Tests for Cloud Monitoring service"""

    def test_initialization_disabled_without_k_service(self, monkeypatch):
        """Test disabled when not on Cloud Run"""
        monkeypatch.delenv("K_SERVICE", raising=False)
        service = CloudMonitoringService()
        result = service.initialize()
        assert result is False

    def test_record_response_time_when_disabled(self):
        """Test recording does nothing when disabled"""
        service = CloudMonitoringService()
        service.enabled = False
        # Should not raise
        service.record_response_time(100.0, "registration")

    def test_record_intent_detection_when_disabled(self):
        """Test recording does nothing when disabled"""
        service = CloudMonitoringService()
        service.enabled = False
        service.record_intent_detection("registration", "high")

    def test_record_cache_hit_when_disabled(self):
        """Test recording does nothing when disabled"""
        service = CloudMonitoringService()
        service.enabled = False
        service.record_cache_hit(True)

    def test_record_data_source_when_disabled(self):
        """Test recording does nothing when disabled"""
        service = CloudMonitoringService()
        service.enabled = False
        service.record_data_source("sheets")

    def test_is_enabled(self):
        """Test is_enabled method"""
        service = CloudMonitoringService()
        assert service.is_enabled() is False

    def test_singleton_pattern(self):
        """Test singleton"""
        service1 = get_cloud_monitoring_service()
        service2 = get_cloud_monitoring_service()
        assert service1 is service2


class TestFirestoreService:
    """Tests for Firestore service"""

    def test_initialization_disabled_without_k_service(self, monkeypatch):
        """Test disabled when not on Cloud Run"""
        monkeypatch.delenv("K_SERVICE", raising=False)
        service = FirestoreService()
        result = service.initialize()
        assert result is False

    def test_log_query_when_disabled(self):
        """Test logging does nothing when disabled"""
        service = FirestoreService()
        service.enabled = False
        # Should not raise
        service.log_query("test", "intent", "high", 3, 100.0, "sheets")

    def test_get_intent_stats_when_disabled(self):
        """Test returns empty when disabled"""
        service = FirestoreService()
        service.enabled = False
        result = service.get_intent_stats()
        assert result == {}

    def test_is_enabled(self):
        """Test is_enabled method"""
        service = FirestoreService()
        assert service.is_enabled() is False

    def test_singleton_pattern(self):
        """Test singleton"""
        service1 = get_firestore_service()
        service2 = get_firestore_service()
        assert service1 is service2
