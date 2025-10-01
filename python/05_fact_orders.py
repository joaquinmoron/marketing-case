from pathlib import Path
import pandas as pd

# Rutas
BASE = Path(__file__).resolve().parent
PROC = BASE / "data_processed"

# 1) Leer insumos (los que ya creaste antes)
orders = pd.read_csv(
    PROC / "orders_clean.csv",
    parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"]
)
items  = pd.read_csv(PROC / "order_items_agg.csv")        # por order_id: items_revenue, freight, n_items
pays   = pd.read_csv(PROC / "payments_agg.csv")           # por order_id: payment_total, main_payment_type, n_payments
custs  = pd.read_csv(PROC / "customers_clean.csv")[["customer_id","customer_unique_id"]].drop_duplicates("customer_id")

# 2) Uniones (LEFT desde orders_clean → mantiene SOLO delivered)
df = (orders
      .merge(items, on="order_id", how="left")
      .merge(pays,  on="order_id", how="left")
      .merge(custs, on="customer_id", how="left"))

# 3) Completar numéricos vacíos si alguna orden no matcheó
for c in ["items_revenue", "freight", "payment_total", "n_items"]:
    if c in df.columns:
        df[c] = df[c].fillna(0)

# Tipos básicos
if "n_items" in df.columns:
    df["n_items"] = df["n_items"].astype("int64", errors="ignore")

# 4) Reordenar/seleccionar columnas finales
cols = [
    "order_id","customer_id","customer_unique_id",
    "order_date","order_month",
    "order_purchase_timestamp","order_delivered_customer_date",
    "items_revenue","freight","payment_total","n_items",
    "order_status"
]
df = df[[c for c in cols if c in df.columns]].copy()

# 5) Chequeos cortos (solo prints)
print("Filas en orders_clean:", len(orders))
print("Filas en fact_orders (debe ser ~igual):", len(df))
print("Órdenes sin ítems (items_revenue == 0):", int((df["items_revenue"] == 0).sum()))
print("Órdenes sin pago (payment_total == 0):", int((df["payment_total"] == 0).sum()))
print("Faltantes de customer_unique_id:", int(df["customer_unique_id"].isna().sum()))

# 6) Guardar salida
out_path = PROC / "fact_orders.csv"
df.to_csv(out_path, index=False)
print("OK ->", out_path)
