# Customer Churn Analysis

**Python · pandas · SQLite · Cohort analysis**

A concise, reproducible analysis of IBM's public Telco Customer Churn sample. The work answers one focused question: **which customer cohorts have the highest observed churn in this sample?**

The repository contains code and aggregate findings only. It does not redistribute customer-level data.

## Executive findings

| Cohort | Observed churn rate |
| --- | ---: |
| All 7,043 sample customers | **26.54%** (1,869 labeled `Churn = Yes`) |
| Month-to-month contract | **42.71%** |
| One-year contract | **11.27%** |
| Two-year contract | **2.83%** |
| 0–12 months of tenure | **47.44%** |

The findings identify cohorts worth investigating. They are **observed associations**, not proof that contract type or tenure causes churn.

## What I did

1. Validated required fields, unique customer IDs, duplicate rows, churn labels, contract categories, and tenure values.
2. Calculated observed churn as customers labeled `Yes` divided by all customers in each cohort.
3. Recomputed contract rates with pandas and an independent SQLite `GROUP BY` query to confirm the results reconcile.
4. Exported only aggregate findings to JSON for review and portfolio use.

## Repository layout

```text
customer-churn-analysis/
├── analysis/
│   └── churn_analysis.py       # Reproducible analysis and validation
├── data/
│   ├── README.md               # Source and data-handling notes
│   └── aggregate-findings.json # Aggregate output; no customer-level data
├── requirements.txt
└── README.md
```

## Reproduce the analysis

Use Python 3.10 or later.

```bash
git clone <your-fork-url>
cd customer-churn-analysis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
curl -L "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv" \
  -o data/Telco-Customer-Churn.csv
python analysis/churn_analysis.py --input data/Telco-Customer-Churn.csv
```

The script writes `data/aggregate-findings.json`. The downloaded CSV is ignored by Git so the repository remains free of customer-level records.

## Data source and scope

The source is the public [IBM Telco Customer Churn sample](https://github.com/IBM/telco-customer-churn-on-icp4d). IBM describes the sample as fictional. It is used here to demonstrate data validation, cohort analysis, and clear communication of descriptive results.

This is not a deployed retention program or a predictive model. No revenue, savings, churn reduction, or causal impact is claimed.

## Interview-ready explanation

> I validated the public IBM sample, then calculated churn rates by contract and early-tenure cohorts. I independently reconciled contract rates with a SQLite query. The analysis shows where churn is concentrated in the sample, but I would test any retention idea with a control group before claiming an impact.
