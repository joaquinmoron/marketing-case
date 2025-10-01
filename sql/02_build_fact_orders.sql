USE db_marketing;

-- 1) Crear la tabla final con los tipos correctos
DROP TABLE IF EXISTS fact_orders;
CREATE TABLE fact_orders (
  order_id                      VARCHAR(50)  NOT NULL,
  customer_id                   VARCHAR(50),
  customer_unique_id            VARCHAR(50),
  order_date                    DATE,
  order_month                   CHAR(7),
  order_purchase_timestamp      DATETIME,
  order_delivered_customer_date DATETIME,
  items_revenue                 DECIMAL(12,2),
  freight                       DECIMAL(12,2),
  payment_total                 DECIMAL(12,2),
  n_items                       INT,
  order_status                  VARCHAR(20),
  PRIMARY KEY (order_id),
  INDEX idx_fact_orders_date(order_date),
  INDEX idx_fact_orders_month(order_month)
);

-- 2) Insertar convirtiendo tipos/fechas desde la RAW
INSERT INTO fact_orders (
  order_id, customer_id, customer_unique_id,
  order_date, order_month,
  order_purchase_timestamp, order_delivered_customer_date,
  items_revenue, freight, payment_total, n_items, order_status
)
SELECT
  TRIM(order_id),
  TRIM(customer_id),
  TRIM(customer_unique_id),
  STR_TO_DATE(order_date, '%Y-%m-%d'),
  TRIM(order_month),
  STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'),
  STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
  CAST(items_revenue AS DECIMAL(12,2)),
  CAST(freight       AS DECIMAL(12,2)),
  CAST(payment_total AS DECIMAL(12,2)),
  CAST(n_items       AS UNSIGNED),
  TRIM(order_status)
FROM fact_orders_raw;

-- 3) Verificación mínima
SELECT COUNT(*) AS row_count FROM fact_orders;

SELECT
  MIN(order_date) AS min_order_date,
  MAX(order_date) AS max_order_date
FROM fact_orders;

SELECT
  SUM(items_revenue) AS revenue_sum,
  SUM(payment_total) AS payment_sum,
  SUM(n_items)       AS items_sum
FROM fact_orders;
