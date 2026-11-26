"""Download raw SEC company-facts JSON into data/raw/.

Usage:
    python scripts/download_sec_data.py 789019          # Microsoft
    python scripts/download_sec_data.py 789019 --force  # download again

Thin entry point: the logic lives in finsight.ingestion.sec.
"""

import argparse
import sys
from pathlib import Path

from finsight.config import ConfigError, get_sec_user_agent
from finsight.ingestion.sec import SecClient, download_company_facts

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ciks", nargs="+", help="SEC CIK numbers, e.g. 789019")
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args(argv)

    try:
        user_agent = get_sec_user_agent()
    except ConfigError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    with SecClient(user_agent) as client:
        for cik in args.ciks:
            path = download_company_facts(cik, client, RAW_DIR, force=args.force)
            size_mb = path.stat().st_size / 1_000_000
            print(f"{cik}: {path.relative_to(RAW_DIR.parent.parent)} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
