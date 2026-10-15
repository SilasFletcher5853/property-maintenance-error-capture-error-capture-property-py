from dataclasses import dataclass
from datetime import date, timedelta
import traceback

from infrai_client import InfraiClient


@dataclass(frozen=True)
class MaintenanceRequest:
    request_id: str
    unit: str
    description: str


@dataclass(frozen=True)
class TenantDocument:
    document_id: str
    tenant_id: str
    kind: str


@dataclass(frozen=True)
class InspectionReminder:
    request_id: str
    due_on: date


def handle_request(request: MaintenanceRequest, document: TenantDocument, client: InfraiClient, today: date | None = None) -> InspectionReminder:
    """Create an inspection reminder and capture a useful backend failure."""
    run_date = today or date.today()
    try:
        if document.tenant_id == "":
            raise ValueError("tenant document has no tenant id")
        if not request.description.strip():
            raise ValueError("maintenance description is empty")
        reminder = InspectionReminder(request.request_id, run_date + timedelta(days=7))
        client.message(text=f"inspection reminder created: {request.request_id}:{reminder.due_on.isoformat()}", level="info")
        return reminder
    except Exception as exc:
        client.capture(title="maintenance workflow failed", message=str(exc), level="error", exception=traceback.format_exc(), fingerprint=["maintenance", request.request_id], context={"unit": request.unit, "document_id": document.document_id})
        raise


if __name__ == "__main__":
    client = InfraiClient()
    result = handle_request(MaintenanceRequest("mr-104", "4B", "Replace a leaking tap"), TenantDocument("doc-9", "tenant-7", "lease"), client)
    print(f"inspection for {result.request_id} is due on {result.due_on}")
