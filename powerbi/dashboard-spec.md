# Customer Churn Analysis — Power BI report specification

## Scope

Build a one-page descriptive cohort report from IBM's public **fictional** Telco Customer Churn sample. The report should state that it shows observed churn labels in historical sample data. It is not a model, a causal analysis, or a revenue-impact claim.

## 1. Import and prepare data

1. Download `Telco-Customer-Churn.csv` from the IBM source referenced in [`../data/README.md`](../data/README.md). Do not commit the downloaded file.
2. In Power BI Desktop, choose **Get data → Text/CSV**, select the file, then choose **Transform Data**.
3. Rename the query and resulting table to `Telco Churn`.
4. Set these data types before loading:
   - `customerID`: Text
   - `Churn`: Text
   - `Contract`: Text
   - `tenure`: Whole number
5. Confirm `Churn` contains only `Yes` and `No`; `Contract` contains only `Month-to-month`, `One year`, and `Two year`; and `tenure` ranges from 0 through 72.
6. Close and apply. Create the `Tenure Cohort` calculated column and the measures in [`measures.dax`](measures.dax).

## 2. Data model

Use one table only: `Telco Churn`. No relationships are needed. Do not place `customerID` or customer-level records on the report canvas.

## 3. Report layout

Use a restrained, readable layout with a white background, dark slate text, and one blue accent. Keep the report to one page.

### Header

- Title: **Customer Churn Cohort Analysis**
- Subtitle: `IBM fictional public sample · descriptive cohort rates`
- Small note: `Observed rate = customers labeled Churn = Yes ÷ customers in the selected cohort.`

### Slicers

Place two dropdown slicers at the top:

- `Contract`
- `Tenure Cohort`

Set both to affect every visual. Keep the default selection as All.

### KPI cards

Use four cards:

1. `[Customers]`
2. `[Churned Customers]`
3. `[Observed Churn Rate]` (format as percentage, two decimals)
4. `[Early-Tenure Observed Churn Rate]` (format as percentage, two decimals)

When a tenure slicer excludes `0–12 months`, the fourth card may be blank; that correctly reflects the current selection.

### Main visual

Create a clustered bar chart:

- **Y-axis:** `Contract`
- **X-axis:** `[Observed Churn Rate]`
- **Tooltip:** `[Customers]`, `[Churned Customers]`, `[Observed Churn Rate]`
- Sort: observed churn rate descending
- Title: `Observed churn rate by contract`

### Supporting table

Create a matrix:

- **Rows:** `Contract`, then `Tenure Cohort`
- **Values:** `[Customers]`, `[Churned Customers]`, `[Observed Churn Rate]`
- Format `[Observed Churn Rate]` as a percentage with two decimals.

### Footer disclosure

`Source: IBM Telco Customer Churn sample (fictional public data). Results are descriptive associations only; no causal effect, prediction, retention lift, or financial impact is claimed.`

## 4. Validation before sharing

With both slicers cleared, the report should show:

| Check | Expected value |
| --- | ---: |
| Customers | 7,043 |
| Churned customers | 1,869 |
| Observed churn rate | 26.54% |
| Month-to-month observed churn rate | 42.71% |
| One-year observed churn rate | 11.27% |
| Two-year observed churn rate | 2.83% |
| 0–12 month observed churn rate | 47.44% (1,037 of 2,186) |

If values do not match, confirm the source file, data types, table name, and calculated `Tenure Cohort` logic before publishing screenshots or a `.pbix` file.
