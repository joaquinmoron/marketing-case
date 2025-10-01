# Marketing Case — SQL + Python (Olist)

Análisis de cohortes, retención y LTV con **Python** y **SQL** usando el dataset público de Olist.

## 🎯 Objetivo
- Limpiar y preparar datos de ventas.
- Construir **cohortes** (adquisición/retención) y **LTV** simple.
- Modelar en **SQL** (staging → facts/dims → vistas KPI).
- Separar **clientes nuevos vs. recurrentes** y su revenue.

## 📂 Estructura

## 🐍 Python (carpeta `python/`)
- `01_eda.py` → limpieza de órdenes  
- `02_items.py` → agregación de ítems  
- `03_payments.py` → consolidación de pagos  
- `04_customers.py` → validación de clientes  
- `05_fact_orders.py` → construcción de `fact_orders`  
- `06_cohortes_ltv.py` → cohortes (retención) y LTV simple

> **Nota:** los CSV intermedios se guardan en `data_processed/` (local, no se sube).

## 🗄️ SQL (carpeta `sql/`) — orden sugerido
1. `01_load_raw.sql`  
2. `02_build_fact_orders.sql`  
3. `03_dim_date.sql`  
4. `04_views.sql`  
5. `05_kpi.sql`  
6. `06_new_returning.sql`

Esto crea `dim_date`, consolida `fact_orders` y genera vistas/KPIs (AOV, items/order, nuevos vs. recurrentes).

## ▶️ Cómo correr
1. Clonar el repo.  
2. (Opcional) Crear entorno:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt  # si corresponde
