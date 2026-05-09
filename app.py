"""
app.py — Dashboard de Ventas · Streamlit + SQLite
Correr con: streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ── Auto ETL: crear BD si no existe ──────────────────────────────────────────
DB_PATH  = "database/ventas.db"
CSV_PATH = "data/Sample - Superstore.csv"

if not os.path.exists(DB_PATH):
    os.makedirs("database", exist_ok=True)
    df_etl = pd.read_csv(CSV_PATH, encoding='latin-1')
    df_etl.columns = (df_etl.columns.str.strip().str.lower()
                      .str.replace(' ', '_').str.replace('-', '_'))
    df_etl['order_date'] = pd.to_datetime(df_etl['order_date'], errors='coerce')
    df_etl['ship_date']  = pd.to_datetime(df_etl['ship_date'],  errors='coerce')
    df_etl['year']       = df_etl['order_date'].dt.year
    df_etl['month']      = df_etl['order_date'].dt.month
    df_etl['month_name'] = df_etl['order_date'].dt.strftime('%B')
    df_etl.drop_duplicates(inplace=True)
    _engine = create_engine(f"sqlite:///{DB_PATH}")
    df_etl.to_sql("ventas", _engine, if_exists="replace", index=False)

# ── Página ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { background: #0F172A !important; }
.block-container { padding: 2rem 2.5rem 1rem !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617 !important;
    border-right: 1px solid #1E293B;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #94A3B8 !important; }
section[data-testid="stSidebar"] .stMarkdown h2 { color: #F8FAFC !important; font-size: 18px !important; }
section[data-testid="stSidebar"] hr { border-color: #1E293B !important; }

/* KPI cards */
[data-testid="metric-container"] {
    background: #1E293B !important;
    border: 1.5px solid #334155 !important;
    border-radius: 14px !important;
    padding: 18px 22px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}
[data-testid="metric-container"] > div:first-child p {
    color: #94A3B8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] div {
    color: #F8FAFC !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

/* Títulos de sección */
.sec-title {
    font-size: 12px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0 0 14px 2px;
}

/* Separador */
.divider { border: none; border-top: 1.5px solid #1E293B; margin: 20px 0; }

/* Títulos y texto general */
h1, h2, h3, p { color: #F1F5F9 !important; }
</style>
""", unsafe_allow_html=True)

# ── Colores ───────────────────────────────────────────────────────────────────
C1, C2, C3, C4, C5 = "#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#F43F5E"
GRID = "#1E293B"
BG   = "#0F172A"
CARD = "#1E293B"

def base(h=340):
    return dict(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family="Inter, sans-serif", color="#CBD5E0", size=12),
        margin=dict(t=20, b=20, l=10, r=10),
        height=h,
    )

# ── Datos ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def engine():
    return create_engine("sqlite:///database/ventas.db")

@st.cache_data
def load():
    df = pd.read_sql("SELECT * FROM ventas", engine())
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

try:
    df = load()
except Exception:
    st.error("⚠️ Ejecuta primero: `python etl.py`")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Sales Dashboard")
    st.markdown("---")

    años  = sorted(df['year'].dropna().unique().tolist())
    cats  = sorted(df['category'].unique().tolist())
    regs  = sorted(df['region'].unique().tolist())
    segs  = sorted(df['segment'].unique().tolist())

    año_sel = st.multiselect("📅 Año",       años, default=años)
    cat_sel = st.multiselect("🏷️ Categoría", cats, default=cats)
    reg_sel = st.multiselect("🌎 Región",    regs, default=regs)
    seg_sel = st.multiselect("👤 Segmento",  segs, default=segs)

    st.markdown("---")
    st.caption("Sample Superstore · Kaggle")

# ── Filtro ────────────────────────────────────────────────────────────────────
dff = df[
    df['year'].isin(año_sel) &
    df['category'].isin(cat_sel) &
    df['region'].isin(reg_sel) &
    df['segment'].isin(seg_sel)
]
if dff.empty:
    st.warning("Sin datos para los filtros seleccionados.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 📊 Dashboard de Ventas")
st.markdown(f"<p style='color:#64748B;font-size:13px;margin-top:-8px'>Sample Superstore &nbsp;·&nbsp; <b style='color:#94A3B8'>{len(dff):,}</b> registros</p>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
vt = dff['sales'].sum()
gt = dff['profit'].sum()
pe = dff['order_id'].nunique()
mg = gt / vt * 100 if vt else 0
tk = vt / pe if pe else 0
cl = dff['customer_id'].nunique()

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("💰 Ventas",        f"${vt/1e6:.2f}M")
c2.metric("📈 Ganancia",      f"${gt:,.0f}")
c3.metric("🛒 Pedidos",       f"{pe:,}")
c4.metric("📊 Margen",        f"{mg:.1f}%")
c5.metric("🧾 Ticket prom.",  f"${tk:,.0f}")
c6.metric("👥 Clientes",      f"{cl:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# FILA 1 — Evolución mensual + Dona categorías
# ════════════════════════════════════════════════════════
col_l, col_r = st.columns([3, 1], gap="large")

with col_l:
    st.markdown('<p class="sec-title">Evolución mensual de ventas</p>', unsafe_allow_html=True)

    vm = dff.groupby(dff['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
    vm['order_date'] = vm['order_date'].dt.to_timestamp()
    vm['mm3'] = vm['sales'].rolling(3, min_periods=1).mean()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=vm['order_date'], y=vm['sales'],
        name='Ventas mensuales',
        fill='tozeroy', fillcolor='rgba(59,130,246,0.1)',
        line=dict(color=C1, width=2.5), mode='lines',
        hovertemplate='%{x|%b %Y}<br><b>$%{y:,.0f}</b><extra></extra>'
    ))
    fig1.add_trace(go.Scatter(
        x=vm['order_date'], y=vm['mm3'],
        name='Media móvil 3M',
        line=dict(color=C5, width=1.8, dash='dash'), mode='lines',
        hovertemplate='Media móvil<br><b>$%{y:,.0f}</b><extra></extra>'
    ))
    fig1.update_layout(**base(290),
        xaxis=dict(showgrid=False, tickformat='%b %Y', tickangle=-30,
                   tickfont=dict(size=11, color='#94A3B8'),
                   linecolor='#334155'),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickprefix='$', tickformat=',.0f',
                   tickfont=dict(size=11, color='#94A3B8')),
        legend=dict(orientation='h', x=0, y=1.12,
                    font=dict(size=12, color='#CBD5E0'),
                    bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_r:
    st.markdown('<p class="sec-title">Por categoría</p>', unsafe_allow_html=True)

    cd = dff.groupby('category')['sales'].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=cd['category'], values=cd['sales'],
        hole=0.60,
        marker=dict(colors=[C1, C2, C3],
                    line=dict(color=CARD, width=3)),
        textinfo='percent',
        textfont=dict(size=13, color='white'),
        insidetextorientation='radial',
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    fig2.update_layout(**base(290),
        showlegend=True,
        legend=dict(orientation='v', x=0, y=0,
                    font=dict(size=11, color='#CBD5E0'),
                    bgcolor='rgba(0,0,0,0)'),
        annotations=[dict(text=f"<b>${vt/1e6:.1f}M</b>",
                          x=0.5, y=0.5,
                          font=dict(size=15, color='#F1F5F9'),
                          showarrow=False)]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# FILA 2 — Top sub-categorías + Región
# ════════════════════════════════════════════════════════
col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown('<p class="sec-title">Top 10 sub-categorías por ventas</p>', unsafe_allow_html=True)

    ts = dff.groupby('sub_category')['sales'].sum().sort_values().tail(10).reset_index()
    fig3 = go.Figure(go.Bar(
        x=ts['sales'], y=ts['sub_category'],
        orientation='h',
        marker=dict(
            color=ts['sales'],
            colorscale=[[0,'#1D4ED8'],[0.5,'#3B82F6'],[1,'#93C5FD']],
            showscale=False
        ),
        text=ts['sales'].map('${:,.0f}'.format),
        textposition='outside',
        textfont=dict(size=11, color='#94A3B8'),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))
    fig3.update_layout(**base(360),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#CBD5E0'),
                   automargin=True)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    st.markdown('<p class="sec-title">Ventas y ganancia por región</p>', unsafe_allow_html=True)

    rd = dff.groupby('region').agg(ventas=('sales','sum'), ganancia=('profit','sum')).reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        name='Ventas', x=rd['region'], y=rd['ventas'],
        marker_color=C1, yaxis='y',
        text=rd['ventas'].map('${:,.0f}'.format),
        textposition='outside',
        textfont=dict(size=10, color='#94A3B8'),
        hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
    ))
    fig4.add_trace(go.Scatter(
        name='Ganancia', x=rd['region'], y=rd['ganancia'],
        mode='lines+markers', yaxis='y2',
        line=dict(color=C2, width=2.5),
        marker=dict(color=C2, size=10, symbol='diamond',
                    line=dict(color=CARD, width=2)),
        hovertemplate='<b>%{x}</b><br>Ganancia: $%{y:,.0f}<extra></extra>'
    ))
    fig4.update_layout(**base(360),
        xaxis=dict(showgrid=False, tickfont=dict(size=12, color='#CBD5E0')),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickprefix='$', tickformat=',.0f',
                   tickfont=dict(size=11, color='#94A3B8'),
                   title=dict(text='Ventas', font=dict(size=11, color='#64748B'))),
        yaxis2=dict(overlaying='y', side='right', zeroline=False,
                    tickprefix='$', tickformat=',.0f',
                    tickfont=dict(size=11, color='#94A3B8'),
                    title=dict(text='Ganancia', font=dict(size=11, color='#64748B'))),
        legend=dict(orientation='h', x=0, y=1.12,
                    font=dict(size=12, color='#CBD5E0'),
                    bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# FILA 3 — Scatter descuento + Línea segmentos
# ════════════════════════════════════════════════════════
col_c, col_d = st.columns(2, gap="large")

with col_c:
    st.markdown('<p class="sec-title">Descuento vs ganancia por sub-categoría</p>', unsafe_allow_html=True)

    sd = dff.groupby('sub_category').agg(
        descuento=('discount','mean'),
        ganancia=('profit','sum'),
        ventas=('sales','sum')
    ).reset_index()

    fig5 = px.scatter(
        sd, x='descuento', y='ganancia',
        size='ventas', color='ganancia', text='sub_category',
        color_continuous_scale=[[0,C5],[0.5,C4],[1,C2]],
        size_max=48,
        labels={'descuento':'Descuento promedio', 'ganancia':'Ganancia total ($)'}
    )
    fig5.update_traces(
        textposition='top center',
        textfont=dict(size=9, color='#94A3B8'),
        marker=dict(line=dict(width=1.5, color=CARD))
    )
    fig5.update_layout(**base(340),
        coloraxis_showscale=False,
        xaxis=dict(tickformat='.0%', showgrid=True, gridcolor=GRID,
                   zeroline=False, tickfont=dict(size=11, color='#94A3B8')),
        yaxis=dict(tickprefix='$', tickformat=',.0f',
                   showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(size=11, color='#94A3B8'))
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_d:
    st.markdown('<p class="sec-title">Ventas por segmento año a año</p>', unsafe_allow_html=True)

    sa = dff.groupby(['year','segment'])['sales'].sum().reset_index()
    fig6 = px.line(
        sa, x='year', y='sales', color='segment',
        markers=True,
        color_discrete_sequence=[C1, C2, C3],
        labels={'year':'Año', 'sales':'Ventas ($)', 'segment':'Segmento'}
    )
    fig6.update_traces(line_width=2.5, marker_size=9,
                       marker=dict(line=dict(width=2, color=CARD)))
    fig6.update_layout(**base(340),
        xaxis=dict(showgrid=False, tickmode='linear', dtick=1,
                   tickfont=dict(size=12, color='#94A3B8')),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickprefix='$', tickformat=',.0f',
                   tickfont=dict(size=11, color='#94A3B8')),
        legend=dict(orientation='h', x=0, y=1.12,
                    font=dict(size=12, color='#CBD5E0'),
                    bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TABLA
# ════════════════════════════════════════════════════════
st.markdown('<p class="sec-title">Resumen por estado — Top 20</p>', unsafe_allow_html=True)

tabla = (
    dff.groupby('state').agg(
        Ventas=('sales','sum'),
        Ganancia=('profit','sum'),
        Pedidos=('order_id','nunique'),
        Clientes=('customer_id','nunique')
    ).reset_index()
    .sort_values('Ventas', ascending=False).head(20)
)
tabla['Margen %'] = (tabla['Ganancia'] / tabla['Ventas'] * 100).round(1)
tabla['Ventas']   = tabla['Ventas'].map('${:,.0f}'.format)
tabla['Ganancia'] = tabla['Ganancia'].map('${:,.0f}'.format)
tabla['Margen %'] = tabla['Margen %'].map('{:.1f}%'.format)
tabla.rename(columns={'state':'Estado'}, inplace=True)

st.dataframe(tabla, use_container_width=True, height=340, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#334155;font-size:12px'>Desarrollado por Juan · Portafolio Data Analyst · 2026 · github.com/Jejattin</p>", unsafe_allow_html=True)