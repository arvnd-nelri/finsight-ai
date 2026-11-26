"""Tests for finsight.catalog.coverage, on tiny made-up data (no network).

CIKs and values below are placeholders, not real companies or figures.
"""

import pytest

from finsight.catalog import load_catalog
from finsight.catalog.coverage import (
    company_status,
    comparison_group,
    frame_period,
    metric_coverage,
    share,
)

CATALOG_TOML = """
[revenue]
label = "Revenue"
statement = "income"
period_type = "duration"
unit = "USD"
subtractable = true
tags = ["Revenues"]

[cost_of_revenue]
label = "Cost of revenue"
statement = "income"
period_type = "duration"
unit = "USD"
subtractable = true
tags = ["CostOfRevenue"]

[gross_profit]
label = "Gross profit"
statement = "income"
period_type = "duration"
unit = "USD"
subtractable = true
tags = ["GrossProfit"]
formulas = ["revenue - cost_of_revenue"]

[total_liabilities]
label = "Total liabilities"
statement = "balance"
period_type = "instant"
unit = "USD"
subtractable = false
tags = ["Liabilities"]
formulas = ["LiabilitiesAndStockholdersEquity - StockholdersEquity"]
"""


@pytest.fixture
def catalog(tmp_path):
    path = tmp_path / "metrics.toml"
    path.write_text(CATALOG_TOML)
    return load_catalog(path)


# --- Small helpers ---------------------------------------------------------------


def test_frame_period():
    assert frame_period("duration", 2025) == "CY2025"
    assert frame_period("instant", 2025) == "CY2025Q4I"


def test_comparison_group_drops_financial_and_small_companies():
    assets = {1: 5e9, 2: 5e9, 3: 1e8}
    assert comparison_group(assets, financial={2}, min_assets=1e9) == {1}


def test_share():
    assert share({1, 2, 9}, {1, 2, 3, 4}) == 50.0  # 9 is outside the group
    assert share({1}, set()) == 0.0


# --- Coverage across companies -----------------------------------------------------


def test_metric_coverage_counts_tags_and_formulas(catalog):
    frames = {
        "Revenues": {1, 2, 3},
        "CostOfRevenue": {2, 3},
        "GrossProfit": {1},
        "Liabilities": {1},
        "LiabilitiesAndStockholdersEquity": {1, 2, 3},
        "StockholdersEquity": {2},
    }
    coverage = metric_coverage(catalog, lambda tag, unit, period: frames.get(tag, set()))
    assert coverage["gross_profit"] == ({1}, {1, 2, 3})  # 2 and 3 via the formula
    assert coverage["total_liabilities"] == ({1}, {1, 2})  # 3 lacks equity
    assert coverage["revenue"] == ({1, 2, 3}, {1, 2, 3})


# --- One company's own file -------------------------------------------------------


def fact(start, end, val, filed="2026-02-01", form="10-K"):
    entry = {"end": end, "val": val, "form": form, "filed": filed}
    if start:
        entry["start"] = start
    return {"units": {"USD": [entry]}}  # same shape as a real company-facts tag


def facts_file(gaap):
    return {"cik": 1, "entityName": "TEST CO", "facts": {"us-gaap": gaap}}


def test_company_status_tag_formula_and_missing(catalog):
    facts = facts_file({
        "Revenues": fact("2025-01-01", "2025-12-31", 100),
        "CostOfRevenue": fact("2025-01-01", "2025-12-31", 60),
        "LiabilitiesAndStockholdersEquity": fact(None, "2025-12-31", 500),
    })
    assert company_status(facts, catalog) == {
        "revenue": "tag",
        "cost_of_revenue": "tag",
        "gross_profit": "formula",
        "total_liabilities": "missing",  # equity not reported
    }


def test_company_status_ignores_quarters_and_older_filings(catalog):
    facts = facts_file({
        "Revenues": fact("2025-10-01", "2025-12-31", 30),  # a quarter, not the year
        "CostOfRevenue": fact("2024-01-01", "2024-12-31", 60, filed="2025-02-01"),  # old 10-K
        "Liabilities": fact(None, "2025-12-31", 400, form="10-Q"),  # not a 10-K
    })
    status = company_status(facts, catalog)
    assert status["revenue"] == "missing"
    assert status["cost_of_revenue"] == "missing"
    assert status["total_liabilities"] == "missing"


def test_company_status_accepts_leap_and_53_week_years(catalog):
    facts = facts_file({"Revenues": fact("2023-07-01", "2024-06-30", 100)})  # 365 days, leap
    assert company_status(facts, catalog)["revenue"] == "tag"
    facts = facts_file({"Revenues": fact("2024-09-29", "2025-10-04", 100)})  # 370 days
    assert company_status(facts, catalog)["revenue"] == "tag"


def test_company_without_10k_has_everything_missing(catalog):
    facts = facts_file({"Revenues": fact("2025-01-01", "2025-12-31", 100, form="10-Q")})
    assert set(company_status(facts, catalog).values()) == {"missing"}
