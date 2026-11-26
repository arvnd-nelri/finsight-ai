"""Download raw XBRL company-facts data from the SEC EDGAR API.

The response is saved byte-for-byte unchanged, next to a small metadata file
recording where and when it was fetched (provenance). Cleaning happens in a
later step, so a cleaning bug never requires downloading again.

SEC access rules (https://www.sec.gov/os/accessing-edgar-data):
- every request must send a User-Agent with a name and email address;
- no more than 10 requests per second.
"""

import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

SEC_API_BASE = "https://data.sec.gov"

# Seconds to wait between requests: at most 5 per second, half the SEC limit.
DEFAULT_MIN_INTERVAL = 0.2


def normalize_cik(cik: int | str) -> str:
    """Return the CIK as the 10-digit, zero-padded string the SEC API uses."""
    digits = str(cik).strip()
    if not digits.isdigit() or len(digits) > 10:
        raise ValueError(f"Invalid CIK: {cik!r} (expected up to 10 digits)")
    return digits.zfill(10)


def company_facts_url(cik: int | str) -> str:
    """URL of the company-facts JSON for one company."""
    return f"{SEC_API_BASE}/api/xbrl/companyfacts/CIK{normalize_cik(cik)}.json"


def raw_company_facts_path(cik: int | str, raw_dir: Path) -> Path:
    """Where the raw company-facts file for `cik` is stored under `raw_dir`."""
    return raw_dir / "sec" / "companyfacts" / f"CIK{normalize_cik(cik)}.json"


class SecClient:
    """A small HTTP client that follows the SEC's access rules."""

    def __init__(
        self,
        user_agent: str,
        *,
        min_interval: float = DEFAULT_MIN_INTERVAL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._http = httpx.Client(
            headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"},
            timeout=timeout,
            transport=transport,  # tests pass a fake transport; None = real network
        )
        self._min_interval = min_interval
        self._last_request: float | None = None

    def get(self, url: str) -> httpx.Response:
        """GET `url`, waiting first if needed to respect the rate limit.

        Raises httpx.HTTPStatusError for 4xx/5xx responses.
        """
        if self._last_request is not None:
            wait = self._min_interval - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
        try:
            response = self._http.get(url)
        finally:
            self._last_request = time.monotonic()
        response.raise_for_status()
        return response

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "SecClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


def download_company_facts(
    cik: int | str, client: SecClient, raw_dir: Path, *, force: bool = False
) -> Path:
    """Download one company's facts JSON into `raw_dir` and return its path.

    Skips the download if the file already exists, unless `force` is True.
    Also writes `<name>.meta.json` with the source URL, time, and checksum.
    """
    path = raw_company_facts_path(cik, raw_dir)
    if path.exists() and not force:
        return path

    url = company_facts_url(cik)
    response = client.get(url)
    content = response.content

    # Sanity check before saving: valid JSON, and for the company we asked for.
    data = json.loads(content)
    if int(data.get("cik", -1)) != int(normalize_cik(cik)):
        raise ValueError(f"Response CIK {data.get('cik')!r} does not match {cik!r}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    metadata = {
        "source_url": url,
        "cik": normalize_cik(cik),
        "entity_name": data.get("entityName"),
        "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "http_status": response.status_code,
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }
    path.with_suffix(".meta.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return path
