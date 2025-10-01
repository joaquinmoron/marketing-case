from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
raw_path = BASE / "data_raw" / "olist_customers_dataset.csv"
out_dir  = BASE / "data_processed"
out_dir.mkdir(parents=True, exist_ok=True)

# 1) Carga mínima
usecols = ["customer_id", "customer_unique_id", "customer_city", "customer_state"]
cust = pd.read_csv(raw_path, usecols=usecols)

# 2) QA rápido
dup_id = cust.duplicated(subset=["customer_id"]).sum()
print("Duplicados por customer_id:", dup_id)

# Nota: En Olist, varios customer_id pueden mapear al mismo customer_unique_id (mudanzas, etc.)
print("customer_id únicos:", cust["customer_id"].nunique())
print("customer_unique_id únicos:", cust["customer_unique_id"].nunique())

# 3) Limpieza simple: nos quedamos con la primera aparición por customer_id
cust_clean = cust.drop_duplicates(subset=["customer_id"], keep="first").copy()

# 4) Guardar
out_path = out_dir / "customers_clean.csv"
cust_clean.to_csv(out_path, index=False)
print(f"OK -> {out_path}  Filas: {len(cust_clean)}")
