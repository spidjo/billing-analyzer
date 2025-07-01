SELECT 
    strftime('%Y-%m', billing_date) AS month,
    ROUND(SUM(cost), 2) AS total_revenue
FROM cdrs
GROUP BY month
ORDER BY month;
