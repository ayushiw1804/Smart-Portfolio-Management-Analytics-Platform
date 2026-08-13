# ==============================================================================
# AI-POWERED PORTFOLIO INTELLIGENCE PLATFORM (STREAMLIT MULTI-DASHBOARD APP)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# 1. Page Configuration (Wide layout, visible sidebar)
st.set_page_config(
    page_title="RM DASHBOARD - Relationship Manager Performance & Portfolio Overview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Theme State Management (Default to Light Power BI Canvas matching reference image)
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# 3. CSS Design System Injection (Exact match to Power BI reference image)
CSS_VARIABLES = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

/* Hide default Streamlit header/footer chrome */
header[data-testid="stHeader"], footer, [data-testid="stDecoration"], .stDeployButton {{
    display: none !important;
}}

:root {{
    --bg-app: {'#0f172a' if IS_DARK else '#f4f6f9'};
    --bg-sidebar: {'#090d16' if IS_DARK else '#081a36'};
    --bg-card: {'rgba(30, 41, 59, 0.85)' if IS_DARK else '#ffffff'};
    --border-color: {'rgba(255, 255, 255, 0.1)' if IS_DARK else '#e2e8f0'};
    --text-main: {'#f8fafc' if IS_DARK else '#0f172a'};
    --text-muted: {'#94a3b8' if IS_DARK else '#64748b'};
    --shadow-sm: {'0 4px 20px rgba(0, 0, 0, 0.35)' if IS_DARK else '0 2px 8px rgba(0,0,0,0.05)'};
    --radius: 10px;
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: var(--bg-app) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
}}

.block-container {{
    padding: 0.8rem 1.5rem 2rem !important;
    max-width: 1600px !important;
}}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {{
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding-top: 1rem !important;
}}
[data-testid="stSidebar"] * {{
    color: #ffffff !important;
}}

.sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    margin-bottom: 1rem;
}}
.sidebar-brand-icon {{
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}}
.sidebar-brand-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.3px;
}}
.sidebar-brand-subtitle {{
    font-size: 0.7rem;
    color: #94a3b8 !important;
}}

/* Header Main */
.dashboard-title-main {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-main);
    margin: 0;
    line-height: 1.1;
}}
.dashboard-subtitle-main {{
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 0;
}}

/* KPI Cards Row Grid */
.kpi-card-box {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 12px 14px;
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    gap: 12px;
    height: 100%;
}}
.kpi-circle-icon {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}}
.kpi-lbl {{ font-size: 0.74rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.3px; }}
.kpi-val {{ font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 800; color: var(--text-main); margin: 1px 0; }}
.kpi-sub {{ font-size: 0.7rem; font-weight: 700; display: inline-flex; align-items: center; gap: 3px; }}
.sub-pos {{ color: #10b981; }}
.sub-neg {{ color: #ef4444; }}

/* Card Visual Wrappers */
.visual-box {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 14px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 14px;
}}
.visual-hdr-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 2px;
}}
.visual-hdr-sub {{
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-top: 6px;
    border-top: 1px solid var(--border-color);
    padding-top: 6px;
    font-style: italic;
}}

/* Data Tables */
.pbi-table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
.pbi-table th {{ text-align: left; padding: 6px 8px; color: var(--text-muted); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; border-bottom: 2px solid var(--border-color); background: {'rgba(255,255,255,0.05)' if IS_DARK else '#f8fafc'}; }}
.pbi-table td {{ padding: 6px 8px; color: var(--text-main); border-bottom: 1px solid var(--border-color); vertical-align: middle; }}

.badge-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; text-align: center; }}
.badge-critical {{ background: #fee2e2; color: #991b1b; }}
.badge-warning {{ background: #fef3c7; color: #92400e; }}
.badge-success {{ background: #d1fae5; color: #065f46; }}

/* Profile Card */
.profile-card-box {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 18px;
    box-shadow: var(--shadow-sm);
}}
</style>
"""
st.markdown(CSS_VARIABLES, unsafe_allow_html=True)

# 4. Plotly Chart Theme Setup
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#64748b" if not IS_DARK else "#94a3b8", size=11),
    margin=dict(l=10, r=10, t=25, b=10),
    xaxis=dict(
        gridcolor="rgba(0,0,0,0.05)" if not IS_DARK else "rgba(255,255,255,0.05)",
        zerolinecolor="rgba(0,0,0,0.05)",
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,0.05)" if not IS_DARK else "rgba(255,255,255,0.05)",
        zerolinecolor="rgba(0,0,0,0.05)",
    ),
)

# 5. Datasets
MONTHLY_REVENUE = pd.DataFrame([
    {"month": "Apr 2024", "rev": 2.8, "lbl": "₹2.8M"},
    {"month": "Jun 2024", "rev": 3.1, "lbl": "₹3.1M"},
    {"month": "Aug 2024", "rev": 3.6, "lbl": "₹3.6M"},
    {"month": "Oct 2024", "rev": 3.9, "lbl": "₹3.9M"},
    {"month": "Dec 2024", "rev": 4.6, "lbl": "₹4.6M"},
    {"month": "Feb 2025", "rev": 5.3, "lbl": "₹5.3M"}
])

PRODUCT_DIST = pd.DataFrame([
    {"product": "Home Loan", "pct": 35, "color": "#2563eb"},
    {"product": "Credit Card", "pct": 20, "color": "#10b981"},
    {"product": "Mutual Funds", "pct": 18, "color": "#f59e0b"},
    {"product": "Insurance", "pct": 15, "color": "#8b5cf6"},
    {"product": "Personal Loan", "pct": 12, "color": "#06b6d4"}
])

LOAN_PIPELINE = pd.DataFrame([
    {"stage": "Leads", "count": 2100, "lbl": "2,100", "color": "#2563eb"},
    {"stage": "Application", "count": 1600, "lbl": "1,600", "color": "#10b981"},
    {"stage": "Verification", "count": 1200, "lbl": "1,200", "color": "#f59e0b"},
    {"stage": "Approved", "count": 980, "lbl": "980", "color": "#8b5cf6"},
    {"stage": "Disbursed", "count": 850, "lbl": "850", "color": "#06b6d4"}
])

RM_PERFORMANCE = pd.DataFrame([
    {"rm": "RM A", "revenue": 9.8, "lbl": "9.8M", "color": "#2563eb"},
    {"rm": "RM B", "revenue": 7.6, "lbl": "7.6M", "color": "#10b981"},
    {"rm": "RM C", "revenue": 6.4, "lbl": "6.4M", "color": "#f59e0b"},
    {"rm": "RM D", "revenue": 4.9, "lbl": "4.9M", "color": "#8b5cf6"},
    {"rm": "RM E", "revenue": 3.7, "lbl": "3.7M", "color": "#06b6d4"}
])

RISK_DIST = pd.DataFrame([
    {"category": "High Risk (482)", "pct": 8.7, "color": "#ef4444"},
    {"category": "Medium Risk (2,216)", "pct": 17.6, "color": "#f59e0b"},
    {"category": "Low Risk (9,870)", "pct": 73.7, "color": "#10b981"}
])

TOP_HIGH_RISK = pd.DataFrame([
    {"name": "Amit Verma", "aum": "₹ 28,45,000", "score": 92, "pd": "89%"},
    {"name": "Rajesh Kumar", "aum": "₹ 35,20,000", "score": 89, "pd": "85%"},
    {"name": "Sunil Sharma", "aum": "₹ 22,10,000", "score": 88, "pd": "83%"},
    {"name": "Neha Singh", "aum": "₹ 18,75,000", "score": 86, "pd": "80%"},
    {"name": "Vikram Patel", "aum": "₹ 26,80,000", "score": 85, "pd": "79%"},
    {"name": "Manoj Tiwari", "aum": "₹ 31,60,000", "score": 83, "pd": "77%"},
    {"name": "Pooja Mehta", "aum": "₹ 17,90,000", "score": 82, "pd": "75%"},
    {"name": "Anil Gupta", "aum": "₹ 19,40,000", "score": 81, "pd": "74%"},
    {"name": "Rohit Agarwal", "aum": "₹ 16,30,000", "score": 80, "pd": "72%"},
    {"name": "Karan Malhotra", "aum": "₹ 15,20,000", "score": 79, "pd": "70%"}
])

CALL_PRIORITIES = pd.DataFrame([
    {"name": "Rahul Mehta", "priority": "High ▲", "reason": "High Risk & No Contact for 45 Days", "aum": "₹ 22,50,000", "score": 91, "contact": "45 Days Ago", "action": "Call Today"},
    {"name": "Sneha Kapoor", "priority": "High ▲", "reason": "Loan Renewal Due in 7 Days", "aum": "₹ 18,20,000", "score": 68, "contact": "2 Days Ago", "action": "Discuss Renewal"},
    {"name": "Vivek Sharma", "priority": "Medium ↔", "reason": "Cross Sell Opportunity", "aum": "₹ 9,80,000", "score": 55, "contact": "5 Days Ago", "action": "Offer Insurance"},
    {"name": "Karan Singh", "priority": "Medium ↔", "reason": "High Value Customer", "aum": "₹ 34,60,000", "score": 40, "contact": "10 Days Ago", "action": "Relationship Check-in"},
    {"name": "Anjali Verma", "priority": "Low ▼", "reason": "Regular Follow-up", "aum": "₹ 6,70,000", "score": 25, "contact": "3 Days Ago", "action": "General Check-in"}
])

CHURN_TREND = pd.DataFrame([
    {"month": "Apr 2024", "rate": 7.8, "lbl": "7.8%"},
    {"month": "Jun 2024", "rate": 7.2, "lbl": "7.2%"},
    {"month": "Aug 2024", "rate": 7.6, "lbl": "7.6%"},
    {"month": "Oct 2024", "rate": 7.1, "lbl": "7.1%"},
    {"month": "Dec 2024", "rate": 6.9, "lbl": "6.9%"},
    {"month": "Feb 2025", "rate": 6.3, "lbl": "6.3%"}
])

CUSTOMER_DEMOGRAPHICS = pd.DataFrame([
    {"age_group": "18-30 Yrs", "pct": 15, "count": 1885},
    {"age_group": "31-45 Yrs", "pct": 42, "count": 5278},
    {"age_group": "46-60 Yrs", "pct": 31, "count": 3896},
    {"age_group": "60+ Yrs", "pct": 12, "count": 1509},
])

CUSTOMER_TIERS = pd.DataFrame([
    {"tier": "HNI (> ₹50L)", "clients": 1240, "aum": "₹ 740 Cr", "avg_rev": "₹ 1.85L"},
    {"tier": "Emerging HNI (₹25L-₹50L)", "clients": 2480, "aum": "₹ 620 Cr", "avg_rev": "₹ 95K"},
    {"tier": "Mass Affluent (₹10L-₹25L)", "clients": 4120, "aum": "₹ 380 Cr", "avg_rev": "₹ 42K"},
    {"tier": "Retail (< ₹10L)", "clients": 4728, "aum": "₹ 84.5 Cr", "avg_rev": "₹ 15K"},
])

RISK_MIGRATION = pd.DataFrame([
    {"rating": "AAA", "exposure": 320, "pct": 38.0},
    {"rating": "AA", "exposure": 240, "pct": 28.5},
    {"rating": "A", "exposure": 150, "pct": 17.8},
    {"rating": "BBB", "exposure": 75, "pct": 8.9},
    {"rating": "BB & Below", "exposure": 57.1, "pct": 6.8},
])

CHURN_DRIVERS = pd.DataFrame([
    {"driver": "Low Engagement (<3 visits/yr)", "pct": 35, "impact": "High"},
    {"driver": "High Fee Dissatisfaction", "pct": 24, "impact": "High"},
    {"driver": "Better Competitor Rates", "pct": 20, "impact": "Medium"},
    {"driver": "Service Delay Issue", "pct": 15, "impact": "Medium"},
    {"driver": "Product Incompatibility", "pct": 6, "impact": "Low"},
])

RM_TARGETS = pd.DataFrame([
    {"rm": "RM A (Anand)", "actual": 9.8, "target": 8.5, "branch": "North"},
    {"rm": "RM B (Bhavna)", "actual": 7.6, "target": 7.0, "branch": "South"},
    {"rm": "RM C (Chetan)", "actual": 6.4, "target": 6.5, "branch": "West"},
    {"rm": "RM D (Deepak)", "actual": 4.9, "target": 5.5, "branch": "East"},
    {"rm": "RM E (Esha)", "actual": 3.7, "target": 4.0, "branch": "North"},
])

LOAN_PRODUCT_MIX = pd.DataFrame([
    {"product": "Home Loans", "value": 166.6, "pct": 52},
    {"product": "Personal Loans", "value": 70.5, "pct": 22},
    {"product": "Business Loans", "value": 57.7, "pct": 18},
    {"product": "Auto Loans", "value": 25.7, "pct": 8},
])

# 6. Sidebar Navigation
with st.sidebar:
    st.markdown("""<div class="sidebar-brand"><div class="sidebar-brand-icon">📊</div><div><div class="sidebar-brand-title">RM Dashboard</div><div class="sidebar-brand-subtitle">AI Portfolio Intelligence</div></div></div>""", unsafe_allow_html=True)

    nav_option = st.radio(
        "Navigation",
        [
            "📊 Executive Summary",
            "👤 Customer Analytics",
            "🛡️ Risk Analytics",
            "🔄 Churn Analytics",
            "📊 RM Performance",
            "🏛️ Loan Pipeline",
            "👤 Customer 360°",
            "⚡ Big Data Stream",
            "🧠 ML Optimizer",
            "🤖 AI Copilot"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="font-size:0.78rem; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px; display:flex; align-items:center; gap:8px;">📅 <span>Data as on: <strong>31-03-2025</strong></span></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    theme_btn_lbl = "☀️ Light Canvas" if IS_DARK else "🌙 Dark Canvas"
    if st.button(theme_btn_lbl, use_container_width=True):
        toggle_theme()
        st.rerun()

# 7. Main Header
hdr_col1, hdr_col2 = st.columns([6, 6])
with hdr_col1:
    sub_title = nav_option.replace('📊 ', '').replace('👤 ', '').replace('🛡️ ', '').replace('🔄 ', '').replace('🏛️ ', '').replace('⚡ ', '').replace('🧠 ', '').replace('🤖 ', '')
    st.markdown(f"""<div><h1 class="dashboard-title-main">RM DASHBOARD</h1><p class="dashboard-subtitle-main">{sub_title} • Relationship Manager Performance & Portfolio Overview</p></div>""", unsafe_allow_html=True)

with hdr_col2:
    f1, f2, f3, f4, f5 = st.columns([2.2, 2, 2, 2, 1.2])
    with f1:
        d_start = st.date_input("Date", value=date(2024, 4, 1), label_visibility="collapsed")
    with f2:
        d_end = st.date_input("Date End", value=date(2025, 3, 31), label_visibility="collapsed")
    with f3:
        branch = st.selectbox("Branch", ["Branch: All", "North", "South", "West", "East"], label_visibility="collapsed")
    with f4:
        rm = st.selectbox("RM", ["RM Name: All", "RM A", "RM B", "RM C", "RM D", "RM E"], label_visibility="collapsed")
    with f5:
        product = st.selectbox("Prod", ["Product: All", "Home Loan", "Credit Card", "Mutual Funds", "Insurance", "Personal Loan"], label_visibility="collapsed")

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# Navigation Router
if nav_option == "📊 Executive Summary":
    # 6 KPI Summary Cards
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(37,99,235,0.15); color:#2563eb;">👥</div><div><div class="kpi-lbl">Total Customers</div><div class="kpi-val">12,568</div><div class="kpi-sub sub-pos">▲ 8.3% vs Last Year</div></div></div>""", unsafe_allow_html=True)

    with k2:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">💰</div><div><div class="kpi-lbl">Portfolio Value (AUM)</div><div class="kpi-val">₹ 1,82,45,70,000</div><div class="kpi-sub sub-pos">▲ 11.6% vs Last Year</div></div></div>""", unsafe_allow_html=True)

    with k3:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">🪙</div><div><div class="kpi-lbl">Revenue Generated</div><div class="kpi-val">₹ 42,37,25,000</div><div class="kpi-sub sub-pos">▲ 9.2% vs Last Year</div></div></div>""", unsafe_allow_html=True)

    with k4:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(239,68,68,0.15); color:#ef4444;">⚠️</div><div><div class="kpi-lbl">High Risk Customers</div><div class="kpi-val">482</div><div class="kpi-sub sub-neg">▲ 15.4% vs Last Year</div></div></div>""", unsafe_allow_html=True)

    with k5:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(139,92,246,0.15); color:#8b5cf6;">📉</div><div><div class="kpi-lbl">Churn Rate</div><div class="kpi-val">6.85%</div><div class="kpi-sub sub-pos">▼ -1.3% vs Last Year</div></div></div>""", unsafe_allow_html=True)

    with k6:
        st.markdown("""<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(6,182,212,0.15); color:#06b6d4;">📞</div><div><div class="kpi-lbl">Calls Due Today</div><div class="kpi-val">128</div><div class="kpi-sub sub-pos">▲ 6.7% vs Yesterday</div></div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Grid Row 1
    r1_col1, r1_col2, r1_col3 = st.columns([4.2, 3.8, 4])

    with r1_col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Revenue Trend (Monthly)</div>', unsafe_allow_html=True)
        fig_rev = px.line(MONTHLY_REVENUE, x="month", y="rev", markers=True, text="lbl", color_discrete_sequence=["#2563eb"])
        fig_rev.update_traces(
            line=dict(width=2.5),
            marker=dict(size=7, color="#2563eb"),
            textposition="top center",
            textfont=dict(size=10, weight="bold")
        )
        fig_rev.update_layout(**PLOT_LAYOUT, height=220, yaxis_title="Revenue (₹ M)", yaxis_range=[0, 6.5])
        st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Shows the monthly revenue generated from the customer portfolio. Helps in identifying revenue growth trends and seasonal patterns.</div></div>', unsafe_allow_html=True)

    with r1_col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Portfolio Distribution by Product</div>', unsafe_allow_html=True)
        fig_prod = px.pie(PRODUCT_DIST, names="product", values="pct", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"], hole=0.62)
        fig_prod.update_traces(textinfo="percent", textfont=dict(size=11, weight="bold"))
        fig_prod.update_layout(
            **PLOT_LAYOUT, height=220, showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=10)),
            annotations=[dict(text="<b>₹ 1.82B</b><br><span style='font-size:10px;color:#64748b;'>Total</span>", x=0.5, y=0.5, font_size=13, showarrow=False)]
        )
        st.plotly_chart(fig_prod, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Shows the distribution of total portfolio value across different products. Helps in understanding which products contribute the most.</div></div>', unsafe_allow_html=True)

    with r1_col3:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Loan Pipeline (This Year)</div>', unsafe_allow_html=True)
        fig_funnel = px.funnel(LOAN_PIPELINE, y="stage", x="count", text="lbl", color="stage", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"])
        fig_funnel.update_traces(textposition="inside", textfont=dict(size=11, color="#ffffff", weight="bold"))
        fig_funnel.update_layout(**PLOT_LAYOUT, height=220, showlegend=False)
        st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Shows the number of customers at each stage of the loan process. Helps in analyzing conversion rate and drop-offs.</div></div>', unsafe_allow_html=True)

    # Grid Row 2
    r2_col1, r2_col2, r2_col3 = st.columns([3.8, 4, 4.2])

    with r2_col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">RM Performance (Revenue)</div>', unsafe_allow_html=True)
        fig_rm = px.bar(RM_PERFORMANCE, x="rm", y="revenue", text="lbl", color="rm", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"])
        fig_rm.update_traces(textposition="outside", textfont=dict(size=10, weight="bold"))
        fig_rm.update_layout(**PLOT_LAYOUT, height=210, showlegend=False, yaxis_title="Revenue (₹ M)", yaxis_range=[0, 11])
        st.plotly_chart(fig_rm, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Compares revenue generated by each Relationship Manager. Helps in identifying top performers and providing support to others.</div></div>', unsafe_allow_html=True)

    with r2_col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Risk Distribution (Customers)</div>', unsafe_allow_html=True)
        fig_risk = px.pie(RISK_DIST, names="category", values="pct", color_discrete_sequence=["#ef4444", "#f59e0b", "#10b981"], hole=0.62)
        fig_risk.update_traces(textinfo="percent", textfont=dict(size=11, weight="bold"))
        fig_risk.update_layout(
            **PLOT_LAYOUT, height=210, showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=10))
        )
        st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Shows the distribution of customers based on risk levels. Helps in focusing on high-risk customers for timely actions.</div></div>', unsafe_allow_html=True)

    with r2_col3:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Top 10 High Risk Customers</div>', unsafe_allow_html=True)
        rows_html = ""
        for _, r in TOP_HIGH_RISK.iterrows():
            badge_cls = "badge-critical" if r['score'] >= 88 else "badge-warning"
            rows_html += f"<tr><td><strong>{r['name']}</strong></td><td>{r['aum']}</td><td><span class=\"badge-tag {badge_cls}\">{r['score']}</span></td><td><strong style=\"color:#ef4444;\">{r['pd']}</strong></td></tr>"
        st.markdown(f"""<div style="height:190px; overflow-y:auto;"><table class="pbi-table"><thead><tr><th>Customer Name</th><th>Portfolio Value</th><th>Risk Score</th><th>Prob. Default</th></tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)
        st.markdown('<div class="visual-hdr-sub">Lists the top 10 customers with the highest risk. Helps RM to prioritize follow-ups and risk mitigation.</div></div>', unsafe_allow_html=True)

    # Grid Row 3
    r3_col1, r3_col2 = st.columns([7.5, 4.5])

    with r3_col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Today\'s Call Priorities</div>', unsafe_allow_html=True)
        call_rows = ""
        for _, c in CALL_PRIORITIES.iterrows():
            p_badge = "badge-critical" if "High" in c['priority'] else ("badge-warning" if "Medium" in c['priority'] else "badge-success")
            s_badge = "badge-critical" if c['score'] > 80 else ("badge-warning" if c['score'] > 50 else "badge-success")
            call_rows += f"<tr><td><strong>{c['name']}</strong></td><td><span class=\"badge-tag {p_badge}\">{c['priority']}</span></td><td>{c['reason']}</td><td>{c['aum']}</td><td><span class=\"badge-tag {s_badge}\">{c['score']}</span></td><td>{c['contact']}</td><td><em>{c['action']}</em></td></tr>"
        st.markdown(f"""<table class="pbi-table"><thead><tr><th>Customer Name</th><th>Priority</th><th>Reason</th><th>Portfolio Value</th><th>Risk Score</th><th>Last Contact</th><th>Next Action</th></tr></thead><tbody>{call_rows}</tbody></table>""", unsafe_allow_html=True)
        st.markdown('<div class="visual-hdr-sub">Prioritized call follow-ups for RMs based on default risk alerts and loan renewal schedules.</div></div>', unsafe_allow_html=True)

    with r3_col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Churn Rate Trend</div>', unsafe_allow_html=True)
        fig_churn = px.line(CHURN_TREND, x="month", y="rate", markers=True, text="lbl", color_discrete_sequence=["#ef4444"])
        fig_churn.update_traces(
            line=dict(width=2.5),
            marker=dict(size=7, color="#ef4444"),
            textposition="top center",
            textfont=dict(size=10, color="#ef4444", weight="bold")
        )
        fig_churn.update_layout(**PLOT_LAYOUT, height=195, yaxis_title="Rate (%)", yaxis_range=[0, 10])
        st.plotly_chart(fig_churn, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Shows the monthly churn rate trend. Helps in evaluating retention strategies effectiveness.</div></div>', unsafe_allow_html=True)

elif nav_option == "👤 Customer Analytics":
    # Customer Analytics Dashboard
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(37,99,235,0.15); color:#2563eb;">👥</div><div><div class="kpi-lbl">Total Customers</div><div class="kpi-val">12,568</div><div class="kpi-sub sub-pos">▲ 93.2% Active</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">💎</div><div><div class="kpi-lbl">HNW Clients (>₹50L)</div><div class="kpi-val">1,240</div><div class="kpi-sub sub-pos">38% Total AUM</div></div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">📊</div><div><div class="kpi-lbl">Avg AUM / Client</div><div class="kpi-val">₹ 14.52 L</div><div class="kpi-sub sub-pos">▲ 6.4% YoY</div></div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(139,92,246,0.15); color:#8b5cf6;">⭐</div><div><div class="kpi-lbl">Net Promoter Score</div><div class="kpi-val">74 / 100</div><div class="kpi-sub sub-pos">Top Decile</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Customer Age Group Demographics</div>', unsafe_allow_html=True)
        fig_demo = px.bar(CUSTOMER_DEMOGRAPHICS, x="age_group", y="count", text="pct", color="age_group", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#8b5cf6"])
        fig_demo.update_traces(texttemplate="%{y:,} (%{text}%)", textposition="outside", textfont=dict(size=10, weight="bold"))
        fig_demo.update_layout(**PLOT_LAYOUT, height=240, showlegend=False, yaxis_title="Customer Count")
        st.plotly_chart(fig_demo, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Distribution of customer base across age brackets. Prime wealth accumulation segment is 31-45 Yrs (42%).</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Customer Segmentation Tiers</div>', unsafe_allow_html=True)
        rows_tier = ""
        for _, t in CUSTOMER_TIERS.iterrows():
            rows_tier += f"<tr><td><strong>{t['tier']}</strong></td><td>{t['clients']:,}</td><td>{t['aum']}</td><td><span class='badge-tag badge-success'>{t['avg_rev']}</span></td></tr>"
        st.markdown(f"""<table class="pbi-table"><thead><tr><th>Tier Segment</th><th>Clients</th><th>Total AUM</th><th>Avg Revenue / Yr</th></tr></thead><tbody>{rows_tier}</tbody></table>""", unsafe_allow_html=True)
        st.markdown('<div class="visual-hdr-sub">Detailed breakdown of wealth management client tiers, total AUM contribution, and annual fee revenue.</div></div>', unsafe_allow_html=True)

elif nav_option == "🛡️ Risk Analytics":
    # Risk Analytics Dashboard
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(239,68,68,0.15); color:#ef4444;">🛡️</div><div><div class="kpi-lbl">Risk-Weighted Exposure</div><div class="kpi-val">₹ 842.10 Cr</div><div class="kpi-sub sub-neg">Basel III Standardized</div></div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">⚠️</div><div><div class="kpi-lbl">High Risk Accounts</div><div class="kpi-val">482</div><div class="kpi-sub sub-neg">PD > 70%</div></div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(37,99,235,0.15); color:#2563eb;">📉</div><div><div class="kpi-lbl">Portfolio Avg PD</div><div class="kpi-val">2.84%</div><div class="kpi-sub sub-pos">Below Risk Limit 3.5%</div></div></div>', unsafe_allow_html=True)
    with r4:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">🏦</div><div><div class="kpi-lbl">Capital Adequacy Ratio</div><div class="kpi-val">16.4%</div><div class="kpi-sub sub-pos">Regulatory Buffer 11.5%</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Credit Risk Rating Migration Exposure (₹ Cr)</div>', unsafe_allow_html=True)
        fig_mig = px.bar(RISK_MIGRATION, x="rating", y="exposure", text="pct", color="rating", color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ef4444"])
        fig_mig.update_traces(texttemplate="₹%{y}Cr (%{text}%)", textposition="outside", textfont=dict(size=10, weight="bold"))
        fig_mig.update_layout(**PLOT_LAYOUT, height=240, showlegend=False, yaxis_title="Exposure (₹ Cr)", yaxis_range=[0, 380])
        st.plotly_chart(fig_mig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Portfolio exposure segmented by Internal Credit Rating tiers. 66.5% of exposure is rated Investment Grade (AAA/AA).</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Interactive Stress Testing Simulator</div>', unsafe_allow_html=True)
        bps = st.slider("Interest Rate Hike (+Bps)", min_value=0, max_value=400, value=150, step=25)
        eq_drop = st.slider("Equity Market Crash (%)", min_value=-40, max_value=0, value=-15, step=5)
        
        loss_pct = ((bps / 10000) * 0.4 + (eq_drop / 100) * 0.35) * 100
        stressed_aum = 182.45 * (1 + loss_pct / 100)
        
        st.markdown(f"""<div style="background:rgba(239,68,68,0.08); padding:12px; border-radius:8px; border:1px solid rgba(239,68,68,0.2); margin-top:8px;"><p style="margin:0; font-size:0.88rem;">Baseline AUM: <strong>₹ 182.45 Cr</strong></p><p style="margin:4px 0 0; font-size:1.1rem; font-weight:800; color:#ef4444;">Stressed AUM: ₹ {stressed_aum:.2f} Cr ({loss_pct:.2f}%)</p></div>""", unsafe_allow_html=True)
        st.markdown('<div class="visual-hdr-sub">Simulates macroeconomic shocks on overall Relationship Manager portfolio AUM based on sensitivity factors.</div></div>', unsafe_allow_html=True)

elif nav_option == "🔄 Churn Analytics":
    # Churn Analytics Dashboard
    ch1, ch2, ch3, ch4 = st.columns(4)
    with ch1:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(139,92,246,0.15); color:#8b5cf6;">📉</div><div><div class="kpi-lbl">Monthly Churn Rate</div><div class="kpi-val">6.85%</div><div class="kpi-sub sub-pos">▼ -1.3% YoY</div></div></div>', unsafe_allow_html=True)
    with ch2:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(239,68,68,0.15); color:#ef4444;">⚠️</div><div><div class="kpi-lbl">At-Risk Clients</div><div class="kpi-val">314</div><div class="kpi-sub sub-neg">Churn Prob > 60%</div></div></div>', unsafe_allow_html=True)
    with ch3:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">💸</div><div><div class="kpi-lbl">Revenue at Risk</div><div class="kpi-val">₹ 18.40 Cr</div><div class="kpi-sub sub-neg">Annualized Fees</div></div></div>', unsafe_allow_html=True)
    with ch4:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">🎯</div><div><div class="kpi-lbl">Retention Campaign Save Rate</div><div class="kpi-val">68.2%</div><div class="kpi-sub sub-pos">Top Performer</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Primary Predictive Churn Drivers</div>', unsafe_allow_html=True)
        fig_drv = px.bar(CHURN_DRIVERS, x="pct", y="driver", orientation="h", text="pct", color="impact", color_discrete_sequence=["#ef4444", "#f59e0b", "#3b82f6"])
        fig_drv.update_traces(texttemplate="%{x}%", textposition="outside", textfont=dict(size=10, weight="bold"))
        fig_drv.update_layout(**PLOT_LAYOUT, height=240, showlegend=True, xaxis_title="Impact Contribution (%)", xaxis_range=[0, 42])
        st.plotly_chart(fig_drv, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Key customer signals triggering ML churn risk models. Low portal engagement (<3 visits/yr) is top driver (35%).</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">12-Month Churn Rate Progression vs Industry Benchmark</div>', unsafe_allow_html=True)
        df_bench = CHURN_TREND.copy()
        df_bench["benchmark"] = [8.5, 8.2, 8.4, 8.1, 7.9, 7.5]
        fig_ch_bench = px.line(df_bench, x="month", y=["rate", "benchmark"], markers=True, color_discrete_sequence=["#ef4444", "#94a3b8"])
        fig_ch_bench.update_traces(line=dict(width=2.5))
        fig_ch_bench.update_layout(**PLOT_LAYOUT, height=240, yaxis_title="Churn Rate (%)", showlegend=True)
        st.plotly_chart(fig_ch_bench, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Comparing monthly customer churn against wealth management industry averages (Benchmark ~7.5%).</div></div>', unsafe_allow_html=True)

elif nav_option == "📊 RM Performance":
    # RM Performance Dashboard
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(37,99,235,0.15); color:#2563eb;">🏆</div><div><div class="kpi-lbl">Top Performer</div><div class="kpi-val">RM A</div><div class="kpi-sub sub-pos">₹ 9.8M Revenue</div></div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">🎯</div><div><div class="kpi-lbl">Target Achievement</div><div class="kpi-val">108.4%</div><div class="kpi-sub sub-pos">▲ Exceeded Plan</div></div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">👥</div><div><div class="kpi-lbl">Avg Clients / RM</div><div class="kpi-val">2,513</div><div class="kpi-sub sub-pos">Optimal Ratio</div></div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(139,92,246,0.15); color:#8b5cf6;">📈</div><div><div class="kpi-lbl">Avg Revenue / RM</div><div class="kpi-val">₹ 6.48 Cr</div><div class="kpi-sub sub-pos">▲ 11.2% YoY</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">RM Revenue Actual vs Target (₹ M)</div>', unsafe_allow_html=True)
        fig_tgt = px.bar(RM_TARGETS, x="rm", y=["actual", "target"], barmode="group", color_discrete_sequence=["#2563eb", "#cbd5e1"])
        fig_tgt.update_layout(**PLOT_LAYOUT, height=240, yaxis_title="Revenue (₹ M)")
        st.plotly_chart(fig_tgt, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Comparison of actual revenue generated versus assigned annual targets for each Relationship Manager.</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">RM Leaderboard Summary</div>', unsafe_allow_html=True)
        rows_rm = ""
        for idx, r in RM_TARGETS.iterrows():
            pct_ach = (r['actual'] / r['target']) * 100
            badge_cls = "badge-success" if pct_ach >= 100 else "badge-warning"
            rows_rm += f"<tr><td><strong>#{idx+1} {r['rm']}</strong></td><td>{r['branch']} Branch</td><td>₹ {r['actual']} M</td><td>₹ {r['target']} M</td><td><span class='badge-tag {badge_cls}'>{pct_ach:.1f}%</span></td></tr>"
        st.markdown(f"""<table class="pbi-table"><thead><tr><th>Rank & RM Name</th><th>Branch</th><th>Actual Rev</th><th>Target</th><th>Target %</th></tr></thead><tbody>{rows_rm}</tbody></table>""", unsafe_allow_html=True)
        st.markdown('<div class="visual-hdr-sub">Ranked relationship manager leaderboard showing branch allocation and sales target completion rate.</div></div>', unsafe_allow_html=True)

elif nav_option == "🏛️ Loan Pipeline":
    # Loan Pipeline Dashboard
    l1, l2, l3, l4 = st.columns(4)
    with l1:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(37,99,235,0.15); color:#2563eb;">🏛️</div><div><div class="kpi-lbl">Active Applications</div><div class="kpi-val">6,680</div><div class="kpi-sub sub-pos">In Pipeline</div></div></div>', unsafe_allow_html=True)
    with l2:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">💵</div><div><div class="kpi-lbl">Total Pipeline Value</div><div class="kpi-val">₹ 320.50 Cr</div><div class="kpi-sub sub-pos">Under Underwriting</div></div></div>', unsafe_allow_html=True)
    with l3:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">🎯</div><div><div class="kpi-lbl">Overall Conversion</div><div class="kpi-val">40.5%</div><div class="kpi-sub sub-pos">Leads to Disbursed</div></div></div>', unsafe_allow_html=True)
    with l4:
        st.markdown('<div class="kpi-card-box"><div class="kpi-circle-icon" style="background:rgba(139,92,246,0.15); color:#8b5cf6;">⏱️</div><div><div class="kpi-lbl">Avg Turnaround Time</div><div class="kpi-val">4.2 Days</div><div class="kpi-sub sub-pos">Fast SLA</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Funnel Stage Conversion Flow</div>', unsafe_allow_html=True)
        fig_fn = px.funnel(LOAN_PIPELINE, y="stage", x="count", text="lbl", color="stage", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"])
        fig_fn.update_traces(textposition="inside", textfont=dict(size=11, color="#ffffff", weight="bold"))
        fig_fn.update_layout(**PLOT_LAYOUT, height=240, showlegend=False)
        st.plotly_chart(fig_fn, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Detailed drop-off tracking across loan workflow stages from initial lead generation to disbursal.</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">Pipeline Value Breakdown by Loan Product</div>', unsafe_allow_html=True)
        fig_pm = px.pie(LOAN_PRODUCT_MIX, names="product", values="value", color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#06b6d4"], hole=0.55)
        fig_pm.update_traces(textinfo="percent+label", textfont=dict(size=10, weight="bold"))
        fig_pm.update_layout(**PLOT_LAYOUT, height=240, showlegend=False)
        st.plotly_chart(fig_pm, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="visual-hdr-sub">Distribution of total pipeline loan value (₹ 320.5 Cr) across Home, Personal, Business, and Auto loans.</div></div>', unsafe_allow_html=True)

elif nav_option == "👤 Customer 360°":
    # Customer 360 Profile Dashboard
    selected_cust = st.selectbox("Select Customer to Inspect:", TOP_HIGH_RISK["name"].tolist())
    cust_data = TOP_HIGH_RISK[TOP_HIGH_RISK["name"] == selected_cust].iloc[0]

    c_col1, c_col2 = st.columns([4, 8])
    with c_col1:
        st.markdown(f"""<div class="profile-card-box"><div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;"><div style="background:linear-gradient(135deg,#2563eb,#1d4ed8); width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.5rem; font-weight:800;">{selected_cust[0]}</div><div><h3 style="margin:0; font-family:'Outfit', sans-serif;">{cust_data['name']}</h3><p style="margin:0; font-size:0.78rem; color:var(--text-muted);">Account ID: CUST-109284 • HNW Client</p></div></div><hr style="border-color:var(--border-color); margin:10px 0;"><p style="font-size:0.85rem;">Portfolio Value: <strong>{cust_data['aum']}</strong></p><p style="font-size:0.85rem;">Assigned RM: <strong>RM A (Anand Sharma)</strong></p><p style="font-size:0.85rem;">Branch: <strong>North Branch</strong></p><p style="font-size:0.85rem;">Risk Score: <span class="badge-tag badge-critical">{cust_data['score']}</span></p><p style="font-size:0.85rem;">Probability of Default: <strong style="color:#ef4444;">{cust_data['pd']}</strong></p></div>""", unsafe_allow_html=True)

    with c_col2:
        st.markdown('<div class="visual-box"><div class="visual-hdr-title">AI Recommended Next Best Actions</div>', unsafe_allow_html=True)
        st.success("✅ **Action 1:** Schedule urgent risk mitigation call regarding 89% credit default probability.")
        st.info("💡 **Action 2:** Offer portfolio rebalancing to shift 15% debt into Sovereign Gold Bonds.")
        st.warning("⚠️ **Action 3:** Review loan renewal terms due in 14 days.")

elif nav_option == "⚡ Big Data Stream":
    st.markdown("## ⚡ Kafka & Spark Real-Time Big Data Ingestion Stream")
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.metric("Events Ingested", "4,892,040", delta="+1,420 / sec")
    with p2: st.metric("Ingestion Velocity", "1,420 req/s", delta="Healthy")
    with p3: st.metric("Sub-50ms Latency", "14 ms", delta="-2 ms SLA")
    with p4: st.metric("Schema Validation", "99.8%", delta="Zero Anomalies")

    st.markdown("""<div class="visual-box" style="background:#030712; font-family:'JetBrains Mono', monospace; font-size:0.82rem; color:#4ade80; height:320px; overflow-y:auto;"><div>[LOG STREAMING ACTIVE] Kafka topic 'market.stock_ticks' - TICK: HDFCBANK price=₹1640.50 (+1.2%) vol=4,200</div><div>[LOG STREAMING ACTIVE] Kafka topic 'customer.transactions' - TX_EVENT: CUST-104 deposited ₹2,50,000 via UPI</div><div>[LOG STREAMING ACTIVE] Kafka topic 'portfolio.balance_updates' - AUM_SYNC: RM A portfolio re-indexed (+₹1.4M delta)</div><div style="color:#f87171; font-weight:700;">[ALERT TRIGGERED] Kafka topic 'credit.risk_signals' - CUST-101 PD increased +2.4% due to credit utilization spike</div><div>[LOG STREAMING ACTIVE] Kafka topic 'pipeline.telemetry' - Spark worker node #3 healthy (CPU 18%, Mem 42%)</div></div>""", unsafe_allow_html=True)

elif nav_option == "🧠 ML Optimizer":
    st.markdown("## 🧠 Markowitz Efficient Frontier Portfolio Optimization")
    ml_left, ml_right = st.columns([7, 5])
    with ml_left:
        risks = np.linspace(0.04, 0.22, 15)
        returns = 0.05 + 2.1 * np.power(risks - 0.03, 0.7)
        df_ef = pd.DataFrame({"Risk": risks * 100, "Return": returns * 100})
        fig_ef = px.scatter(df_ef, x="Risk", y="Return", title="Efficient Frontier Curve", color_discrete_sequence=["#38bdf8"])
        fig_ef.add_trace(go.Scatter(x=[11.2], y=[14.8], mode="markers", marker=dict(size=14, color="#f59e0b", symbol="star"), name="Optimal Portfolio"))
        fig_ef.update_layout(**PLOT_LAYOUT, height=350, xaxis_title="Portfolio Risk / Volatility (%)", yaxis_title="Expected Return (%)")
        st.plotly_chart(fig_ef, use_container_width=True)

    with ml_right:
        st.markdown("### Optimization Controls")
        risk_aversion = st.slider("Risk Aversion Factor", min_value=0.1, max_value=1.0, value=0.5, step=0.05)
        capital = st.number_input("Target Capital Investment (₹)", value=10000000, step=500000)
        st.success(f"Optimal Allocation calculated for ₹{capital:,.0f}:")
        st.write("• Home Loans: **35%** (₹3,500,000)")
        st.write("• Mutual Funds: **25%** (₹2,500,000)")
        st.write("• Equity Stocks: **15%** (₹1,500,000)")
        st.write("• Govt Bonds: **15%** (₹1,500,000)")
        st.write("• Insurance: **10%** (₹1,000,000)")

elif nav_option == "🤖 AI Copilot":
    st.markdown("## 🤖 AI Copilot Natural Language Intelligence Center")
    user_query = st.text_input("Ask AI Copilot about portfolio optimization, risk drivers, or revenue forecasts:", placeholder="e.g. Which RMs are top performers in mutual funds?")
    if user_query:
        st.info(f"**AI Copilot Analysis for:** '{user_query}'")
        st.write("• **RM A (Anand Sharma)** is leading with ₹9.8M revenue (North Branch).")
        st.write("• **RM B (Bhavna Patel)** is #2 with ₹7.6M revenue (South Branch).")
        st.write("• **Recommendation:** Cross-pollinate Mutual Fund cross-selling strategies to RM D and RM E.")
