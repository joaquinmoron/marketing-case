from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
raw_path = BASE / "data_raw" / "olist_order_payments_dataset.csv"
out_dir  = BASE / "data_processed"
out_dir.mkdir(parents=True, exist_ok=True)

# 1) Carga mínima
usecols = ["order_id", "payment_sequential", "payment_type", "payment_value"]
pay = pd.read_csv(raw_path, usecols=usecols)

# 2) Tipos y QA rápidos
pay["payment_value"] = pd.to_numeric(pay["payment_value"], errors="coerce")
dup = pay.duplicated(subset=["order_id", "payment_sequential"]).sum()
print("Duplicados (order_id, payment_sequential):", dup)

# 3) Limpieza simple
pay_clean = pay.dropna(subset=["order_id", "payment_value"]).copy()
pay_clean = pay_clean[pay_clean["payment_value"] >= 0]  # por las dudas, sin negativos

# 4) Guardar limpio (opcional, por trazabilidad)
clean_path = out_dir / "order_payments_clean.csv"
pay_clean.to_csv(clean_path, index=False)
print(f"OK -> {clean_path}  Filas: {len(pay_clean)}")

# 5) Agregado por orden (total pago, tipo principal y #pagos)
agg = (
    pay_clean.groupby("order_id", as_index=False)
             .agg(payment_total=("payment_value", "sum"),
                  main_payment_type=("payment_type",
                                     lambda s: s.mode().iat[0] if not s.mode().empty else None),
                  n_payments=("payment_sequential", "count"))
)

agg_path = out_dir / "payments_agg.csv"
agg.to_csv(agg_path, index=False)
print(f"OK -> {agg_path}  Órdenes únicas: {len(agg)}")

# 6) Chequeo rápido de tipos de pago
print("\nTipos de pago (Top):")
print(agg["main_payment_type"].value_counts().head(5))
