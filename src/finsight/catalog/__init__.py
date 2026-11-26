"""The metric catalog: our metric names mapped to SEC us-gaap tags.

The catalog lives in `metrics.toml` next to this file, so it can be read and
edited like a table. `load_catalog()` reads it and checks every entry, so a
typo in the file fails loudly instead of silently producing wrong data.
"""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

CATALOG_FILE = Path(__file__).with_name("metrics.toml")

STATEMENTS = {"income", "balance", "cash_flow"}
PERIOD_TYPES = {"duration", "instant"}
UNITS = {"USD", "USD/shares", "shares"}
_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
_TAG = re.compile(r"^[A-Z][A-Za-z0-9]*$")
_REQUIRED = {"label", "statement", "period_type", "unit", "subtractable", "tags"}
_OPTIONAL = {"may_be_absent", "formulas", "coverage_pct"}


class CatalogError(ValueError):
    """The catalog file has a missing, unknown, or inconsistent entry."""


@dataclass(frozen=True)
class Metric:
    name: str
    label: str
    statement: str
    period_type: str
    unit: str
    subtractable: bool
    tags: tuple[str, ...]
    may_be_absent: bool = False
    formulas: tuple[str, ...] = ()
    coverage_pct: float | None = None


def _check(name: str, entry: dict) -> Metric:
    def fail(problem: str) -> CatalogError:
        return CatalogError(f"metric {name!r}: {problem}")

    if not _NAME.match(name):
        raise fail("name must be snake_case")
    if missing := _REQUIRED - entry.keys():
        raise fail(f"missing fields {sorted(missing)}")
    if unknown := entry.keys() - _REQUIRED - _OPTIONAL:
        raise fail(f"unknown fields {sorted(unknown)}")
    if entry["statement"] not in STATEMENTS:
        raise fail(f"statement must be one of {sorted(STATEMENTS)}")
    if entry["period_type"] not in PERIOD_TYPES:
        raise fail(f"period_type must be one of {sorted(PERIOD_TYPES)}")
    if entry["unit"] not in UNITS:
        raise fail(f"unit must be one of {sorted(UNITS)}")

    tags = entry["tags"]
    if not tags or not all(isinstance(t, str) and t for t in tags):
        raise fail("tags must be a non-empty list of tag names")
    if len(set(tags)) != len(tags):
        raise fail("tags contain a duplicate")

    # Balance-sheet items are snapshots; the other statements are period totals.
    if (entry["statement"] == "balance") != (entry["period_type"] == "instant"):
        raise fail("balance-sheet metrics must be instant, others duration")
    # Quarterly subtraction is only valid for dollar totals over a period.
    if entry["subtractable"] and (entry["period_type"] == "instant" or entry["unit"] != "USD"):
        raise fail("only USD duration metrics can be subtractable")

    formulas = entry.get("formulas", [])
    if not isinstance(formulas, list) or not all(isinstance(f, str) for f in formulas):
        raise fail("formulas must be a list of strings")

    return Metric(
        name=name,
        label=entry["label"],
        statement=entry["statement"],
        period_type=entry["period_type"],
        unit=entry["unit"],
        subtractable=entry["subtractable"],
        tags=tuple(tags),
        may_be_absent=entry.get("may_be_absent", False),
        formulas=tuple(formulas),
        coverage_pct=entry.get("coverage_pct"),
    )


def formula_terms(formula: str) -> list[tuple[int, str]]:
    """Split "a - B + c" into [(+1, "a"), (-1, "B"), (+1, "c")]."""
    tokens = formula.split()
    if len(tokens) % 2 == 0 or any(op not in "+-" for op in tokens[1::2]):
        raise ValueError(f"formula must look like 'a + b - c': {formula!r}")
    signs = [1] + [1 if op == "+" else -1 for op in tokens[1::2]]
    return list(zip(signs, tokens[::2], strict=True))


def _check_formula(metric: Metric, formula: str, catalog: dict[str, Metric]) -> None:
    try:
        terms = formula_terms(formula)
    except ValueError as err:
        raise CatalogError(f"metric {metric.name!r}: {err}") from None
    for _, term in terms:
        if _NAME.match(term):
            if term == metric.name or term not in catalog:
                raise CatalogError(f"metric {metric.name!r}: formula uses unknown metric {term!r}")
            if catalog[term].unit != metric.unit:
                raise CatalogError(f"metric {metric.name!r}: formula mixes units ({term!r})")
        elif not _TAG.match(term):
            raise CatalogError(f"metric {metric.name!r}: formula term {term!r} is not a metric or tag")


def load_catalog(path: Path = CATALOG_FILE) -> dict[str, Metric]:
    """Read and validate the catalog; return metrics by name, in file order."""
    with path.open("rb") as f:
        data = tomllib.load(f)
    catalog = {name: _check(name, entry) for name, entry in data.items()}
    for metric in catalog.values():
        for formula in metric.formulas:
            _check_formula(metric, formula, catalog)
    return catalog
