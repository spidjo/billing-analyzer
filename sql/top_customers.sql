SELECT 
    subscriber_id,
    COUNT(*) AS call_count,
    ROUND(SUM(cost), 2) AS total_spent
FROM cdrs
GROUP BY subscriber_id
ORDER BY total_spent DESC
LIMIT 10;
