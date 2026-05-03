"""Full coverage tests for response service"""
from app.services.response_service import ResponseService


def test_format_response_with_all_fields():
    """Test response formatting with complete data"""
    service = ResponseService()
    data = {
        "title": "Test",
        "overview": "Overview",
        "steps": ["Step 1", "Step 2"],
        "documents": ["Doc 1"],
        "tips": ["Tip 1"],
        "next_action": "Next"
    }
    response = service.format_response("test", data)
    assert response.title == "Test"
    assert len(response.steps) == 2


def test_format_response_with_missing_fields():
    """Test response formatting with missing fields"""
    service = ResponseService()
    data = {"title": "Test"}
    response = service.format_response("test", data)
    assert response.title == "Test"
    assert response.steps == []
