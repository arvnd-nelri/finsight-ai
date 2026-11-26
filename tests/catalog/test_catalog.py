"""Tests for finsight.catalog: the metric catalog file and its checks."""

from collections import Counter

import pytest

from finsight.catalog import CatalogError, formula_terms, load_catalog

# --- The real catalog ----------------------------------------------------------


@pytest.fixture(scope="module")
def catalog():
    return load_catalog()


def test_catalog_has_40_metrics(catalog):
    assert len(catalog) == 40


def test_metrics_per_statement(catalog):
    counts = Counter(m.statement for m in catalog.values())
    assert counts == {"income": 14, "balance": 16, "cash_flow": 10}


def test_per_share_values_and_share_counts_are_not_subtractable(catalog):
    # Q4 EPS = annual EPS - 9-month EPS is wrong: the share count changes.
    for name in ["eps_basic", "eps_diluted", "basic_shares", "diluted_shares",
                 "dividends_per_share"]:
        assert not catalog[name].subtractable, name


def test_a_tag_maps_to_one_meaning(catalog):
    # The same tag under two metrics is only allowed for the combined
    # "basic and diluted" tags, which really do report both values.
    shared_ok = {"EarningsPerShareBasicAndDiluted",
                 "WeightedAverageNumberOfShareOutstandingBasicAndDiluted"}
    seen = Counter(t for m in catalog.values() for t in m.tags)
    assert {t for t, n in seen.items() if n > 1} <= shared_ok


def test_revenue_tags_follow_d008_priority(catalog):
    assert catalog["revenue"].tags[:2] == (
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    )


# --- Validation catches mistakes in the file ---------------------------------

VALID = """
[revenue]
label = "Revenue"
statement = "income"
period_type = "duration"
unit = "USD"
subtractable = true
tags = ["Revenues"]
"""


def load_text(tmp_path, text):
    path = tmp_path / "metrics.toml"
    path.write_text(text)
    return load_catalog(path)


def test_valid_entry_loads(tmp_path):
    metric = load_text(tmp_path, VALID)["revenue"]
    assert metric.tags == ("Revenues",)
    assert metric.may_be_absent is False and metric.formulas == ()


@pytest.mark.parametrize(
    "old, new, message",
    [
        ('statement = "income"', 'statement = "incme"', "statement"),
        ('unit = "USD"', 'unit = "EUR"', "unit"),
        ('tags = ["Revenues"]', "tags = []", "tags"),
        ('tags = ["Revenues"]', 'tags = ["Revenues", "Revenues"]', "duplicate"),
        ('label = "Revenue"\n', "", "missing"),
        ('label = "Revenue"', 'label = "Revenue"\ncoverage = 1', "unknown"),
        ('label = "Revenue"', 'label = "Revenue"\nformulas = "Revenues"', "list of strings"),
        ("[revenue]", "[Revenue]", "snake_case"),
        ('period_type = "duration"', 'period_type = "instant"', "instant"),
        ('unit = "USD"', 'unit = "USD/shares"', "subtractable"),
    ],
)
def test_invalid_entry_is_rejected(tmp_path, old, new, message):
    with pytest.raises(CatalogError, match=message):
        load_text(tmp_path, VALID.replace(old, new))


# --- Fallback formulas -----------------------------------------------------------


def test_formula_terms_are_parsed_with_signs():
    assert formula_terms("revenue - cost_of_revenue + OtherTag") == [
        (1, "revenue"), (-1, "cost_of_revenue"), (1, "OtherTag"),
    ]


@pytest.mark.parametrize("bad", ["revenue -", "revenue * 2", "- revenue", ""])
def test_malformed_formula_is_rejected(bad):
    with pytest.raises(ValueError):
        formula_terms(bad)


def test_real_formulas_found_by_the_coverage_survey(catalog):
    assert catalog["gross_profit"].formulas == ("revenue - cost_of_revenue",)
    assert catalog["sga"].formulas == (
        "SellingAndMarketingExpense + GeneralAndAdministrativeExpense",  # e.g. Microsoft
    )


def test_total_liabilities_subtracts_equity_including_minority_owners_first(catalog):
    # Subtracting parent-only equity first would overstate liabilities for
    # companies with minority owners (Walmart: by $6.3B).
    first = catalog["total_liabilities"].formulas[0]
    assert first.endswith("- StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")


@pytest.mark.parametrize(
    "formula, message",
    [
        ('"revenue - unknown_metric"', "unknown metric"),
        ('"revenue2 - revenue"', "unknown metric"),  # refers to itself
        ('"Revenues - eps_basic"', "mixes units"),
        ('"Revenues - bad-tag"', "not a metric or tag"),
    ],
)
def test_invalid_formula_is_rejected(tmp_path, formula, message):
    eps = (VALID.replace("[revenue]", "[eps_basic]")
           .replace('unit = "USD"', 'unit = "USD/shares"')
           .replace("subtractable = true", "subtractable = false"))
    with_formula = VALID.replace("[revenue]", "[revenue2]") + f"formulas = [{formula}]\n"
    with pytest.raises(CatalogError, match=message):
        load_text(tmp_path, VALID + eps + with_formula)
