from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
PROC = BASE / "data_processed"

# 1) Cargar
df = pd.read_csv(PROC / "fact_orders.csv", parse_dates=["order_date"])

# 2) Fecha de adquisición por cliente
acq = (df.groupby("customer_unique_id", as_index=False)["order_date"]
         .min()
         .rename(columns={"order_date": "acquisition_date"}))
df = df.merge(acq, on="customer_unique_id", how="left")

# 3) Cohorte y período (método robusto)
df["cohort_month"] = df["acquisition_date"].dt.to_period("M").astype(str)
df["order_month"]  = df["order_date"].dt.to_period("M").astype(str)
df["period_month"] = (
    (df["order_date"].dt.year - df["acquisition_date"].dt.year) * 12 +
    (df["order_date"].dt.month - df["acquisition_date"].dt.month)
)
df = df[df["period_month"] >= 0].copy()

# --- RETENCIÓN ---
cohort_size = (df.groupby("cohort_month")["customer_unique_id"]
                 .nunique()
                 .rename("cohort_size"))

active = (df.groupby(["cohort_month", "period_month"])["customer_unique_id"]
            .nunique()
            .rename("active_customers")
            .reset_index())

ret = active.merge(cohort_size, on="cohort_month", how="left")
ret["retention_rate"] = ret["active_customers"] / ret["cohort_size"]

ret_count = (ret.pivot(index="cohort_month", columns="period_month",
                       values="active_customers").fillna(0).astype(int).sort_index())
ret_rate  = (ret.pivot(index="cohort_month", columns="period_month",
                       values="retention_rate").fillna(0).round(4).sort_index())

# --- LTV (ARPU acumulado) ---
rev = (df.groupby(["cohort_month", "period_month"])["items_revenue"]
         .sum()
         .rename("revenue")
         .reset_index())

ltv = rev.merge(cohort_size, on="cohort_month", how="left")
ltv["arpu"] = ltv["revenue"] / ltv["cohort_size"]
ltv["ltv_cum"] = (ltv.sort_values("period_month")
                     .groupby("cohort_month")["arpu"]
                     .cumsum())
ltv_pivot = (ltv.pivot(index="cohort_month", columns="period_month",
                       values="ltv_cum").fillna(0).round(2).sort_index())

# 4) Guardar
ret_count.to_csv(PROC / "cohort_retention_counts.csv")
ret_rate.to_csv(PROC / "cohort_retention_rates.csv", float_format="%.4f")
ltv_pivot.to_csv(PROC / "cohort_ltv.csv", float_format="%.2f")

print("OK -> cohort_retention_counts.csv, cohort_retention_rates.csv, cohort_ltv.csv")
