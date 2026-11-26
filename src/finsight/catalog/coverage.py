"""Measure how well the metric catalog finds each metric.

Two complementary checks (task 2.3b):

- **Coverage across many companies** (`metric_coverage`): for each metric,
  which companies report one of its tags or all parts of one of its
  formulas, according to SEC frames (one tag, one period, every company).
- **Company check** (`company_status`): for one company's own facts file,
  is each metric found in its latest 10-K, and how (tag or formula)?

Both are pure functions over already-downloaded data, so they are easy to
test; `scripts/check_catalog_coverage.py` does the downloading.
"""

from collections.abc import Callable
from datetime import date

from finsight.catalog import Metric, formula_terms

# Tags that (almost) only banks, insurers, lenders, funds, and brokers report.
# Frames carry no industry code, so these approximate "financial company".
FINANCIAL_FLAGS: tuple[tuple[str, str, str], ...] = (  # (tag, unit, period_type)
    ("Deposits", "USD", "instant"),
    ("InterestAndDividendIncomeOperating", "USD", "duration"),
    ("PremiumsEarnedNet", "USD", "duration"),
    ("LiabilityForFuturePolicyBenefits", "USD", "instant"),
    ("LoansAndLeasesReceivableNetReportedAmount", "USD", "instant"),
    ("InvestmentOwnedAtFairValue", "USD", "instant"),
)

# Annual periods are 365 or 366 days, or 364/371 for 52/53-week years.
ANNUAL_DAYS = range(350, 381)

# (tag, unit, period_type) -> CIKs reporting it
Reporters = Callable[[str, str, str], set[int]]


def frame_period(period_type: str, year: int) -> str:
    """Frame name for a calendar year: duration -> "CY2025", instant -> "CY2025Q4I"."""
    return f"CY{year}" if period_type == "duration" else f"CY{year}Q4I"


def comparison_group(
    assets: dict[int, float], financial: set[int], min_assets: float = 1e9
) -> set[int]:
    """Non-financial companies with total assets of at least `min_assets`."""
    return {cik for cik, value in assets.items() if cik not in financial and value >= min_assets}


def metric_coverage(
    catalog: dict[str, Metric], reporters: Reporters
) -> dict[str, tuple[set[int], set[int]]]:
    """For each metric: (companies found by a tag, companies found by a tag or formula)."""
    result: dict[str, tuple[set[int], set[int]]] = {}

    def covered(name: str) -> tuple[set[int], set[int]]:
        if name not in result:
            m = catalog[name]
            by_tag = set().union(*(reporters(t, m.unit, m.period_type) for t in m.tags))
            total = set(by_tag)
            for formula in m.formulas:
                parts = [
                    covered(term)[1] if term in catalog else reporters(term, m.unit, m.period_type)
                    for _, term in formula_terms(formula)
                ]
                total |= set.intersection(*parts)
            result[name] = (by_tag, total)
        return result[name]

    for name in catalog:
        covered(name)
    return result


def share(companies: set[int], group: set[int]) -> float:
    """Percentage of `group` that is in `companies`, rounded to 0.1."""
    return round(100 * len(companies & group) / len(group), 1) if group else 0.0


def company_status(facts: dict, catalog: dict[str, Metric]) -> dict[str, str]:
    """For one company-facts file: "tag", "formula", or "missing" per metric,
    judged on the latest 10-K (full fiscal year, or the year-end snapshot)."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    tenk = [e for t in gaap.values() for u in t["units"].values() for e in u
            if e.get("form") == "10-K"]
    if not tenk:
        return dict.fromkeys(catalog, "missing")
    filed = max(e["filed"] for e in tenk)
    year_end = max(e["end"] for e in tenk if e["filed"] == filed)

    def reported(tag: str, unit: str, period_type: str) -> bool:
        for e in gaap.get(tag, {}).get("units", {}).get(unit, []):
            if e.get("form") != "10-K" or e["filed"] != filed or e["end"] != year_end:
                continue
            if period_type == "instant" and "start" not in e:
                return True
            if period_type == "duration" and "start" in e:
                days = (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days
                if days in ANNUAL_DAYS:
                    return True
        return False

    status: dict[str, str] = {}

    def found(name: str) -> str:
        if name not in status:
            m = catalog[name]
            if any(reported(t, m.unit, m.period_type) for t in m.tags):
                status[name] = "tag"
            elif any(
                all(found(term) != "missing" if term in catalog
                    else reported(term, m.unit, m.period_type)
                    for _, term in formula_terms(formula))
                for formula in m.formulas
            ):
                status[name] = "formula"
            else:
                status[name] = "missing"
        return status[name]

    for name in catalog:
        found(name)
    return status
