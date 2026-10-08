# Power BI build assets

This folder contains a reproducible report specification and DAX measures for the public IBM Telco Customer Churn sample. It does **not** contain a `.pbix` file or customer-level data.

To build the report, download the public CSV from the IBM source linked in [`../data/README.md`](../data/README.md), then follow [`dashboard-spec.md`](dashboard-spec.md). The source file remains local and is ignored by Git.

Files:

- [`measures.dax`](measures.dax) — calculated-column and measure definitions for a table named `Telco Churn`.
- [`dashboard-spec.md`](dashboard-spec.md) — import, data-model, validation, and visual layout instructions.

The resulting report should be labeled as a descriptive analysis of a fictional public sample. It must not be presented as a predictive model, a deployed retention program, or an employer result.
