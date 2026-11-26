import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="RetailIQ | Intelligence Platform",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# BOOT SPLASH (shows once per session, auto-dismisses)
# =====================================================

if "booted" not in st.session_state:

    st.session_state["booted"] = True

    st.markdown("""
    <style>
    @keyframes riqSplashOut {
        to { opacity: 0; visibility: hidden; }
    }
    @keyframes riqRing {
        0%   { transform: scale(.6); opacity: .9; }
        100% { transform: scale(1.8); opacity: 0; }
    }
    @keyframes riqPulse {
        0%, 100% { transform: scale(1); }
        50%      { transform: scale(1.06); }
    }
    @keyframes riqBarFill {
        0%   { width: 0%; }
        55%  { width: 68%; }
        100% { width: 100%; }
    }
    @keyframes riqStep {
        0%, 28%   { opacity: 1; }
        33%, 100% { opacity: 0; }
    }
    #riq-splash {
        position: fixed; inset: 0; z-index: 9999;
        background: #0B1220;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-family: 'Inter', sans-serif;
        animation: riqSplashOut .5s ease 2.6s forwards;
    }
    #riq-splash .rings { position: relative; width: 110px; height: 110px; margin-bottom: 34px; }
    #riq-splash .ring {
        position: absolute; inset: 0; border-radius: 26px;
        border: 2px solid #2563EB;
        animation: riqRing 1.6s cubic-bezier(.2,.6,.4,1) infinite;
    }
    #riq-splash .ring:nth-child(2) { animation-delay: .55s; border-color: #8B5CF6; }
    #riq-splash .mark {
        position: absolute; inset: 0; margin: auto;
        width: 74px; height: 74px; border-radius: 20px;
        background: linear-gradient(135deg, #2563EB, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        color: #fff; font-size: 34px; font-weight: 800;
        animation: riqPulse 1.6s ease-in-out infinite;
        box-shadow: 0 0 60px rgba(99,102,241,.5);
    }
    #riq-splash .word {
        color: #F8FAFC; font-size: 26px; font-weight: 800; letter-spacing: .01em;
    }
    #riq-splash .word span { color: #2563EB; }
    #riq-splash .tag {
        color: #64748B; font-size: 11px; letter-spacing: .3em; margin-top: 6px;
    }
    #riq-splash .bar {
        width: 220px; height: 3px; border-radius: 99px;
        background: rgba(148,163,184,.18); margin-top: 34px; overflow: hidden;
    }
    #riq-splash .bar i {
        display: block; height: 100%; border-radius: 99px;
        background: linear-gradient(90deg, #2563EB, #8B5CF6);
        animation: riqBarFill 2.2s cubic-bezier(.4,.1,.3,1) forwards;
    }
    #riq-splash .steps { position: relative; height: 18px; margin-top: 16px; width: 240px; }
    #riq-splash .steps span {
        position: absolute; inset: 0; text-align: center;
        color: #94A3B8; font-size: 12px;
        animation: riqStep 2.4s linear forwards; opacity: 0;
    }
    #riq-splash .steps span:nth-child(1) { animation-delay: 0s; }
    #riq-splash .steps span:nth-child(2) { animation-delay: .8s; }
    #riq-splash .steps span:nth-child(3) { animation-delay: 1.6s; }
    </style>

    <div id="riq-splash">
        <div class="rings">
            <div class="ring"></div>
            <div class="ring"></div>
            <div class="mark">R</div>
        </div>
        <div class="word">Retail<span>IQ</span></div>
        <div class="tag">INTELLIGENCE PLATFORM</div>
        <div class="bar"><i></i></div>
        <div class="steps">
            <span>Loading datasets…</span>
            <span>Warming up engines…</span>
            <span>Rendering insights…</span>
        </div>
    </div>

    <script>
    setTimeout(function() {
        var s = document.getElementById('riq-splash');
        if (s) { s.style.transition = 'opacity .45s ease'; s.style.opacity = '0';
                 setTimeout(function(){ s.remove(); }, 500); }
    }, 3100);
    </script>
    """, unsafe_allow_html=True)

# =====================================================
# DESIGN SYSTEM
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --riq-bg: #F6F7FA;
    --riq-surface: #FFFFFF;
    --riq-border: #E9EDF2;
    --riq-text: #0F172A;
    --riq-text-2: #475569;
    --riq-text-3: #94A3B8;
    --riq-accent: #2563EB;
    --riq-accent-2: #8B5CF6;
    --riq-green: #059669;
    --riq-red: #DC2626;
    --riq-sidebar: #0B1220;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--riq-bg);
}

/* subtle ambient mesh in the background */
.stApp::before {
    content: "";
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(600px 300px at 85% -5%, rgba(37,99,235,.05), transparent 60%),
        radial-gradient(500px 280px at 10% 110%, rgba(139,92,246,.05), transparent 60%);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1440px;
    position: relative; z-index: 1;
}

/* ---------- Page fade-in + staggered reveal ---------- */

@keyframes riqFadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.block-container > div {
    animation: riqFadeUp .45s ease both;
}

[data-testid="stMetric"], .info-card {
    animation: riqFadeUp .5s ease both;
}

[data-testid="stMetric"]:nth-of-type(2) { animation-delay: .06s; }
[data-testid="stMetric"]:nth-of-type(3) { animation-delay: .12s; }
[data-testid="stMetric"]:nth-of-type(4) { animation-delay: .18s; }

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"] {
    background: var(--riq-sidebar);
    border-right: none;
}

[data-testid="stSidebar"] * {
    color: #CBD5E1;
}

[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 9px 12px;
    border-radius: 9px;
    font-weight: 500;
    font-size: 14px;
    transition: background .18s ease, color .18s ease, box-shadow .18s ease;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(148,163,184,.12);
    color: #F1F5F9;
}

[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(90deg, #2563EB, #4F46E5);
    color: #FFFFFF;
    box-shadow: 0 4px 16px rgba(79,70,229,.35);
}

/* ---------- Metric cards ---------- */

[data-testid="stMetric"] {
    background: var(--riq-surface);
    border: 1px solid var(--riq-border);
    padding: 18px 20px;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
    position: relative;
    overflow: hidden;
    transition: box-shadow .18s ease, transform .18s ease;
}

[data-testid="stMetric"]::after {
    content: "";
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #2563EB, #8B5CF6);
    opacity: 0;
    transition: opacity .18s ease;
}

[data-testid="stMetric"]:hover {
    box-shadow: 0 6px 20px rgba(15,23,42,.09);
    transform: translateY(-2px);
}

[data-testid="stMetric"]:hover::after { opacity: 1; }

[data-testid="stMetricLabel"] {
    color: var(--riq-text-3) !important;
    font-weight: 600;
    font-size: 11px !important;
    letter-spacing: .05em;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: var(--riq-text) !important;
    font-weight: 700;
    font-size: 26px !important;
    font-variant-numeric: tabular-nums;
}

/* ---------- Custom shimmer spinner ---------- */

[data-testid="stSpinner"] {
    background: var(--riq-surface);
    border: 1px solid var(--riq-border);
    border-radius: 12px;
    padding: 16px 22px;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
}

[data-testid="stSpinner"] > div {
    border: 3px solid #E9EDF2;
    border-top-color: #2563EB !important;
    border-radius: 50%;
    width: 22px; height: 22px;
    animation: riqSpin .7s linear infinite;
}

@keyframes riqSpin {
    to { transform: rotate(360deg); }
}

[data-testid="stSpinner"] p {
    color: var(--riq-text-2) !important;
    font-weight: 500;
}

/* ---------- Charts & tables ---------- */

div[data-testid="stPlotlyChart"] {
    background: var(--riq-surface);
    border: 1px solid var(--riq-border);
    border-radius: 12px;
    padding: 12px 8px 4px;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
    transition: box-shadow .18s ease;
}

div[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 6px 20px rgba(15,23,42,.07);
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--riq-border);
    border-radius: 12px;
    background: var(--riq-surface);
}

/* ---------- Buttons ---------- */

div.stButton > button {
    background: linear-gradient(90deg, #2563EB, #4F46E5);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 14px;
    background-size: 150% 100%;
    transition: background-position .25s ease, box-shadow .2s ease;
}

div.stButton > button:hover {
    background-position: 100% 0;
    color: white;
    box-shadow: 0 6px 18px rgba(79,70,229,.3);
}

div.stDownloadButton > button {
    background: var(--riq-surface);
    color: var(--riq-text);
    border: 1px solid var(--riq-border);
    border-radius: 9px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 14px;
    transition: background .15s ease, border-color .15s ease;
}

div.stDownloadButton > button:hover {
    background: #F1F5F9;
    color: var(--riq-text);
    border-color: #D8DFE8;
}

/* ---------- Page header ---------- */

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 4px 2px 18px;
    border-bottom: 1px solid var(--riq-border);
    margin-bottom: 22px;
}

.page-header h1 {
    color: var(--riq-text);
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
}

.page-header p {
    color: var(--riq-text-3);
    font-size: 14px;
    margin: 4px 0 0;
}

.page-header .stamp {
    text-align: right;
    color: var(--riq-text-3);
    font-size: 12px;
    line-height: 1.5;
}

/* ---------- Section titles ---------- */

.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--riq-text);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin: 30px 0 14px;
}

.section-title::before {
    content: "";
    width: 3px; height: 16px; border-radius: 2px;
    background: linear-gradient(180deg, #2563EB, #8B5CF6);
}

/* ---------- Info cards ---------- */

.info-card {
    background: var(--riq-surface);
    border: 1px solid var(--riq-border);
    padding: 18px 20px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
    transition: box-shadow .18s ease, transform .18s ease;
}

.info-card:hover {
    box-shadow: 0 6px 20px rgba(15,23,42,.08);
    transform: translateY(-2px);
}

.info-card .label {
    color: var(--riq-text-3);
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: .05em;
    margin-bottom: 6px;
}

.info-card h2 {
    color: var(--riq-text);
    font-size: 22px; font-weight: 700;
    margin: 0 0 4px;
}

.info-card .hint { color: var(--riq-text-3); font-size: 12px; }

/* ---------- Delta pills ---------- */

.delta {
    display: inline-block;
    font-size: 12px; font-weight: 600;
    padding: 3px 9px; border-radius: 999px;
}

.delta.up   { color: var(--riq-green); background: #ECFDF5; }
.delta.down { color: var(--riq-red);   background: #FEF2F2; }

/* ---------- Live pulse dot ---------- */

@keyframes riqLive {
    0%   { box-shadow: 0 0 0 0 rgba(16,185,129,.5); }
    70%  { box-shadow: 0 0 0 7px rgba(16,185,129,0); }
    100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10B981;
    animation: riqLive 1.8s ease-out infinite;
}

/* ---------- Custom scrollbar ---------- */

::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: #D8DFE8;
    border-radius: 99px;
    border: 2px solid var(--riq-bg);
}
::-webkit-scrollbar-thumb:hover { background: #B7C2D0; }

/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: var(--riq-text-3);
    font-size: 12px;
    padding-top: 8px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# COUNT-UP ANIMATION FOR KPI VALUES
# =====================================================

st.markdown("""
<script>
(function() {
    function animateValue(el) {
        var raw = el.textContent.trim();
        var m = raw.match(/^([^0-9]*)([0-9,.]+)(.*)$/);
        if (!m) return;
        var prefix = m[1], suffix = m[3];
        var hasDecimals = m[2].indexOf('.') !== -1;
        var end = parseFloat(m[2].replace(/,/g, ''));
        if (isNaN(end)) return;
        var dur = 900, t0 = null;
        function fmt(n) {
            return n.toLocaleString('en-US',
                { minimumFractionDigits: hasDecimals ? 2 : 0,
                  maximumFractionDigits: hasDecimals ? 2 : 0 });
        }
        function step(ts) {
            if (!t0) t0 = ts;
            var p = Math.min((ts - t0) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = prefix + fmt(end * eased) + suffix;
            if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
    var obs = new MutationObserver(function() {
        document.querySelectorAll('[data-testid="stMetricValue"]')
            .forEach(function(el) {
                if (!el.dataset.riqCounted) {
                    el.dataset.riqCounted = "1";
                    animateValue(el);
                }
            });
    });
    obs.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)


# =====================================================
# DATA LOADING
# =====================================================

@st.cache_data
def load_data():

    daily = pd.read_csv("processed/daily_sales_baseline.csv")
    daily["Date"] = pd.to_datetime(daily["Date"])

    forecast = pd.read_csv("reports/next_30_days_forecast.csv")
    forecast["Date"] = pd.to_datetime(forecast["Date"])

    inventory = pd.read_csv("reports/inventory_optimization.csv")

    validation = pd.read_csv("reports/forecast_validation_results.csv")

    return daily, forecast, inventory, validation


with st.spinner("Loading intelligence data…"):
    try:
        daily, forecast, inventory, validation = load_data()
    except Exception as e:
        st.error(f"Unable to load project data: {e}")
        st.stop()


# =====================================================
# CHART THEME
# =====================================================

PALETTE = {
    "blue":   "#2563EB",
    "indigo": "#6366F1",
    "purple": "#8B5CF6",
    "green":  "#10B981",
    "amber":  "#F59E0B",
    "red":    "#EF4444",
    "gray":   "#94A3B8",
}


def style_chart(fig, height=360):

    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", color="#64748B", size=12),
        title=dict(font=dict(size=14, color="#0F172A", family="Inter")),
        margin=dict(l=10, r=10, t=48, b=20),
        hoverlabel=dict(bgcolor="#0B1220", font_color="white", font_family="Inter"),
        legend=dict(orientation="h", y=1.14, x=0, font=dict(size=12))
    )

    fig.update_xaxes(showgrid=False, linecolor="#E9EDF2",
                     ticks="outside", tickcolor="#CBD5E1")
    fig.update_yaxes(gridcolor="#F1F4F8", zeroline=False)

    return fig


def page_header(title, subtitle):

    stamp = datetime.now().strftime("%A, %d %b · %H:%M")

    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div class="stamp">
                RetailIQ v1.0<br>{stamp}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def delta(current, previous):
    if previous in (0, None) or pd.isna(previous):
        return ""
    pct = (current - previous) / previous * 100
    cls = "up" if pct >= 0 else "down"
    arrow = "▲" if pct >= 0 else "▼"
    return f'<span class="delta {cls}">{arrow} {abs(pct):.1f}%</span>'


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:6px 4px 14px;">
            <div style="width:34px;height:34px;border-radius:9px;
                        background:linear-gradient(135deg,#2563EB,#8B5CF6);
                        display:flex;align-items:center;justify-content:center;
                        color:white;font-weight:800;font-size:16px;font-family:Inter;
                        box-shadow:0 4px 14px rgba(99,102,241,.4);">R</div>
            <div>
                <div style="color:#F8FAFC;font-weight:700;font-size:17px;font-family:Inter;">RetailIQ</div>
                <div style="color:#64748B;font-size:10px;letter-spacing:.14em;font-family:Inter;">INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Overview", "Sales Analytics", "Sales Forecast",
         "Inventory Intelligence", "Model Performance"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div style="color:#64748B;font-size:10px;letter-spacing:.12em;'
        'padding:0 4px 8px;">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    for label in ["Analytics engine", "Forecasting engine", "Inventory engine"]:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;padding:4px;">'
            f'<span class="live-dot" style="animation:riqLive 1.8s ease-out infinite;"></span>'
            f'<span style="color:#CBD5E1;font-size:13px;">{label}</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.caption("RetailIQ v1.0 · Streamlit")


# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    page_header(
        "Business Overview",
        "Retail performance, demand signals and forecast intelligence at a glance."
    )

    total_revenue = daily["Revenue"].sum()
    total_transactions = daily["Transactions"].sum()
    total_items = daily["ItemsSold"].sum()
    avg_revenue = daily["Revenue"].mean()

    last30 = daily.tail(30)["Revenue"].sum()
    prev30 = daily.tail(60).head(30)["Revenue"].sum()
    rev_delta = delta(last30, prev30)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"£{total_revenue:,.0f}")
    c2.metric("Transactions", f"{total_transactions:,.0f}")
    c3.metric("Units Sold", f"{total_items:,.0f}")
    c4.metric("Average Daily Revenue", f"£{avg_revenue:,.0f}")

    if rev_delta:
        st.markdown(
            f'<div style="font-size:12px;color:#94A3B8;margin:-6px 0 8px;">'
            f'Last 30 days {rev_delta} vs previous 30 days</div>',
            unsafe_allow_html=True
        )

    section("Revenue Performance")

    fig = px.area(daily, x="Date", y="Revenue", title="Daily Revenue Trend")
    fig.update_traces(line_color=PALETTE["blue"],
                      fillcolor="rgba(37,99,235,0.10)", line_shape="spline")
    st.plotly_chart(style_chart(fig), use_container_width=True)

    left, right = st.columns(2)

    with left:
        monthly = (daily.set_index("Date")["Revenue"]
                   .resample("ME").sum().reset_index())
        fig = px.bar(monthly, x="Date", y="Revenue", title="Monthly Revenue")
        fig.update_traces(marker_color=PALETTE["blue"], marker_line_width=0, opacity=0.9)
        st.plotly_chart(style_chart(fig, 320), use_container_width=True)

    with right:
        weekday = daily.copy()
        weekday["Weekday"] = weekday["Date"].dt.day_name()
        weekday_summary = (weekday.groupby("Weekday")["Revenue"].mean()
                           .reindex(["Monday","Tuesday","Wednesday","Thursday",
                                     "Friday","Saturday","Sunday"]).reset_index())
        fig = px.bar(weekday_summary, x="Weekday", y="Revenue",
                     title="Average Revenue by Weekday")
        fig.update_traces(marker_color=[
            PALETTE["blue"] if d in ("Saturday","Sunday")
            else "rgba(148,163,184,0.55)"
            for d in weekday_summary["Weekday"]], marker_line_width=0)
        st.plotly_chart(style_chart(fig, 320), use_container_width=True)

    section("Business Snapshot")

    a, b, c = st.columns(3)
    best = validation.loc[validation["RMSE"].idxmin(), "Model"]

    with a:
        st.markdown(
            f'<div class="info-card"><div class="label">Products Analyzed</div>'
            f'<h2>{len(inventory):,}</h2>'
            f'<div class="hint">Product-level inventory analysis</div></div>',
            unsafe_allow_html=True)
    with b:
        st.markdown(
            f'<div class="info-card"><div class="label">Forecast Horizon</div>'
            f'<h2>{len(forecast)} Days</h2>'
            f'<div class="hint">Future sales projection</div></div>',
            unsafe_allow_html=True)
    with c:
        st.markdown(
            f'<div class="info-card"><div class="label">Best Validated Method</div>'
            f'<h2 style="font-size:19px;">{best}</h2>'
            f'<div class="hint">Lowest RMSE on the test period</div></div>',
            unsafe_allow_html=True)


# =====================================================
# SALES ANALYTICS
# =====================================================

elif page == "Sales Analytics":

    page_header(
        "Sales Analytics",
        "Historical revenue, transaction activity and sales patterns."
    )

    section("Filter Sales by Date")

    date_col1, date_col2 = st.columns(2)

    with date_col1:
        start = st.date_input(
            "Start Date",
            value=daily["Date"].min().date(),
            min_value=daily["Date"].min().date(),
            max_value=daily["Date"].max().date(),
            key="sales_start"
        )

    with date_col2:
        end = st.date_input(
            "End Date",
            value=daily["Date"].max().date(),
            min_value=daily["Date"].min().date(),
            max_value=daily["Date"].max().date(),
            key="sales_end"
        )

    if start > end:
        st.error("Start date must be before end date.")
        st.stop()

    filtered = daily[(daily["Date"] >= pd.Timestamp(start)) &
                     (daily["Date"] <= pd.Timestamp(end))]

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"£{filtered['Revenue'].sum():,.2f}")
    col2.metric("Transactions", f"{filtered['Transactions'].sum():,.0f}")
    col3.metric("Items Sold", f"{filtered['ItemsSold'].sum():,.0f}")

    section("Revenue Trend")

    fig = px.line(filtered, x="Date", y="Revenue", markers=True)
    fig.update_traces(line_color=PALETTE["blue"], line_shape="spline",
                      marker=dict(size=5, color=PALETTE["blue"]))
    st.plotly_chart(style_chart(fig), use_container_width=True)

    left, right = st.columns(2)

    with left:
        fig = px.bar(filtered, x="Date", y="Transactions", title="Daily Transactions")
        fig.update_traces(marker_color=PALETTE["purple"], marker_line_width=0)
        st.plotly_chart(style_chart(fig, 320), use_container_width=True)
    with right:
        fig = px.bar(filtered, x="Date", y="ItemsSold", title="Daily Units Sold")
        fig.update_traces(marker_color=PALETTE["green"], marker_line_width=0)
        st.plotly_chart(style_chart(fig, 320), use_container_width=True)

    section("Detailed Sales Records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Sales Data",
        filtered.to_csv(index=False).encode("utf-8"),
        "sales_analysis.csv", "text/csv")


# =====================================================
# SALES FORECAST
# =====================================================

elif page == "Sales Forecast":

    page_header(
        "Sales Forecast",
        "Upcoming 30-day sales projection based on historical weekday patterns."
    )

    total_forecast = forecast["Predicted_Revenue"].sum()
    avg_forecast = forecast["Predicted_Revenue"].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Projected Revenue", f"£{total_forecast:,.0f}")
    c2.metric("Daily Average", f"£{avg_forecast:,.0f}")
    c3.metric("Forecast Period", f"{len(forecast)} Days")

    section("Future Revenue Projection")

    fig = px.area(forecast, x="Date", y="Predicted_Revenue", markers=True)
    fig.update_traces(line_color=PALETTE["purple"],
                      fillcolor="rgba(139,92,246,0.10)", line_shape="spline",
                      marker=dict(size=5, color=PALETTE["purple"]))
    st.plotly_chart(style_chart(fig, 420), use_container_width=True)

    section("Forecast by Weekday")

    weekday_forecast = (forecast.groupby("Day")["Predicted_Revenue"]
                        .mean().reset_index())
    day_order = ["Monday","Tuesday","Wednesday","Thursday",
                 "Friday","Saturday","Sunday"]
    weekday_forecast["Day"] = pd.Categorical(
        weekday_forecast["Day"], categories=day_order, ordered=True)
    weekday_forecast = weekday_forecast.sort_values("Day")

    fig = px.bar(weekday_forecast, x="Day", y="Predicted_Revenue",
                 color="Predicted_Revenue", color_continuous_scale="Purples")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig, 330), use_container_width=True)

    section("Forecast Records")
    st.dataframe(forecast.style.format({"Predicted_Revenue": "£{:,.2f}"}),
                 use_container_width=True, hide_index=True)
    st.download_button(
        "Download Forecast",
        forecast.to_csv(index=False).encode("utf-8"),
        "sales_forecast.csv", "text/csv")

    st.info("Forecasts are estimates based on historical weekday medians. "
            "They are not guaranteed future sales.")


# =====================================================
# INVENTORY INTELLIGENCE
# =====================================================

elif page == "Inventory Intelligence":

    page_header(
        "Inventory Intelligence",
        "Product demand and data-driven replenishment estimates."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Products Analyzed", f"{len(inventory):,}")
    c2.metric("Total Units Sold", f"{inventory['Total_Units_Sold'].sum():,.0f}")
    c3.metric("Total Product Revenue", f"£{inventory['Total_Revenue'].sum():,.0f}")

    section("Top Revenue Generators")

    top = inventory.nlargest(10, "Total_Revenue").sort_values("Total_Revenue")
    fig = px.bar(top, x="Total_Revenue", y="Description", orientation="h",
                 color="Total_Revenue", color_continuous_scale="Blues")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig, 430), use_container_width=True)

    section("Product Search")

    search = st.text_input(
        "Search by product name or stock code",
        placeholder="Example: JUMBO BAG or 85123A")

    filtered = inventory.copy()
    if search:
        mask = (filtered["Description"].astype(str).str.contains(
                    search, case=False, na=False)
                | filtered["StockCode"].astype(str).str.contains(
                    search, case=False, na=False))
        filtered = filtered[mask]

    columns = ["StockCode", "Description", "Total_Units_Sold", "Total_Revenue",
               "Average_Daily_Demand", "Daily_Demand_Std", "Safety_Stock",
               "Reorder_Point", "Recommended_Reorder_Qty"]

    st.caption(f"{len(filtered):,} matching products")

    st.dataframe(
        filtered[columns].style.format({
            "Total_Revenue": "£{:,.2f}",
            "Average_Daily_Demand": "{:.2f}",
            "Daily_Demand_Std": "{:.2f}",
            "Safety_Stock": "{:.2f}",
            "Reorder_Point": "{:.2f}"}),
        use_container_width=True, hide_index=True)

    st.download_button(
        "Download Inventory Report",
        filtered[columns].to_csv(index=False).encode("utf-8"),
        "inventory_optimization.csv", "text/csv")

    st.warning("Reorder quantities are estimates based on historical demand "
               "and assumed lead/review periods. Actual stock on hand and "
               "supplier lead times are not available in the dataset.")


# =====================================================
# MODEL PERFORMANCE
# =====================================================

elif page == "Model Performance":

    page_header(
        "Model Performance",
        "Forecasting methods compared on a consistent historical test set."
    )

    best = validation.loc[validation["RMSE"].idxmin()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Best Validated Method", best["Model"])
    c2.metric("Lowest RMSE", f"£{best['RMSE']:,.2f}")
    c3.metric("Lowest MAE", f"£{validation['MAE'].min():,.2f}")

    section("Performance Comparison")

    metric = st.selectbox("Choose evaluation metric", ["MAE", "RMSE", "MAPE (%)"])

    fig = px.bar(validation, x="Model", y=metric, color="Model", text_auto=".2f",
                 color_discrete_sequence=[PALETTE["gray"], PALETTE["blue"],
                                          PALETTE["green"]])
    st.plotly_chart(style_chart(fig, 400), use_container_width=True)

    section("Evaluation Results")

    st.dataframe(
        validation.style.format({
            "MAE": "£{:,.2f}", "RMSE": "£{:,.2f}", "MAPE (%)": "{:.2f}%"}),
        use_container_width=True, hide_index=True)

    st.success(f"{best['Model']} achieved the lowest RMSE on the historical "
               "test dataset.")
    st.info("The Weekday Median method is a statistical benchmark, while "
            "Random Forest is a machine-learning model. Both are compared "
            "on the same test period.")


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <b>RetailIQ</b> · Retail Sales Forecasting &amp; Inventory Optimization<br>
        Built with Python · Pandas · Scikit-learn · Plotly · Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
