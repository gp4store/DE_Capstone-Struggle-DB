
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    LEFT(REGEXP_REPLACE(phone, '[^0-9]', ''), 10) as phone,
    registration_date,
    loyalty_points
FROM myDataSource
