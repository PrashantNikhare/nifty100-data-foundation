-- Nifty100 Data Foundation
-- Sprint 1 - Exploratory Queries

-- 1. Total number of companies
SELECT COUNT(*) AS total_companies
FROM companies;


-- 2. Company list with basic information
SELECT
    id,
    company_name,
    website
FROM companies
ORDER BY company_name;


-- 3. Profit and loss row count by company
SELECT
    company_id,
    COUNT(*) AS record_count
FROM profitandloss
GROUP BY company_id
ORDER BY record_count DESC;


-- 4. Year coverage by company
SELECT
    company_id,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(year) AS year_count
FROM profitandloss
GROUP BY company_id
ORDER BY company_id;


-- 5. Companies with fewer than 5 years of data
SELECT
    company_id,
    COUNT(year) AS year_count
FROM profitandloss
GROUP BY company_id
HAVING COUNT(year) < 5
ORDER BY year_count;


-- 6. Latest available stock price for each company
SELECT
    company_id,
    MAX(date) AS latest_date
FROM stock_prices
GROUP BY company_id
ORDER BY company_id;


-- 7. Companies with financial ratio data
SELECT
    company_id,
    COUNT(*) AS ratio_records
FROM financial_ratios
GROUP BY company_id
ORDER BY ratio_records DESC;


-- 8. Average net profit margin by company
SELECT
    company_id,
    ROUND(AVG(net_profit_margin_pct), 2) AS avg_net_profit_margin
FROM financial_ratios
WHERE net_profit_margin_pct IS NOT NULL
GROUP BY company_id
ORDER BY avg_net_profit_margin DESC;


-- 9. Companies with the highest market capitalization
SELECT
    company_id,
    market_cap
FROM market_cap
ORDER BY market_cap DESC
LIMIT 10;


-- 10. Sector-wise company count
SELECT
    sector,
    COUNT(*) AS company_count
FROM sectors
GROUP BY sector
ORDER BY company_count DESC;