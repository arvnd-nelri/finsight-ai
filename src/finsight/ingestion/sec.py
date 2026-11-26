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


def _write_metadata(path: Path, url: str, status: int, content: bytes, **extra) -> None:
    """Write `<name>.meta.json` next to `path`: where, when, and a checksum."""
    metadata = {
        "source_url": url,
        **extra,
        "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "http_status": status,
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.with_suffix(".meta.json").write_text(json.dumps(metadata, indent=2) + "\n")


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
    _write_metadata(path, url, response.status_code, content,
                    cik=normalize_cik(cik), entity_name=data.get("entityName"))
    return path


# --- Frames: one tag, one period, every company ---------------------------------


def _unit_slug(unit: str) -> str:
    """The SEC writes "USD/shares" in data but "USD-per-shares" in frame URLs."""
    return unit.replace("/", "-per-")


def frame_url(tag: str, unit: str, period: str, taxonomy: str = "us-gaap") -> str:
    """URL of one frame, e.g. period "CY2025" (a year) or "CY2025Q4I" (an instant)."""
    return f"{SEC_API_BASE}/api/xbrl/frames/{taxonomy}/{tag}/{_unit_slug(unit)}/{period}.json"


def raw_frame_path(
    tag: str, unit: str, period: str, raw_dir: Path, taxonomy: str = "us-gaap"
) -> Path:
    """Where the raw frame for this tag, unit, and period is stored."""
    name = f"{taxonomy}_{tag}_{_unit_slug(unit)}_{period}.json"
    return raw_dir / "sec" / "frames" / name


def download_frame(
    tag: str, unit: str, period: str, client: SecClient, raw_dir: Path,
    *, force: bool = False,
) -> Path | None:
    """Download one frame into `raw_dir`; return its path, or None if the SEC
    has no data for it (HTTP 404).

    A 404 is remembered in the metadata file only, so the raw folder never
    holds anything the SEC did not send. Skips work already done unless `force`.
    """
    path = raw_frame_path(tag, unit, period, raw_dir)
    meta = path.with_suffix(".meta.json")
    if not force:
        if path.exists():
            return path
        if meta.exists() and json.loads(meta.read_text())["http_status"] == 404:
            return None

    url = frame_url(tag, unit, period)
    try:
        response = client.get(url)
    except httpx.HTTPStatusError as err:
        if err.response.status_code != 404:
            raise
        path.unlink(missing_ok=True)
        _write_metadata(path, url, 404, b"", tag=tag, unit=unit, period=period)
        return None

    content = response.content
    data = json.loads(content)
    if data.get("tag") != tag or "data" not in data:
        raise ValueError(f"Response is not the frame for {tag!r}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    _write_metadata(path, url, response.status_code, content, tag=tag, unit=unit, period=period)
    return path


def load_frame(path: Path | None) -> dict[int, float]:
    """CIK -> value from a downloaded frame; empty if there was no frame."""
    if path is None:
        return {}
    return {row["cik"]: row["val"] for row in json.loads(path.read_bytes())["data"]}
