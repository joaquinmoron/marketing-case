USE db_marketing;

-- 1) Tabla RAW (todo texto)
DROP TABLE IF EXISTS fact_orders_raw;
CREATE TABLE fact_orders_raw (
  order_id                      TEXT,
  customer_id                   TEXT,
  customer_unique_id            TEXT,
  order_date                    TEXT,
  order_month                   TEXT,
  order_purchase_timestamp      TEXT,
  order_delivered_customer_date TEXT,
  items_revenue                 TEXT,
  freight                       TEXT,
  payment_total                 TEXT,
  n_items                       TEXT,
  order_status                  TEXT
);

-- 2) Carga masiva rápida desde el CSV
LOAD DATA LOCAL INFILE 'C:/Users/PC/Desktop/Marketing-Case/data_processed/fact_orders.csv'
INTO TABLE fact_orders_raw
CHARACTER SET utf8
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(order_id, customer_id, customer_unique_id, order_date, order_month,
 order_purchase_timestamp, order_delivered_customer_date,
 items_revenue, freight, payment_total, n_items, order_status);

-- 3) Verificación
SELECT COUNT(*) AS row_count FROM fact_orders_raw;
