USE db_marketing;

CREATE OR REPLACE VIEW v_kpi_daily AS
SELECT
  order_date,
  orders,
  unique_customers,
  revenue,
  payment_total,
  items,
  -- ticket medio (Average Order Value)
  CASE WHEN orders > 0 THEN revenue / orders ELSE 0 END AS aov,
  -- items por orden
  CASE WHEN orders > 0 THEN items / orders ELSE 0 END AS items_per_order
FROM v_orders_daily;

USE db_marketing;

DROP VIEW IF EXISTS v_kpi_monthly;
CREATE VIEW v_kpi_monthly AS
SELECT
  m.`year_month`,
  m.`orders`,
  m.`unique_customers`,
  m.`revenue`,
  m.`payment_total`,
  m.`items`,
  -- ticket medio (AOV)
  CASE WHEN m.`orders` > 0 THEN m.`revenue` / m.`orders` ELSE 0 END AS aov,
  -- ARPU mensual
  CASE WHEN m.`unique_customers` > 0 THEN m.`revenue` / m.`unique_customers` ELSE 0 END AS arpu,
  -- items por orden
  CASE WHEN m.`orders` > 0 THEN m.`items` / m.`orders` ELSE 0 END AS items_per_order
FROM v_orders_monthly AS m;

-- primeras filas en orden cronológico
SELECT *
FROM v_kpi_monthly
ORDER BY STR_TO_DATE(CONCAT(`year_month`,'-01'), '%Y-%m-%d')
LIMIT 12;

-- totales deben cuadrar con v_orders_monthly
SELECT
  SUM(`orders`)        AS orders_total,
  SUM(`revenue`)       AS revenue_total,
  SUM(`payment_total`) AS payment_total,
  SUM(`items`)         AS items_total
FROM v_kpi_monthly;

