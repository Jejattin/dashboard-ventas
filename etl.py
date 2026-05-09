"""
etl.py — Carga el dataset Superstore desde CSV a una base de datos SQLite.
Ejecutar una sola vez antes de correr la app: python etl.py
"""

import pandas as pd
from sqlalchemy import create_engine
import os

# ── Rutas ────────────────────────────────────────────────────────────────────
CSV_PATH = "data/Sample - Superstore.csv"
DB_PATH  = "database/ventas.db"

os.makedirs("database", exist_ok=True)

# ── Cargar CSV ────────────────────────────────────────────────────────────────
print("📂 Cargando CSV...")
df = pd.read_csv(CSV_PATH, encoding='latin-1')

# ── Limpieza básica ───────────────────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
)

# Fechas
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['ship_date']  = pd.to_datetime(df['ship_date'],  errors='coerce')

# Columnas derivadas útiles para el dashboard
df['year']  = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['month_name'] = df['order_date'].dt.strftime('%B')

# Eliminar duplicados
antes = len(df)
df.drop_duplicates(inplace=True)
print(f"🗑️  Duplicados eliminados: {antes - len(df)}")

# ── Cargar a SQLite ───────────────────────────────────────────────────────────
engine = create_engine(f"sqlite:///{DB_PATH}")
df.to_sql("ventas", engine, if_exists="replace", index=False)

print(f"✅ Base de datos creada en: {DB_PATH}")
print(f"   Registros cargados: {len(df):,}")
print(f"   Columnas: {list(df.columns)}")
