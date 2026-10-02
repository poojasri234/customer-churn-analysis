#!/usr/bin/env python3
"""Produce aggregate findings for the IBM Telco Customer Churn sample.

The repository intentionally does not include customer-level records. Download
the public CSV named ``Telco-Customer-Churn.csv`` from the IBM source linked in
the README, then run:

    python analysis/churn_analysis.py --input data/Telco-Customer-Churn.csv

The script validates the known public sample, calculates descriptive cohort
rates, independently reconciles contract rates with SQLite, and writes only an
aggregate JSON file. Findings are observed associations; this is not a churn
prediction model or a causal analysis.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "Telco-Customer-Churn.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "aggregate-findings.json"
SOURCE_URL = (
    "https://raw.githubusercontent.com/IBM/"
    "telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
)
SOURCE_REPOSITORY = "https://github.com/IBM/telco-customer-churn-on-icp4d"
CONTRACT_ORDER = ("Month-to-month", "One year", "Two year")
EXPECTED = {
    "records": 7043,
    "churned": 1869,
    "overall_rate": 26.54,
    "month_to_month_rate": 42.71,
    "one_year_rate": 11.27,
    "two_year_rate": 2.83,
    "early_tenure_rate": 47.44,
}


def require(condition: bool, message: str) -> None:
    """Raise a clear error even when Python runs with optimization enabled."""
    if not condition:
        raise ValueError(message)


def rounded_rate(churned: int, customers: int) -> float:
    require(customers > 0, "A cohort cannot have zero customers.")
    return round(100 * churned / customers, 2)


def load_and_validate(path: Path) -> pd.DataFrame:
    """Read the public sample and validate the fields used by this analysis."""
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}\n"
            f"Download the public IBM CSV from {SOURCE_URL} and rerun with --input."
        )

    data = pd.read_csv(path, dtype={"customerID": "string"})
    required_columns = {"customerID", "Churn", "Contract", "tenure"}
    require(
        required_columns.issubset(data.columns),
        f"Input is missing required columns: {sorted(required_columns - set(data.columns))}",
    )
    require(data["customerID"].notna().all(), "Customer IDs contain missing values.")
    require(not data["customerID"].duplicated().any(), "Customer IDs must be unique.")
    require(not data.duplicated().any(), "The input contains duplicate rows.")
    require(set(data["Churn"].dropna().unique()) == {"Yes", "No"}, "Unexpected churn labels.")
    require(
        set(data["Contract"].dropna().unique()) == set(CONTRACT_ORDER),
        "Unexpected contract categories.",
    )

    data = data.copy()
    data["tenure"] = pd.to_numeric(data["tenure"], errors="raise")
    require(data["tenure"].between(0, 72).all(), "Tenure must be between 0 and 72 months.")
    data["churn_flag"] = data["Churn"].eq("Yes").astype(int)
    return data


def contract_rates_pandas(data: pd.DataFrame) -> dict[str, float]:
    """Calculate cohort churn rates with pandas."""
    grouped = data.groupby("Contract", observed=True)["churn_flag"].agg(["sum", "count"])
    return {
        contract: rounded_rate(int(grouped.loc[contract, "sum"]), int(grouped.loc[contract, "count"]))
        for contract in CONTRACT_ORDER
    }


def contract_rates_sqlite(data: pd.DataFrame) -> dict[str, float]:
    """Independently recalculate cohort rates using a SQLite GROUP BY query."""
    with sqlite3.connect(":memory:") as connection:
        data[["Contract", "Churn"]].to_sql("customers", connection, index=False)
        rows = connection.execute(
            """
            SELECT Contract,
                   SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
                   COUNT(*) AS customers
            FROM customers
            GROUP BY Contract
            """
        ).fetchall()
    return {contract: rounded_rate(int(churned), int(customers)) for contract, churned, customers in rows}


def calculate(data: pd.DataFrame) -> dict[str, Any]:
    """Create a concise, reviewable aggregate analysis payload."""
    records = len(data)
    churned = int(data["churn_flag"].sum())
    overall_rate = rounded_rate(churned, records)
    pandas_contract_rates = contract_rates_pandas(data)
    sqlite_contract_rates = contract_rates_sqlite(data)
    require(pandas_contract_rates == sqlite_contract_rates, "Pandas and SQLite contract rates disagree.")

    early_tenure = data.loc[data["tenure"] <= 12]
    early_tenure_rate = rounded_rate(int(early_tenure["churn_flag"].sum()), len(early_tenure))

    calculated = {
        "records": records,
        "churned": churned,
        "overall_rate": overall_rate,
        "month_to_month_rate": pandas_contract_rates["Month-to-month"],
        "one_year_rate": pandas_contract_rates["One year"],
        "two_year_rate": pandas_contract_rates["Two year"],
        "early_tenure_rate": early_tenure_rate,
    }
    for key, expected_value in EXPECTED.items():
        require(calculated[key] == expected_value, f"Unexpected {key}: {calculated[key]}.")

    return {
        "project": {
            "title": "Customer Churn Analysis",
            "question": "Which customer cohorts show the highest observed churn in the IBM sample?",
            "tools": ["Python", "pandas", "SQLite"],
        },
        "source": {
            "name": "IBM Telco Customer Churn sample",
            "repository": SOURCE_REPOSITORY,
            "csv": SOURCE_URL,
            "scope": "Public fictional sample data. Customer-level records are intentionally not redistributed in this repository.",
        },
        "data_validation": [
            "Validated required fields, unique customer IDs, duplicate rows, churn labels, contract categories, and tenure range.",
            "Recomputed contract cohort rates with pandas and a separate SQLite GROUP BY query; the results reconciled.",
        ],
        "findings": [
            {
                "cohort": "All sample customers",
                "observed_churn_rate_percent": overall_rate,
                "detail": f"{churned:,} of {records:,} records are labeled Churn = Yes.",
            },
            {
                "cohort": "Month-to-month contract",
                "observed_churn_rate_percent": pandas_contract_rates["Month-to-month"],
            },
            {
                "cohort": "One-year contract",
                "observed_churn_rate_percent": pandas_contract_rates["One year"],
            },
            {
                "cohort": "Two-year contract",
                "observed_churn_rate_percent": pandas_contract_rates["Two year"],
            },
            {
                "cohort": "0–12 months of tenure",
                "observed_churn_rate_percent": early_tenure_rate,
            },
        ],
        "interpretation": (
            "These are descriptive observed associations in a fictional sample. They do not show that a contract type or tenure causes churn."
        ),
        "next_steps": [
            "Investigate early-tenure onboarding and service experience with qualitative feedback and additional operational data.",
            "Evaluate a retention offer with a randomized holdout before claiming incremental retention or financial impact.",
        ],
        "limitations": [
            "The IBM dataset is a fictional sample and does not represent an employer's customers or results.",
            "No predictive model, intervention, revenue uplift, savings, or causal effect is claimed.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to IBM's Telco-Customer-Churn.csv")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path for aggregate JSON output")
    args = parser.parse_args()

    findings = calculate(load_and_validate(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(findings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Aggregate findings written to {args.output}")


if __name__ == "__main__":
    main()
