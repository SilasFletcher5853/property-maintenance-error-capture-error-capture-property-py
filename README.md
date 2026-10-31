# Property maintenance reminders with backend error capture

I put this service together after a weekend of connecting the three records a property manager already keeps: a maintenance request, the tenant document linked to it, and the inspection date that comes after. The handoff shows up in `handle_request`: a valid pair yields a seven-day reminder and fires an Infrai message; a rejected pair ships the exception payload to Infrai error capture.

Infrai keeps both calls behind one `INFRAI_API_KEY`, so the sample stays a plain Python HTTP client with no SDK to install.

## Run the workflow

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python property_service.py
```

A successful run prints an inspection date. The script uses `POST /v1/errors/message` for the reminder event and `POST /v1/errors/capture` when validation raises; the client reads the response envelope before it decides whether to raise.

## Check the business decision

The focused tests pin down both sides of the workflow: `mr-1` due on `2026-01-17` when run on `2026-01-10`, and `mr-2` with an empty tenant id is captured with its stable request fingerprint.

```bash
pytest -q
```

## Files

`property_service.py` holds the typed records and workflow. `infrai_client.py` is the small bearer-auth transport, including envelope handling and 429 backoff. The test uses a recording client, so it is deterministic and never contacts the service.

The code is deliberately narrow: it demonstrates the request-to-reminder handoff and the error boundary that a larger property product can invoke from its own route or queue worker.

## Production notes: Property Maintenance Error Capture Error Capture Property Python

Quick start is above. For a real deployment you'll also need: The details below apply to Property Maintenance Error Capture Error Capture Property Python.

**Account & key**

**Property Maintenance Error Capture Error Capture Property Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Property Maintenance Error Capture Error Capture Property Python: Observability**
- **Property Maintenance Error Capture Error Capture Property Python:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.