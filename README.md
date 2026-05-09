# 📊 Dashboard Interactivo de Ventas

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)

Dashboard web interactivo construido con Python, Streamlit y SQLite que permite
analizar métricas de ventas con filtros dinámicos por año, categoría, región y segmento.

🔗 **[Ver demo en vivo](https://TU-APP.streamlit.app)**

---

## ✨ Funcionalidades

- **KPIs en tiempo real** — ventas totales, ganancia, pedidos, margen y ticket promedio
- **Filtros dinámicos** — por año, categoría, región y segmento de cliente
- **Evolución mensual** — gráfica de línea con tendencia de ventas
- **Análisis por categoría** — gráfica de torta interactiva
- **Top sub-categorías** — ranking horizontal de las más vendidas
- **Ventas vs Ganancia** — scatter plot por región
- **Tabla detallada** — métricas por estado ordenables

---

## 🛠 Stack tecnológico

| Herramienta | Uso |
|-------------|-----|
| Python 3.10 | Lenguaje principal |
| Pandas | Manipulación de datos |
| SQLAlchemy + SQLite | Pipeline ETL y base de datos |
| Plotly | Visualizaciones interactivas |
| Streamlit | Framework del dashboard web |

---

## 🚀 Cómo ejecutar localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/dashboard-ventas.git
cd dashboard-ventas

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Descargar el dataset y guardarlo en data/superstore.csv
# https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

# 5. Ejecutar el ETL (solo la primera vez)
python etl.py

# 6. Correr la app
streamlit run app.py
```

---

## 📂 Estructura del proyecto

```
dashboard-ventas/
├── data/
│   └── superstore.csv
├── database/
│   └── ventas.db
├── app.py
├── etl.py
├── requirements.txt
└── README.md
```

---

## 📋 Dataset

**Fuente:** Sample Superstore — [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)  
**Registros:** ~10,000 órdenes de venta  
**Período:** 2014–2017  

---

## 👤 Autor

**Juan Jattin**  
Ingeniero de Sistemas | Data Analyst  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/juanjattin/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Jejattin)

---
*Proyecto parte del portafolio de análisis de datos — Mayo 2026*
