-- SnowCost: Synthetic Transaction Data
-- Purpose: Seed 10,000 synthetic transactions.
-- Run once on a fresh project database.
-- Re-running is blocked if the raw table already contains data.

USE WAREHOUSE SNOWCOST_WH;
USE DATABASE SNOWCOST;
USE SCHEMA RAW;

-- Safety check: prevent accidental duplicate seeding.
EXECUTE IMMEDIATE $$
DECLARE
    existing_rows NUMBER;
    seed_error EXCEPTION (
        -20001,
        'RAW.TRANSACTIONS is not empty. Seeding aborted to prevent duplicate data.'
    );
BEGIN
    SELECT COUNT(*)
      INTO :existing_rows
      FROM SNOWCOST.RAW.TRANSACTIONS;

    IF (existing_rows > 0) THEN
        RAISE seed_error;
    END IF;

    INSERT INTO SNOWCOST.RAW.TRANSACTIONS (
        TRANSACTION_ID,
        CUSTOMER_ID,
        TRANSACTION_TS,
        AMOUNT,
        CURRENCY,
        MERCHANT_CATEGORY,
        COUNTRY_CODE,
        STATUS,
        IS_SUSPICIOUS
    )
    SELECT
        UUID_STRING(),
        'C' || LPAD(UNIFORM(1, 500, RANDOM())::VARCHAR, 5, '0'),
        DATEADD(
            SECOND,
            -UNIFORM(0, 15552000, RANDOM()),
            CURRENT_TIMESTAMP()
        ),
        ROUND(UNIFORM(100, 250000, RANDOM()) / 100.0, 2),
        'INR',
        CASE UNIFORM(1, 6, RANDOM())
            WHEN 1 THEN 'GROCERY'
            WHEN 2 THEN 'TRAVEL'
            WHEN 3 THEN 'ONLINE_RETAIL'
            WHEN 4 THEN 'DINING'
            WHEN 5 THEN 'FUEL'
            ELSE 'UTILITIES'
        END,
        'IN',
        CASE
            WHEN UNIFORM(1, 100, RANDOM()) <= 5 THEN 'DECLINED'
            ELSE 'SETTLED'
        END,
        UNIFORM(1, 100, RANDOM()) <= 2
    FROM TABLE(GENERATOR(ROWCOUNT => 10000));
END;
$$;

-- Verify seeded data
SELECT
    COUNT(*) AS TOTAL_TRANSACTIONS,
    COUNT(DISTINCT TRANSACTION_ID) AS UNIQUE_TRANSACTION_IDS,
    MIN(TRANSACTION_TS) AS EARLIEST_TRANSACTION,
    MAX(TRANSACTION_TS) AS LATEST_TRANSACTION
FROM SNOWCOST.RAW.TRANSACTIONS;
