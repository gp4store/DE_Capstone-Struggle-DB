
SELECT 
    p.brand,
    SUM(s.total_amount) as total_revenue,
    COUNT(*) as total_orders
FROM sales_transaction s
INNER JOIN product p ON s.product_id = p.product_id
WHERE s.order_status IN ('completed', 'shipped', 'delivered')
GROUP BY p.brand
ORDER BY total_revenue DESC
LIMIT 10
