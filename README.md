# Customer Churn Analysis

[Open the live dashboard](https://poojasri234.github.io/customer-churn-analysis/)

**Tools:** Python/pandas · SQL/SQLite · cohort analysis · interactive HTML dashboard · Power BI report specification and DAX measures

A descriptive, reproducible cohort analysis of IBM's public Telco Customer Churn sample. The source is fictional and customer-level records are intentionally not redistributed in this repository.

## Business question

Which customer groups in the public IBM Telco sample show the highest observed churn, and where should a retention team investigate first?

## Approach

1. Validated required fields, unique customer IDs, duplicate rows, churn labels, contract categories, and the `0–72` month tenure range.
2. Calculated `observed churn rate = customers labelled Churn = Yes ÷ customers in the selected group`.
3. Recomputed contract and tenure rates in pandas and independently reconciled contract-level results with [SQLite queries](sql/churn_cohort_analysis.sql).
4. Exported aggregate findings only for the dashboard and review; no customer-level records are committed.

## Findings

- **26.54%** of the sample churned: **1,869 of 7,043** customers.
- Month-to-month customers had **42.71%** observed churn (**1,655 of 3,875**), compared with **11.27%** for one-year and **2.83%** for two-year contracts.
- Customers in their first **0–12 months** had **47.44%** observed churn (**1,037 of 2,186**).
- The early-tenure/month-to-month group was the sharpest descriptive signal: **51.35%** observed churn (**1,024 of 1,994**). This is a prioritisation signal, not proof that a contract type or tenure causes churn.

## Recommendation

Start with a controlled onboarding and plan-review experiment for newly acquired month-to-month customers. Randomly assign eligible customers to a new experience or standard treatment, then compare retention at an agreed horizon, offer cost per retained customer, complaints, and plan changes.

Investigate service, billing, support-contact, and customer-value data before deciding whether a contract-upgrade offer is appropriate.

## Potential business value — illustrative only

If an intervention prevented **10% of the 1,024 observed churn events** in the comparable early-tenure/month-to-month group, that arithmetic scenario equals about **102 fewer churn events** and would move observed cohort churn from **51.35% to roughly 46.2%** (about **5.1 percentage points**).

This is not a forecast or a claimed outcome. The sample has no offer exposure, causal evidence, customer value, margin, or time horizon, so it cannot support a monetary benefit estimate.

## Limitations

- IBM describes this as a fictional public sample; it does not represent an employer's customers or results.
- This is a descriptive historical comparison, not a predictive model or deployed retention programme.
- The observed differences may reflect customer mix, pricing, service experience, or variables not controlled here.
- A randomized holdout and operational data are required before claiming incremental retention or financial impact.

## SQL and dashboard evidence

- [`sql/churn_cohort_analysis.sql`](sql/churn_cohort_analysis.sql) — input-quality checks plus overall, contract, tenure, and contract-by-tenure cohort queries.
- [`analysis/churn_analysis.py`](analysis/churn_analysis.py) — reproducible validation and aggregate analysis.
- [`powerbi/`](powerbi/) — DAX measures and report specification. A completed `.pbix` file is not included.
- [`data/aggregate-findings.json`](data/aggregate-findings.json) — aggregate-only results.

## 3-minute interview walkthrough

- **0:00–0:25:** Frame this as a cohort-prioritisation question, not a predictive model.
- **0:25–1:00:** Describe schema, ID, label, contract, tenure, and duplicate validation.
- **1:00–1:40:** Explain the churn-rate formula and the month-to-month / early-tenure findings.
- **1:40–2:15:** Show how SQLite independently reconciles the pandas cohort rates.
- **2:15–2:45:** Recommend a randomized onboarding or plan-review test and explain the 102-event scenario is arithmetic only.
- **2:45–3:00:** With production data, add service, billing, support, price, margin, and treatment-exposure history.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
curl -L "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv" \
  -o data/Telco-Customer-Churn.csv
python analysis/churn_analysis.py --input data/Telco-Customer-Churn.csv
```

See [data/README.md](data/README.md) for source and handling notes.
