"""
app.py — Global Military Expenditure Dashboard
==============================================
An interactive dashboard visualising global military spending data sourced
from Wikipedia (SIPRI 2024 & IISS 2025).

Launch:
  streamlit run app/app.py
"""

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Design tokens ────────────────────────────────────────────────────────────
BG = "#0b1020"
PANEL = "#151c30"
BORDER = "#243049"
TEXT = "#e6ebf5"
MUTED = "#8a96b3"
ACCENT = "#f5b301"
ACCENT_2 = "#5b8def"
DANGER = "#ff6b6b"
GRID = "rgba(255,255,255,0.06)"

# Cohesive palettes used across every chart
CATEGORICAL = ["#f5b301", "#5b8def", "#ff6b6b", "#36d399",
               "#a78bfa", "#f97316", "#22d3ee", "#e879f9"]
SEQUENTIAL = [[0.0, "#16203a"], [0.45, "#3f63b0"], [1.0, "#f5b301"]]
GDP_SCALE = [[0.0, "#16203a"], [0.5, "#b3471f"], [1.0, "#ff6b6b"]]

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Military Spending",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom styling ───────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

.stApp {
    background:
        radial-gradient(1200px 600px at 80% -10%, rgba(91,141,239,0.10), transparent 60%),
        radial-gradient(900px 500px at -10% 0%, rgba(245,179,1,0.08), transparent 55%),
        #0b1020;
}

/* tighten the default top padding */
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1300px; }

/* hide default chrome */
#MainMenu, footer { visibility: hidden; }

/* ── Hero ── */
.hero { margin-bottom: 1.4rem; }
.hero h1 {
    font-size: 2.5rem; font-weight: 800; letter-spacing: -0.02em;
    margin: 0; line-height: 1.1;
    background: linear-gradient(90deg, #ffffff 0%, #cdd7ef 60%, #f5b301 130%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #8a96b3; font-size: 1.02rem; margin: 0.45rem 0 0; }
.pill {
    display: inline-flex; align-items: center; gap: 0.45rem;
    background: rgba(245,179,1,0.10); color: #f5b301;
    border: 1px solid rgba(245,179,1,0.30);
    padding: 0.25rem 0.7rem; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.02em;
    margin-bottom: 0.9rem;
}

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 0.4rem 0 0.6rem; }
.kpi {
    position: relative; background: linear-gradient(160deg, #182039 0%, #121829 100%);
    border: 1px solid #243049; border-radius: 16px;
    padding: 1.15rem 1.25rem; overflow: hidden;
    transition: transform .15s ease, border-color .15s ease;
}
.kpi:hover { transform: translateY(-3px); border-color: #3a4a7a; }
.kpi::before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(180deg, #f5b301, #5b8def);
}
.kpi-label { color: #8a96b3; font-size: 0.78rem; font-weight: 600;
             text-transform: uppercase; letter-spacing: 0.06em; }
.kpi-value { color: #ffffff; font-size: 1.9rem; font-weight: 800; margin: 0.25rem 0 0.1rem; }
.kpi-sub { color: #6f7c9b; font-size: 0.82rem; }
.kpi-sub b { color: #f5b301; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 1px solid #243049; }
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px 10px 0 0;
    padding: 0.55rem 1.05rem; color: #8a96b3; font-weight: 600;
}
.stTabs [aria-selected="true"] { background: #151c30; color: #ffffff; }

/* ── Section labels ── */
.section { font-size: 1.15rem; font-weight: 700; color: #e6ebf5; margin: 0.2rem 0 0.6rem; }
.caption { color: #6f7c9b; font-size: 0.85rem; margin-bottom: 0.8rem; }

/* sidebar polish */
section[data-testid="stSidebar"] { background: #0d1324; border-right: 1px solid #243049; }
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stSelectbox label { font-weight: 600; }

/* dataframe + insight callout */
div[data-testid="stMetricValue"] { color: #f5b301; }
.insight {
    background: rgba(91,141,239,0.08); border: 1px solid rgba(91,141,239,0.25);
    border-radius: 12px; padding: 0.9rem 1.1rem; color: #cdd7ef; font-size: 0.92rem;
}
.insight b { color: #f5b301; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Data loading ─────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

REGION_MAP = {
    "United States": "North America", "Canada": "North America", "Mexico": "North America",
    "Brazil": "South America", "Colombia": "South America",
    "China": "Asia", "India": "Asia", "Japan": "Asia", "South Korea": "Asia",
    "Taiwan": "Asia", "Singapore": "Asia", "Indonesia": "Asia", "Pakistan": "Asia",
    "Philippines": "Asia", "Iran": "Asia",
    "Russia": "Europe", "Germany": "Europe", "United Kingdom": "Europe",
    "Ukraine": "Europe", "France": "Europe", "Poland": "Europe", "Italy": "Europe",
    "Spain": "Europe", "Netherlands": "Europe", "Sweden": "Europe", "Norway": "Europe",
    "Denmark": "Europe", "Romania": "Europe", "Belgium": "Europe", "Greece": "Europe",
    "Finland": "Europe", "Switzerland": "Europe", "Czech Republic": "Europe",
    "Turkey": "Middle East", "Saudi Arabia": "Middle East", "Israel": "Middle East",
    "Kuwait": "Middle East", "Iraq": "Middle East",
    "Algeria": "Africa", "Australia": "Oceania",
}

# ISO-3 codes for a robust choropleth (locationmode="ISO-3")
ISO3_MAP = {
    "United States": "USA", "China": "CHN", "Russia": "RUS", "Germany": "DEU",
    "India": "IND", "United Kingdom": "GBR", "Saudi Arabia": "SAU", "Ukraine": "UKR",
    "France": "FRA", "Japan": "JPN", "South Korea": "KOR", "Israel": "ISR",
    "Poland": "POL", "Italy": "ITA", "Australia": "AUS", "Canada": "CAN",
    "Turkey": "TUR", "Spain": "ESP", "Netherlands": "NLD", "Algeria": "DZA",
    "Brazil": "BRA", "Mexico": "MEX", "Taiwan": "TWN", "Colombia": "COL",
    "Singapore": "SGP", "Sweden": "SWE", "Indonesia": "IDN", "Norway": "NOR",
    "Pakistan": "PAK", "Denmark": "DNK", "Romania": "ROU", "Belgium": "BEL",
    "Greece": "GRC", "Iran": "IRN", "Kuwait": "KWT", "Finland": "FIN",
    "Switzerland": "CHE", "Czech Republic": "CZE", "Iraq": "IRQ", "Philippines": "PHL",
}


@st.cache_data
def load_data():
    sipri = pd.read_csv(os.path.join(DATA_DIR, "military_spending_sipri_2024.csv"))
    iiss = pd.read_csv(os.path.join(DATA_DIR, "military_spending_iiss_2025.csv"))
    gdp_sipri = pd.read_csv(os.path.join(DATA_DIR, "gdp_pct_sipri_2024.csv"))
    gdp_iiss = pd.read_csv(os.path.join(DATA_DIR, "gdp_pct_iiss_2020.csv"))
    sipri["Region"] = sipri["Country"].map(REGION_MAP).fillna("Other")
    sipri["ISO3"] = sipri["Country"].map(ISO3_MAP)
    return sipri, iiss, gdp_sipri, gdp_iiss


sipri, iiss, gdp_sipri, gdp_iiss = load_data()
SPEND = "Spending (US$ bn)"


# ── Helpers ──────────────────────────────────────────────────────────────────
def style_fig(fig, height=460, show_legend=True):
    """Apply the unified dark theme to any plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Inter, Segoe UI, sans-serif", size=13),
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=show_legend,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, borderwidth=0),
        hoverlabel=dict(bgcolor=PANEL, bordercolor=BORDER, font_color=TEXT),
        title=dict(font=dict(size=15, color=TEXT)),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=BORDER)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=BORDER)
    fig.update_coloraxes(colorbar=dict(outlinewidth=0, tickcolor=BORDER, title=""))
    return fig


def kpi(label, value, sub):
    return (
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>'
    )


def section(title, caption=None):
    st.markdown(f'<div class="section">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="caption">{caption}</div>', unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.4rem;font-weight:800;letter-spacing:-0.01em">'
        '🛰️ Defense Spend</div>'
        '<div style="color:#6f7c9b;font-size:0.82rem;margin-bottom:1rem">Controls</div>',
        unsafe_allow_html=True,
    )

    dataset = st.radio("Dataset", ["SIPRI 2024 (Top 40)", "IISS 2025 (Top 15)"], index=0)
    max_n = 40 if "SIPRI" in dataset else 15
    top_n = st.slider("Countries to display", 5, max_n, min(10, max_n), step=5)
    chart_type = st.selectbox(
        "Rankings chart", ["Bar", "Horizontal Bar", "Treemap", "Pie", "Scatter (vs % GDP)"]
    )

    st.markdown("<hr style='border-color:#243049'>", unsafe_allow_html=True)
    st.markdown(
        "**Sources**  \n"
        "[SIPRI / IISS via Wikipedia]"
        "(https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures)",
    )
    st.caption("All figures in current US$ billions. Estimates differ by source and year.")

# ── Active dataset ───────────────────────────────────────────────────────────
df = sipri.copy() if "SIPRI" in dataset else iiss.copy()
df_display = df.nlargest(top_n, SPEND)

total = sipri[SPEND].sum()
top5_share = sipri.nlargest(5, SPEND)[SPEND].sum() / total * 100

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero">'
    '<span class="pill">● GLOBAL DEFENSE INTELLIGENCE</span>'
    "<h1>Global Military Expenditure</h1>"
    "<p>Interactive analysis of worldwide defense spending — SIPRI 2024 &amp; IISS 2025.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── KPI row ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="kpi-grid">'
    + kpi("Total Tracked Spending", f"${total:,.0f}B", "SIPRI 2024 · 40 nations")
    + kpi("Top Spender", sipri.iloc[0]["Country"],
          f"<b>${sipri.iloc[0][SPEND]:,.0f}B</b> · {sipri.iloc[0]['% of global spending']}% of total")
    + kpi("Top-5 Concentration", f"{top5_share:.0f}%", "share held by 5 nations")
    + kpi("Highest % of GDP", gdp_sipri.iloc[0]["Country"],
          f"<b>{gdp_sipri.iloc[0]['% of GDP']}%</b> of GDP")
    + "</div>",
    unsafe_allow_html=True,
)

st.write("")

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_overview, tab_rank, tab_gdp, tab_cmp, tab_data = st.tabs(
    ["🌍  Overview", "🏆  Rankings", "💰  % of GDP", "🔄  Source Comparison", "📋  Data"]
)

# ── Overview: world map + leaders ────────────────────────────────────────────
with tab_overview:
    section("Where the money goes", "Military spending by country (SIPRI 2024, US$ bn)")
    world = px.choropleth(
        sipri, locations="ISO3", locationmode="ISO-3",
        color=SPEND, color_continuous_scale=SEQUENTIAL,
        hover_name="Country",
        hover_data={SPEND: ":,.1f", "% of GDP": True, "ISO3": False},
    )
    world.update_geos(
        bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False,
        landcolor="#10182c", showland=True, showocean=True, oceancolor="#0b1020",
        projection_type="natural earth",
    )
    style_fig(world, height=480, show_legend=False)
    world.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(world)

    col1, col2 = st.columns([3, 2])
    with col1:
        section("Top 10 spenders")
        top10 = sipri.nlargest(10, SPEND).iloc[::-1]
        fig = px.bar(top10, x=SPEND, y="Country", orientation="h",
                     color=SPEND, color_continuous_scale=SEQUENTIAL, text=SPEND)
        fig.update_traces(texttemplate="$%{text:,.0f}B", textposition="outside",
                          cliponaxis=False)
        st.plotly_chart(style_fig(fig, height=420, show_legend=False))
    with col2:
        section("By region")
        reg = (sipri.groupby("Region")[SPEND].sum()
               .sort_values(ascending=False).reset_index())
        fig = px.pie(reg, values=SPEND, names="Region", hole=0.55,
                     color_discrete_sequence=CATEGORICAL)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(style_fig(fig, height=420, show_legend=False))

# ── Rankings (configurable) ──────────────────────────────────────────────────
with tab_rank:
    label = dataset.split("(")[0].strip()
    section(f"Top {top_n} military spenders", f"{label} · {chart_type}")

    if chart_type == "Bar":
        fig = px.bar(df_display, x="Country", y=SPEND, text=SPEND,
                     color=SPEND, color_continuous_scale=SEQUENTIAL)
        fig.update_traces(texttemplate="$%{text:,.0f}B", textposition="outside",
                          cliponaxis=False)
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(style_fig(fig, show_legend=False))

    elif chart_type == "Horizontal Bar":
        fig = px.bar(df_display.iloc[::-1], x=SPEND, y="Country", orientation="h",
                     text=SPEND, color=SPEND, color_continuous_scale=SEQUENTIAL)
        fig.update_traces(texttemplate="$%{text:,.0f}B", textposition="outside",
                          cliponaxis=False)
        st.plotly_chart(style_fig(fig, height=max(420, top_n * 34), show_legend=False))

    elif chart_type == "Treemap":
        fig = px.treemap(df_display, path=["Country"], values=SPEND,
                         color=SPEND, color_continuous_scale=SEQUENTIAL)
        fig.update_traces(marker=dict(cornerradius=6),
                          texttemplate="<b>%{label}</b><br>$%{value:,.0f}B")
        st.plotly_chart(style_fig(fig, show_legend=False))

    elif chart_type == "Pie":
        fig = px.pie(df_display, values=SPEND, names="Country", hole=0.5,
                     color_discrete_sequence=CATEGORICAL)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(style_fig(fig, show_legend=False))

    elif chart_type == "Scatter (vs % GDP)":
        if "% of GDP" in df_display.columns:
            fig = px.scatter(df_display, x=SPEND, y="% of GDP",
                             size="% of global spending", color="Region",
                             hover_name="Country", size_max=55,
                             color_discrete_sequence=CATEGORICAL)
            fig.update_layout(xaxis_title="Spending (US$ bn)", yaxis_title="% of GDP")
            st.plotly_chart(style_fig(fig))
        else:
            st.info("The scatter view needs the % of GDP column — switch to **SIPRI 2024**.")

# ── % of GDP ─────────────────────────────────────────────────────────────────
with tab_gdp:
    section("Military burden — spending as % of GDP",
            "A country can spend little in absolute terms yet carry a heavy defense burden.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SIPRI 2024 — Top 25**")
        fig = px.bar(gdp_sipri, x="Country", y="% of GDP",
                     color="% of GDP", color_continuous_scale=GDP_SCALE)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_fig(fig, height=440, show_legend=False))
    with col2:
        st.markdown("**IISS 2020 — Top 15**")
        fig = px.bar(gdp_iiss, x="Country", y="% of GDP",
                     color="% of GDP", color_continuous_scale=GDP_SCALE)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_fig(fig, height=440, show_legend=False))

    st.markdown(
        f'<div class="insight"><b>Key insight:</b> Ukraine carries the heaviest burden at '
        f'<b>{gdp_sipri.iloc[0]["% of GDP"]}% of GDP</b> — far above any other nation — '
        "reflecting the ongoing conflict, while large absolute spenders like the US "
        "(3.4%) and China (1.7%) sit far lower relative to their economies.</div>",
        unsafe_allow_html=True,
    )

# ── Source comparison ────────────────────────────────────────────────────────
with tab_cmp:
    section("SIPRI 2024 vs IISS 2025", "Where the two leading sources agree — and don't.")
    merged = pd.merge(
        sipri[["Country", SPEND]], iiss[["Country", SPEND]],
        on="Country", how="inner", suffixes=("_SIPRI", "_IISS"),
    )
    merged["Difference"] = merged[f"{SPEND}_SIPRI"] - merged[f"{SPEND}_IISS"]
    merged = merged.sort_values(f"{SPEND}_SIPRI", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="SIPRI 2024", x=merged["Country"],
                         y=merged[f"{SPEND}_SIPRI"], marker_color=ACCENT))
    fig.add_trace(go.Bar(name="IISS 2025", x=merged["Country"],
                         y=merged[f"{SPEND}_IISS"], marker_color=ACCENT_2))
    fig.update_layout(barmode="group", xaxis_tickangle=-45)
    st.plotly_chart(style_fig(fig, height=460))

    col1, col2 = st.columns([3, 2])
    with col1:
        section("Difference (SIPRI − IISS)")
        st.dataframe(
            merged.rename(columns={
                f"{SPEND}_SIPRI": "SIPRI ($bn)", f"{SPEND}_IISS": "IISS ($bn)"
            })[["Country", "SIPRI ($bn)", "IISS ($bn)", "Difference"]].round(1),
            width="stretch", hide_index=True, height=360,
        )
    with col2:
        section("Regional totals")
        reg = (sipri.groupby("Region")[SPEND]
               .agg(["sum", "mean", "count"]).round(1)
               .rename(columns={"sum": "Total", "mean": "Avg", "count": "Nations"})
               .sort_values("Total", ascending=False).reset_index())
        st.dataframe(reg, width="stretch", hide_index=True, height=360)

# ── Data ─────────────────────────────────────────────────────────────────────
with tab_data:
    section("Full dataset", f"{dataset} — search, sort and export.")
    search = st.text_input("Search country", "", placeholder="e.g. India")
    filtered = (df[df["Country"].str.contains(search, case=False, na=False)]
                if search else df)
    st.dataframe(filtered, width="stretch", hide_index=True, height=420)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(
            "⬇  Download CSV", filtered.to_csv(index=False).encode("utf-8"),
            file_name=f"{'sipri' if 'SIPRI' in dataset else 'iiss'}_military_spending.csv",
            mime="text/csv", width="stretch",
        )
    with col2:
        st.caption(
            f"{filtered.shape[0]} rows × {filtered.shape[1]} columns · "
            f"columns: {', '.join(df.columns)}"
        )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center;color:#6f7c9b;font-size:0.85rem;margin-top:1.5rem'>"
    "Data: <a style='color:#8a96b3' href='https://en.wikipedia.org/wiki/"
    "List_of_countries_with_highest_military_expenditures'>Wikipedia — SIPRI &amp; IISS</a>"
    " · Built with Streamlit &amp; Plotly</div>",
    unsafe_allow_html=True,
)
