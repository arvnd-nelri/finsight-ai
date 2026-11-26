"""Tests for finsight.ingestion.sec. No real network: a fake transport plays the SEC."""

import hashlib
import json

import httpx
import pytest

from finsight.ingestion.sec import (
    SecClient,
    company_facts_url,
    download_company_facts,
    normalize_cik,
    raw_company_facts_path,
)

USER_AGENT = "Test User test@example.com"
# A tiny stand-in for the real response. Placeholder values, not real figures.
FAKE_FACTS = json.dumps(
    {"cik": 789019, "entityName": "MICROSOFT CORP", "facts": {}}
).encode()


def make_client(handler) -> SecClient:
    """A SecClient whose requests go to `handler` instead of the internet."""
    return SecClient(USER_AGENT, min_interval=0, transport=httpx.MockTransport(handler))


class Recorder:
    """Fake SEC server: records each request and returns a canned response."""

    def __init__(self, status: int = 200, body: bytes = FAKE_FACTS):
        self.requests: list[httpx.Request] = []
        self.status, self.body = status, body

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(self.status, content=self.body)


# --- CIK and URL helpers -----------------------------------------------------


@pytest.mark.parametrize("cik", [789019, "789019", "0000789019", " 789019 "])
def test_normalize_cik_pads_to_ten_digits(cik):
    assert normalize_cik(cik) == "0000789019"


@pytest.mark.parametrize("bad", ["MSFT", "", "12345678901", "-1"])
def test_normalize_cik_rejects_invalid(bad):
    with pytest.raises(ValueError):
        normalize_cik(bad)


def test_company_facts_url():
    assert (
        company_facts_url(789019)
        == "https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json"
    )


def test_raw_path_layout(tmp_path):
    path = raw_company_facts_path(789019, tmp_path)
    assert path == tmp_path / "sec" / "companyfacts" / "CIK0000789019.json"


# --- SecClient ---------------------------------------------------------------


def test_client_sends_user_agent():
    server = Recorder()
    with make_client(server) as client:
        client.get(company_facts_url(789019))
    assert server.requests[0].headers["User-Agent"] == USER_AGENT


def test_client_raises_on_http_error():
    with make_client(Recorder(status=404, body=b"not found")) as client:
        with pytest.raises(httpx.HTTPStatusError):
            client.get(company_facts_url(789019))


def test_client_waits_between_requests(monkeypatch):
    sleeps: list[float] = []
    monkeypatch.setattr("finsight.ingestion.sec.time.sleep", sleeps.append)
    client = SecClient(
        USER_AGENT, min_interval=0.2, transport=httpx.MockTransport(Recorder())
    )
    client.get(company_facts_url(789019))
    client.get(company_facts_url(789019))
    client.close()
    assert len(sleeps) == 1 and 0 < sleeps[0] <= 0.2


# --- download_company_facts --------------------------------------------------


def test_download_saves_response_unchanged(tmp_path):
    with make_client(Recorder()) as client:
        path = download_company_facts(789019, client, tmp_path)
    assert path == raw_company_facts_path(789019, tmp_path)
    assert path.read_bytes() == FAKE_FACTS


def test_download_writes_provenance_metadata(tmp_path):
    with make_client(Recorder()) as client:
        path = download_company_facts(789019, client, tmp_path)
    meta = json.loads(path.with_suffix(".meta.json").read_text())
    assert meta["source_url"] == company_facts_url(789019)
    assert meta["cik"] == "0000789019"
    assert meta["entity_name"] == "MICROSOFT CORP"
    assert meta["http_status"] == 200
    assert meta["size_bytes"] == len(FAKE_FACTS)
    assert meta["sha256"] == hashlib.sha256(FAKE_FACTS).hexdigest()
    assert meta["retrieved_at"].endswith("+00:00")  # stored in UTC


def test_download_skips_existing_file(tmp_path):
    server = Recorder()
    with make_client(server) as client:
        download_company_facts(789019, client, tmp_path)
        download_company_facts(789019, client, tmp_path)
    assert len(server.requests) == 1


def test_download_force_fetches_again(tmp_path):
    server = Recorder()
    with make_client(server) as client:
        download_company_facts(789019, client, tmp_path)
        download_company_facts(789019, client, tmp_path, force=True)
    assert len(server.requests) == 2


def test_download_rejects_response_for_wrong_company(tmp_path):
    other = json.dumps({"cik": 320193, "facts": {}}).encode()
    with make_client(Recorder(body=other)) as client:
        with pytest.raises(ValueError, match="does not match"):
            download_company_facts(789019, client, tmp_path)
    assert not raw_company_facts_path(789019, tmp_path).exists()


def test_download_does_not_save_on_http_error(tmp_path):
    with make_client(Recorder(status=403, body=b"blocked")) as client:
        with pytest.raises(httpx.HTTPStatusError):
            download_company_facts(789019, client, tmp_path)
    assert not raw_company_facts_path(789019, tmp_path).exists()
