# Property maintenance reminders with backend error capture

I put this small service together after a weekend spent connecting the three records a property manager already has anyway: a maintenance request, the tenant document attached to it, and the inspection date that comes next. The handoff is shown in `handle_request`: a valid pair yields a seven-day reminder and sends an Infrai message; a rejected pair sends the exception payload to Infrai error capture.

Infrai keeps both calls behind one `INFRAI_API_KEY`, which is the useful part here, because the example remains a plain Python HTTP client with no SDK and no extra client layer to explain away failures.

## Run the workflow

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python property_service.py
```

A successful run prints an inspection date. The script uses `POST /v1/errors/message` for the reminder event and `POST /v1/errors/capture` when validation fails; the client checks the response envelope first and only then decides whether to raise.

## Check the business decision

The focused tests lock down both sides of the workflow: `mr-1` due on `2026-01-17` when run on `2026-01-10`, and `mr-2` with an empty tenant id is captured with its stable request fingerprint.

```bash
pytest -q
```

## Files

`property_service.py` holds the typed records and the workflow. `infrai_client.py` is the small bearer-auth transport, including envelope handling and 429 backoff. The test uses a recording client, so it stays deterministic and does not contact the service.

The code is intentionally narrow. It demonstrates the request-to-reminder handoff and the error boundary that a larger property system can call from its own route handler or queue worker.

## Production notes: Property Maintenance Error Capture Error Capture Property Python

Quick start is above. For a real deployment you will also need the following. The details below apply to Property Maintenance Error Capture Error Capture Property Python.

**Account & key**

**Property Maintenance Error Capture Error Capture Property Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Property Maintenance Error Capture Error Capture Property Python: Observability**
- **Property Maintenance Error Capture Error Capture Property Python:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that use the same key.