from datetime import date

import pytest

from property_service import InspectionReminder, MaintenanceRequest, TenantDocument, handle_request


class RecordingClient:
    def __init__(self):
        self.messages = []
        self.captures = []

    def message(self, **payload):
        self.messages.append(payload)

    def capture(self, **payload):
        self.captures.append(payload)


def test_valid_request_creates_seven_day_reminder_and_message():
    client = RecordingClient()
    result = handle_request(MaintenanceRequest("mr-1", "2A", "Heating check"), TenantDocument("doc-1", "t-1", "lease"), client, date(2026, 1, 10))
    assert result == InspectionReminder("mr-1", date(2026, 1, 17))
    assert client.messages[0] == {"text": "inspection reminder created: mr-1:2026-01-17", "level": "info"}


def test_missing_tenant_document_is_captured_and_rejected():
    client = RecordingClient()
    with pytest.raises(ValueError):
        handle_request(MaintenanceRequest("mr-2", "2A", "Heating check"), TenantDocument("doc-2", "", "lease"), client, date(2026, 1, 10))
    assert client.captures[0]["fingerprint"] == ["maintenance", "mr-2"]
