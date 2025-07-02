SELECT billing_date, cost 
FROM billing_records 
WHERE customer_id = (SELECT id FROM users WHERE username = ?) 
ORDER BY billing_date DESC;