# SnowCost — Snowflake Analytics & Query Performance

SnowCost is a portfolio project demonstrating a Snowflake-based data pipeline for synthetic transaction data, data-quality validation, analytical data marts, and query-performance analysis.

The project uses Snowflake SQL to transform raw transactions into clean analytical tables, validate aggregate consistency, and compare direct aggregation against a pre-aggregated summary mart.

## Project Objectives

- Build a layered data pipeline using Snowflake.
- Generate and analyze 10,000 synthetic financial transactions.
- Clean and deduplicate transaction records.
- Create analytical marts for daily transaction and merchant-category reporting.
- Validate data quality and reconcile transaction counts.
- Inspect query history, scanned data, partitions, and clustering information.
- Compare query execution times for direct aggregation and pre-aggregated reporting.

## Architecture

```text
Synthetic Transactions
        |
        v
SNOWCOST.RAW.TRANSACTIONS
        |
        v
SNOWCOST.CORE.TRANSACTIONS_CLEAN
        |
        +------------------------------+
        |                              |
        v                              v
MARTS.DAILY_TRANSACTION_SUMMARY   MARTS.DAILY_CATEGORY_SUMMARY
        |                              |
        +---------------+--------------+
                        |
                        v
              Data Quality & Audit
                        |
                        v
              Performance Analysis
```

## Technology Stack

- **Data warehouse:** Snowflake
- **Query language:** SQL
- **Development environment:** VS Code and Snowflake Snowsight
- **Data modeling:** Raw, core, and mart layers
- **Monitoring:** Snowflake Query History, query profiles, table metadata, and clustering information

## Repository Structure

```text
snowcost/
├── data/
├── docs/
├── src/
├── tests/
├── sql/
│   ├── 01_setup.sql
│   ├── 02_seed_data.sql
│   ├── 03_analytics.sql
│   ├── 04_data_quality.sql
│   └── 05_performance_monitoring.sql
├── README.md
└── .gitignore
```

## Data Pipeline

### 1. Setup

`sql/01_setup.sql`

Creates the SnowCost warehouse, database, schemas, and raw transaction table.

### 2. Seed data

`sql/02_seed_data.sql`

Generates 10,000 synthetic transaction records with randomized customers, transaction amounts, timestamps, merchant categories, transaction statuses, and suspicious-transaction flags. To prevent accidental duplicate seeding, the script runs only when `SNOWCOST.RAW.TRANSACTIONS` is empty and aborts if the table already contains rows. Because the data is randomized, separate fresh runs may produce different records and performance measurements.

### 3. Analytics

`sql/03_analytics.sql`

Creates the following tables:

- `SNOWCOST.CORE.TRANSACTIONS_CLEAN` — standardized and deduplicated transaction data.
- `SNOWCOST.MARTS.DAILY_TRANSACTION_SUMMARY` — daily transaction counts, amounts, average amounts, suspicious counts, and declined counts by country and currency.
- `SNOWCOST.MARTS.DAILY_CATEGORY_SUMMARY` — daily transaction metrics by merchant category.

The analytics script rebuilds derived tables using `CREATE OR REPLACE TABLE`.

### 4. Data quality

`sql/04_data_quality.sql`

Checks required transaction fields, validates amounts and statuses, reconciles transaction counts, and records reconciliation results in `SNOWCOST.AUDIT.DATA_QUALITY_AUDIT`.

### 5. Performance monitoring

`sql/05_performance_monitoring.sql`

Inspects recent query history, execution times, bytes scanned, table metadata, clustering information, and saved performance measurements.

## Validation Results

The following results were observed in the development Snowflake environment:

| Validation | Result |
|---|---:|
| Raw transaction rows | 10,000 |
| Clean transaction rows | 10,000 |
| Daily mart represented transactions | 10,000 |
| Category mart represented transactions | 10,000 |
| Aggregate mismatches after aligning date filters | 0 |
| Duplicate query IDs in the performance audit after cleanup | 0 |

The count totals for the marts represent the sum of their aggregated `TRANSACTION_COUNT` columns, not the physical number of rows in each mart.

## Query Performance Experiment

Two equivalent daily category queries were compared using the core table and the pre-aggregated category mart.

| Metric | Direct aggregation | Category mart |
|---|---:|---:|
| Observed execution time | 137 ms | 67 ms |
| Observed latency reduction | — | 51.1% |

The category-mart query was 70 ms faster in the observed test.

These are single-run observations on a small dataset. Both queries were cache-assisted, and their scan statistics differed. The results do not establish a guaranteed or generalizable performance improvement.

## Running the Project

1. Set up a Snowflake account and select a role with the required warehouse, database, schema, and table privileges.
2. Open the scripts in `sql/` using Snowsight or another Snowflake SQL client.
3. Run `01_setup.sql`.
4. Run `02_seed_data.sql` once on a fresh project database.
5. Run `03_analytics.sql`.
6. Run `04_data_quality.sql`.
7. Run `05_performance_monitoring.sql`.
8. Inspect the query profiles and validation outputs.

**Important:** The analytics script replaces its derived tables. The seed script appends rows and should not be rerun against an already populated raw table without an intentional reset plan.

## Limitations and Future Improvements

- Use deterministic synthetic data to make experiments reproducible.
- Add automated tests for invalid data and aggregate consistency.
- Implement a repeatable refresh strategy for the analytical marts.
- Capture query-performance measurements automatically with deduplication safeguards.
- Compare repeated cold-cache and warm-cache executions on a larger dataset.
- Evaluate cost and performance across larger workloads before making scaling claims.

## Author

Manoj Gangula
