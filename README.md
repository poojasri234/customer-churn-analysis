# Customer Churn Analysis

[View the live dashboard](https://poojasri234.github.io/customer-churn-analysis/)

This project uses IBM's public Telco Customer Churn sample to identify customer groups that deserve retention-team attention. IBM describes the dataset as fictional, and customer-level records are not included here.

## Question

Which cohorts have the highest observed churn, and where would I start investigating retention?

## Method

- Validated required fields, customer IDs, duplicates, churn labels, contract categories, and the `0–72` month tenure range.
- Defined observed churn rate as `customers labelled Churn = Yes ÷ customers in the cohort`.
- Analysed contract, tenure, and contract-by-tenure cohorts in pandas.
- Reconciled contract-level results with [SQLite](sql/churn_cohort_analysis.sql) and published aggregate results only.

## Results

- **1,869 of 7,043 customers (26.54%)** were labelled as churned.
- Month-to-month customers had **42.71%** observed churn (**1,655 of 3,875**), versus **11.27%** for one-year and **2.83%** for two-year contracts.
- Customers in their first 12 months had **47.44%** observed churn (**1,037 of 2,186**).
- The early-tenure, month-to-month cohort had the highest useful signal: **51.35%** observed churn (**1,024 of 1,994**).

These are descriptive patterns, not proof that contract type or tenure causes churn.

## Recommended next step

Test a better onboarding or plan-review journey with a randomized group of newly acquired month-to-month customers. Track retention at a defined horizon, offer cost per retained customer, complaints, and plan changes. Investigate service, billing, support-contact, and customer-value data before choosing a contract-upgrade offer.

For scale only, preventing 10% of the 1,024 observed churn events in a comparable cohort would mean about **102 fewer churn events** and a cohort rate near **46.2%**. The dataset cannot show whether that outcome is achievable or what it would be worth financially.

## Notes on the data

- This is a fictional public sample, not employer data.
- The analysis is descriptive; it is not a predictive model or deployed programme.
- Customer mix, pricing, and service experience may explain the observed gaps.
- A randomized holdout and operational data are needed before claiming incremental retention or financial impact.

## Project files

- [SQL cohort checks](sql/churn_cohort_analysis.sql)
- [Python analysis](analysis/churn_analysis.py)
- [Power BI measures and report plan](powerbi/)
- [Aggregate findings](data/aggregate-findings.json)

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
curl -L "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv" \
  -o data/Telco-Customer-Churn.csv
python analysis/churn_analysis.py --input data/Telco-Customer-Churn.csv
```

[Data notes](data/README.md) cover the source and handling rules.
