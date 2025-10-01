USE db_marketing;

CREATE OR REPLACE VIEW v_orders_daily AS
SELECT
  d.date_key                                AS order_date,
  COUNT(DISTINCT f.order_id)                AS orders,
  COUNT(DISTINCT f.customer_unique_id)      AS unique_customers,
  SUM(COALESCE(f.items_revenue, 0))         AS revenue,
  SUM(COALESCE(f.payment_total, 0))         AS payment_total,
  SUM(COALESCE(f.freight, 0))               AS freight,
  SUM(COALESCE(f.n_items, 0))               AS items
FROM dim_date d
LEFT JOIN fact_orders f
  ON f.order_date = d.date_key
GROUP BY d.date_key;

-- debe dar 714 (mismo conteo que dim_date)
SELECT COUNT(*) AS days FROM v_orders_daily;

-- los totales deben igualar a fact_orders (≈ 96.470/13.220.248,93/15.421.082,85/110.189 según tus sumas)
SELECT
  SUM(orders)          AS orders_total,
  SUM(revenue)         AS revenue_total,
  SUM(payment_total)   AS payment_total,
  SUM(items)           AS items_total
FROM v_orders_daily;

SELECT * FROM v_orders_daily ORDER BY order_date LIMIT 10;
