SELECT 
    YEAR(s.order_date) as year,
    MONTH(s.order_date) as month,
    DATE_FORMAT(s.order_date, 'yyyy-MM') as year_month,
    COUNT(DISTINCT s.customer_id) as unique_customers,
    COUNT(*) as total_orders,
    SUM(s.quantity) as total_items_sold,
    SUM(s.total_amount) as monthly_income,
    ROUND(AVG(s.total_amount), 2) as avg_order_value,
    SUM(s.quantity * p.price) as calculated_revenue
FROM sales_transaction s
INNER JOIN product p ON s.product_id = p.product_id
WHERE s.order_status != 'cancelled'
GROUP BY 
    YEAR(s.order_date), 
    MONTH(s.order_date),
    DATE_FORMAT(s.order_date, 'yyyy-MM')
ORDER BY year DESC, month DESC
