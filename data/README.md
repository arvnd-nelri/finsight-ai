# data/

Local data for FinSight AI. Most of it is **not committed to Git**.

| Folder | Contents | In Git? |
| --- | --- | --- |
| `raw/` | Untouched downloads from SEC EDGAR (JSON, filing text), kept as the source of truth | No |
| `processed/` | Cleaned and normalized data, and local database files | No |

Everything in `raw/` and `processed/` must be reproducible by running the
project's scripts, so it never needs to be committed. Sub-folders are created
when Milestone 2 (data collection) starts.
