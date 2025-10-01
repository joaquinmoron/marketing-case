from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
orders_path = BASE_DIR / "data_raw" / "olist_orders_dataset.csv"
out_dir = BASE_DIR / "data_processed"
out_dir.mkdir(parents=True, exist_ok=True)

# 1) Carga
orders = pd.read_csv(orders_path)

# 2) Fechas
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for c in date_cols:
    orders[c] = pd.to_datetime(orders[c], errors="coerce")
orders["order_date"] = orders["order_purchase_timestamp"].dt.date
orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

# 3) QA rápido
dup_count = orders["order_id"].duplicated().sum()

# 4) Filtrado mínimo (solo delivered con fecha de entrega) + columnas útiles
orders_clean = (
    orders.loc[orders["order_status"].eq("delivered")]
          .dropna(subset=["order_delivered_customer_date"])
          [["order_id","customer_id","order_status",
            "order_purchase_timestamp","order_delivered_customer_date",
            "order_date","order_month"]]
          .copy()
)

# 5) Guardar
out_file = out_dir / "orders_clean.csv"
orders_clean.to_csv(out_file, index=False)

print(f"Filas/cols orders: {orders.shape}")
print(f"Duplicados por order_id: {dup_count}")
print(f"Filas en orders_clean: {len(orders_clean)}")
print(f"Guardado: {out_file}")
