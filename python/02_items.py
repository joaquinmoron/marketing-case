from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
raw_path = BASE / "data_raw" / "olist_order_items_dataset.csv"
out_dir  = BASE / "data_processed"
out_dir.mkdir(parents=True, exist_ok=True)

# 1) Carga mínima
usecols = ["order_id", "order_item_id", "product_id", "price", "freight_value"]
items = pd.read_csv(raw_path, usecols=usecols)

# 2) Tipos y QA rápidos
items["price"] = pd.to_numeric(items["price"], errors="coerce")
items["freight_value"] = pd.to_numeric(items["freight_value"], errors="coerce")
dup = items.duplicated(subset=["order_id", "order_item_id"]).sum()
print("Duplicados (order_id, order_item_id):", dup)

# 3) Limpieza simple
items_clean = items.dropna(subset=["order_id", "price"]).copy()

# 4) Guardar nivel ítem (limpio)
clean_path = out_dir / "order_items_clean.csv"
items_clean.to_csv(clean_path, index=False)
print(f"OK -> {clean_path}  Filas: {len(items_clean)}")

# 5) Agregado por orden (revenue, flete, #ítems)
agg = (
    items_clean.groupby("order_id", as_index=False)
               .agg(items_revenue=("price", "sum"),
                    freight=("freight_value", "sum"),
                    n_items=("order_item_id", "count"))
)
agg_path = out_dir / "order_items_agg.csv"
agg.to_csv(agg_path, index=False)
print(f"OK -> {agg_path}  Órdenes únicas: {len(agg)}")
