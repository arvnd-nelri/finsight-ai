"""Measure how well the metric catalog finds each metric (task 2.3b).

Usage:
    python scripts/check_catalog_coverage.py                    # across companies
    python scripts/check_catalog_coverage.py --companies 789019 104169
    python scripts/check_catalog_coverage.py --year 2025 --min-assets 1e9
    python scripts/check_catalog_coverage.py --refresh          # download again

Downloads (once) the SEC frames each catalog tag needs into data/raw/, then
prints coverage per metric for large non-financial companies. With
--companies, also checks each company's own latest 10-K for all metrics.

Thin entry point: the logic lives in finsight.catalog.coverage.
"""

import argparse
import json
import sys
from pathlib import Path

from finsight.catalog import load_catalog
from finsight.catalog.coverage import (
    FINANCIAL_FLAGS,
    company_status,
    comparison_group,
    frame_period,
    metric_coverage,
    share,
)
from finsight.config import ConfigError, get_sec_user_agent
from finsight.ingestion.sec import SecClient, download_company_facts, download_frame, load_frame

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--year", type=int, default=2025, help="calendar year (default 2025)")
    parser.add_argument("--min-assets", type=float, default=1e9, help="minimum total assets, USD")
    parser.add_argument("--companies", nargs="*", default=[], help="CIKs to check one by one")
    parser.add_argument("--refresh", action="store_true", help="re-download frames")
    args = parser.parse_args(argv)

    try:
        user_agent = get_sec_user_agent()
    except ConfigError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    catalog = load_catalog()
    cache: dict[tuple[str, str, str], set[int]] = {}

    with SecClient(user_agent) as client:
        def frame(tag: str, unit: str, period_type: str) -> dict[int, float]:
            path = download_frame(tag, unit, frame_period(period_type, args.year), client,
                                  RAW_DIR, force=args.refresh)
            return load_frame(path)

        def reporters(tag: str, unit: str, period_type: str) -> set[int]:
            key = (tag, unit, period_type)
            if key not in cache:
                cache[key] = set(frame(*key))
            return cache[key]

        assets = frame("Assets", "USD", "instant")
        financial = set().union(*(reporters(*flag) for flag in FINANCIAL_FLAGS))
        group = comparison_group(assets, financial, args.min_assets)
        coverage = metric_coverage(catalog, reporters)

        print(f"Comparison group: {len(group):,} non-financial companies with assets "
              f">= ${args.min_assets:,.0f} (of {len(assets):,} reporting assets), CY{args.year}")
        print(f"{'metric':28}{'by tag':>8}{'+ formula':>11}  may be absent")
        for name, m in catalog.items():
            by_tag, total = coverage[name]
            formula_pct = f"{share(total, group):>11}" if m.formulas else f"{'':>11}"
            print(f"{name:28}{share(by_tag, group):>8}{formula_pct}  {'yes' if m.may_be_absent else ''}")

        for cik in args.companies:
            facts = json.loads(download_company_facts(cik, client, RAW_DIR).read_bytes())
            status = company_status(facts, catalog)
            missing = [n for n, s in status.items() if s == "missing"]
            derived = [n for n, s in status.items() if s == "formula"]
            print(f"\n{facts.get('entityName', cik)}: {len(catalog) - len(missing)}/{len(catalog)} found")
            print(f"  by formula: {', '.join(derived) or 'none'}")
            print(f"  missing:    {', '.join(missing) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
