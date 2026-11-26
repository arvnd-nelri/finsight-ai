# data/

Local data for FinSight AI. Most of it is **not committed to Git**.

| Folder | Contents | In Git? |
| --- | --- | --- |
| `raw/` | Untouched downloads from SEC EDGAR (JSON, filing text), kept as the source of truth | No |
| `processed/` | Cleaned and normalized data, and local database files | No |

Everything in `raw/` and `processed/` must be reproducible by running the
project's scripts, so it never needs to be committed.

## Layout

```text
raw/sec/companyfacts/
├── CIK0000789019.json        SEC response, byte-for-byte unchanged
└── CIK0000789019.meta.json   provenance: source URL, UTC time, size, SHA-256
raw/sec/frames/
├── us-gaap_Assets_USD_CY2025Q4I.json        one tag, one period, every company
└── us-gaap_Assets_USD_CY2025Q4I.meta.json   provenance (a 404 is recorded here only)
```

Rebuild company facts with `python scripts/download_sec_data.py <CIK> [--force]`
and frames with `python scripts/check_catalog_coverage.py [--refresh]`
(both need `SEC_USER_AGENT` in `~/.config/finsight-ai/sec.env`).
