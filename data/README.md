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
```

Rebuild with `python scripts/download_sec_data.py <CIK> [--force]`
(needs `SEC_USER_AGENT` in `~/.config/finsight-ai/sec.env`).
