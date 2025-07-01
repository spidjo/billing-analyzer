SELECT 
    strftime('%Y-%m', start_time) AS month,
    ROUND(SUM(cost), 2) AS total_revenue
FROM cdrs
GROUP BY month
ORDER BY month;
