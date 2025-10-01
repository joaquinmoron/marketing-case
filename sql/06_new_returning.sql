USE db_marketing;

DROP VIEW IF EXISTS v_first_order_month;
CREATE VIEW v_first_order_month AS
SELECT
  customer_unique_id,
  MIN(order_date)                           AS first_order_date,
  DATE_FORMAT(MIN(order_date), '%Y-%m')     AS first_order_month
FROM fact_orders
GROUP BY customer_unique_id;

DROP VIEW IF EXISTS `v_monthly_customer`;
CREATE VIEW `v_monthly_customer` AS
SELECT
  o.`order_month`,
  o.`customer_unique_id`,
  SUM(o.`items_revenue`) AS `revenue_month_customer`,
  CASE WHEN fo.`first_order_month` = o.`order_month` THEN 1 ELSE 0 END AS `is_new_month`
FROM `fact_orders` o
JOIN `v_first_order_month` fo
  ON fo.`customer_unique_id` = o.`customer_unique_id`
GROUP BY o.`order_month`, o.`customer_unique_id`;

DROP VIEW IF EXISTS `v_new_returning_monthly`;
CREATE VIEW `v_new_returning_monthly` AS
SELECT
  `order_month`                                  AS `year_month`,
  SUM(`is_new_month`)                            AS `new_customers`,
  COUNT(*) - SUM(`is_new_month`)                 AS `returning_customers`,
  SUM(CASE WHEN `is_new_month` = 1 THEN `revenue_month_customer` ELSE 0 END) AS `new_revenue`,
  SUM(CASE WHEN `is_new_month` = 0 THEN `revenue_month_customer` ELSE 0 END) AS `returning_revenue`
FROM `v_monthly_customer`
GROUP BY `order_month`;

DESCRIBE v_new_returning_monthly;

SELECT *
FROM v_new_returning_monthly
ORDER BY `year_month`   -- con backticks
LIMIT 12;

SELECT
  m.year_month,
  m.unique_customers,
  (nr.new_customers + nr.returning_customers) AS customers_split,
  m.revenue,
  (nr.new_revenue + nr.returning_revenue)   AS revenue_split
FROM v_orders_monthly AS m
JOIN v_new_returning_monthly AS nr
  ON nr.year_month = m.year_month
ORDER BY m.year_month
LIMIT 12;

SELECT * 
FROM v_new_returning_monthly
ORDER BY `year_month`
LIMIT 12;

SELECT COUNT(*) AS mismatches
FROM (
  SELECT 
    m.year_month,
    m.unique_customers,
    (nr.new_customers + nr.returning_customers) AS customers_split,
    m.revenue,
    (nr.new_revenue + nr.returning_revenue)     AS revenue_split
  FROM v_orders_monthly m
  JOIN v_new_returning_monthly nr
    ON nr.year_month = m.year_month
) x
WHERE x.unique_customers <> x.customers_split
   OR ABS(x.revenue - x.revenue_split) > 0.01;  -- tolerancia centavos

-- Totales de la partición New/Returning (deben ser consistentes con m.revenue)
SELECT 
  SUM(new_customers)        AS new_customers_total,
  SUM(returning_customers)  AS returning_customers_total,
  SUM(new_revenue)          AS new_revenue_total,
  SUM(returning_revenue)    AS returning_revenue_total
FROM v_new_returning_monthly;

-- (opcional) Totales de v_orders_monthly para comparar
SELECT 
  SUM(unique_customers) AS unique_customers_total,
  SUM(revenue)          AS revenue_total
FROM v_orders_monthly;


