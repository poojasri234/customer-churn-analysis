-- Customer Churn Analysis — SQLite validation and cohort queries
--
-- Import IBM's public Telco-Customer-Churn.csv into a table named telco_churn.
-- The raw file is intentionally not committed to this repository. See data/README.md.
--
-- Expected source fields used here: customerID, Churn, Contract, tenure.
-- The queries are descriptive only. Churn rate means rows labeled `Churn = Yes`
-- divided by the rows in each selected cohort.

-- -----------------------------------------------------------------------------
-- 1. Source quality checks
-- -----------------------------------------------------------------------------

-- Expected for the cited IBM sample: 7,043 rows and 7,043 distinct customer IDs.
SELECT
    COUNT(*) AS rows_loaded,
    COUNT(DISTINCT "customerID") AS unique_customer_ids,
    COUNT(*) - COUNT(DISTINCT "customerID") AS duplicate_customer_id_rows
FROM telco_churn;

-- This result should be empty for the cited sample.
SELECT
    "customerID",
    COUNT(*) AS rows_per_customer_id
FROM telco_churn
GROUP BY "customerID"
HAVING COUNT(*) > 1;

-- Expected labels: Yes and No only.
SELECT
    "Churn" AS churn_label,
    COUNT(*) AS customers
FROM telco_churn
GROUP BY "Churn"
ORDER BY churn_label;

-- Expected contracts: Month-to-month, One year, and Two year only.
SELECT
    "Contract" AS contract,
    COUNT(*) AS customers
FROM telco_churn
GROUP BY "Contract"
ORDER BY
    CASE "Contract"
        WHEN 'Month-to-month' THEN 1
        WHEN 'One year' THEN 2
        WHEN 'Two year' THEN 3
        ELSE 4
    END;

-- Expected tenure range for the cited sample: 0 through 72 months.
SELECT
    MIN(CAST("tenure" AS INTEGER)) AS minimum_tenure_months,
    MAX(CAST("tenure" AS INTEGER)) AS maximum_tenure_months
FROM telco_churn;

-- -----------------------------------------------------------------------------
-- 2. Overall observed churn rate
-- Expected for the cited IBM sample: 7,043 customers; 1,869 churned; 26.54%.
-- -----------------------------------------------------------------------------
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN "Churn" = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN "Churn" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS observed_churn_rate_percent
FROM telco_churn;

-- -----------------------------------------------------------------------------
-- 3. Contract cohorts
-- Expected rates: Month-to-month 42.71%; One year 11.27%; Two year 2.83%.
-- -----------------------------------------------------------------------------
SELECT
    "Contract" AS contract,
    COUNT(*) AS customers,
    SUM(CASE WHEN "Churn" = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN "Churn" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS observed_churn_rate_percent
FROM telco_churn
GROUP BY "Contract"
ORDER BY
    CASE "Contract"
        WHEN 'Month-to-month' THEN 1
        WHEN 'One year' THEN 2
        WHEN 'Two year' THEN 3
        ELSE 4
    END;

-- -----------------------------------------------------------------------------
-- 4. Tenure cohorts
-- The 0–12 month result should be 1,037 churned of 2,186 customers = 47.44%.
-- -----------------------------------------------------------------------------
WITH cohort_rows AS (
    SELECT
        CASE
            WHEN CAST("tenure" AS INTEGER) BETWEEN 0 AND 12 THEN '0–12 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 13 AND 24 THEN '13–24 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 25 AND 48 THEN '25–48 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 49 AND 72 THEN '49–72 months'
            ELSE 'Outside expected range'
        END AS tenure_cohort,
        "Churn" AS churn_label
    FROM telco_churn
)
SELECT
    tenure_cohort,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_label = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_label = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS observed_churn_rate_percent
FROM cohort_rows
GROUP BY tenure_cohort
ORDER BY
    CASE tenure_cohort
        WHEN '0–12 months' THEN 1
        WHEN '13–24 months' THEN 2
        WHEN '25–48 months' THEN 3
        WHEN '49–72 months' THEN 4
        ELSE 5
    END;

-- -----------------------------------------------------------------------------
-- 5. Contract × tenure-cohort aggregate export
-- This query reproduces the aggregate-only structure used by dashboard/data.json.
-- -----------------------------------------------------------------------------
WITH cohort_rows AS (
    SELECT
        "Contract" AS contract,
        CASE
            WHEN CAST("tenure" AS INTEGER) BETWEEN 0 AND 12 THEN '0–12 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 13 AND 24 THEN '13–24 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 25 AND 48 THEN '25–48 months'
            WHEN CAST("tenure" AS INTEGER) BETWEEN 49 AND 72 THEN '49–72 months'
            ELSE 'Outside expected range'
        END AS tenure_cohort,
        "Churn" AS churn_label
    FROM telco_churn
)
SELECT
    contract,
    tenure_cohort,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn_label = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN churn_label = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS observed_churn_rate_percent
FROM cohort_rows
GROUP BY contract, tenure_cohort
ORDER BY
    CASE contract
        WHEN 'Month-to-month' THEN 1
        WHEN 'One year' THEN 2
        WHEN 'Two year' THEN 3
        ELSE 4
    END,
    CASE tenure_cohort
        WHEN '0–12 months' THEN 1
        WHEN '13–24 months' THEN 2
        WHEN '25–48 months' THEN 3
        WHEN '49–72 months' THEN 4
        ELSE 5
    END;
