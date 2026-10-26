import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM UI
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #080c14;
    --surface: #0d1422;
    --surface-2: #111b2d;
    --border: rgba(148, 163, 184, 0.13);
    --text: #f8fafc;
    --muted: #94a3b8;
    --subtle: #64748b;
    --blue: #60a5fa;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 0%,
            rgba(59,130,246,.10),
            transparent 26%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(139,92,246,.08),
            transparent 25%
        ),
        var(--bg);
}

html, body, [class*="css"] {
    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}


/* ===========================================================
   MAIN CONTAINER
   Extra top spacing keeps content clear of Streamlit toolbar.
   =========================================================== */

.block-container {
    max-width: 1500px;
    padding-top: 4.5rem;
    padding-bottom: 3rem;
}


/* ===========================================================
   SIDEBAR
   =========================================================== */

[data-testid="stSidebar"] {
    background: rgba(9,14,24,.98);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.sidebar-logo {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    flex: 0 0 42px;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,.20),
            rgba(139,92,246,.18)
        );

    border: 1px solid rgba(96,165,250,.22);

    color: #bfdbfe;
    font-size: 20px;
}

.sidebar-title {
    color: #f8fafc;
    font-size: .96rem;
    font-weight: 700;
    margin: 0;
}

.sidebar-subtitle {
    color: #64748b;
    font-size: .72rem;
    margin: 2px 0 0 0;
}

.sidebar-section {
    color: #64748b;

    font-size: .68rem;
    font-weight: 800;

    letter-spacing: .11em;
    text-transform: uppercase;

    margin: 1.7rem 0 .7rem;
}


/* ===========================================================
   ARCHITECTURE
   =========================================================== */

.architecture-card {
    padding: 14px;

    background: rgba(15,23,42,.50);

    border: 1px solid rgba(148,163,184,.10);
    border-radius: 13px;
}

.architecture-title {
    color: #cbd5e1;

    font-size: .76rem;
    font-weight: 700;

    margin-bottom: 11px;
}

.architecture-row {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 8px;

    margin-top: 9px;

    font-size: .72rem;
}

.architecture-label {
    color: #64748b;
}

.architecture-value {
    color: #cbd5e1;

    font-weight: 600;
    text-align: right;
}

.status-dot {
    width: 7px;
    height: 7px;

    display: inline-block;

    border-radius: 50%;

    background: #22c55e;

    margin-right: 5px;

    box-shadow:
        0 0 8px rgba(34,197,94,.45);
}


/* ===========================================================
   DEVELOPER CARD
   =========================================================== */

.developer-card {
    padding: 14px;

    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,.62),
            rgba(10,15,25,.60)
        );

    border: 1px solid rgba(148,163,184,.10);
    border-radius: 13px;
}

.developer-label {
    color: #64748b;

    font-size: .63rem;
    font-weight: 800;

    letter-spacing: .10em;
    text-transform: uppercase;

    margin-bottom: 7px;
}

.developer-name {
    color: #e2e8f0;

    font-size: .78rem;
    font-weight: 700;

    line-height: 1.45;
}

.developer-project {
    color: #64748b;

    font-size: .68rem;
    line-height: 1.5;

    margin-top: 4px;
}


/* ===========================================================
   HERO
   =========================================================== */

.hero {
    position: relative;
    overflow: hidden;

    padding: 32px;

    margin-bottom: 26px;

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,.95),
            rgba(10,15,25,.96)
        );

    border: 1px solid var(--border);
    border-radius: 20px;

    box-shadow:
        0 18px 50px rgba(0,0,0,.18);
}

.hero::after {
    content: "";

    position: absolute;

    width: 300px;
    height: 300px;

    border-radius: 50%;

    right: -100px;
    top: -170px;

    background: rgba(59,130,246,.15);

    filter: blur(16px);

    pointer-events: none;
}

.eyebrow {
    position: relative;
    z-index: 1;

    display: inline-flex;

    padding: 6px 10px;

    margin-bottom: 15px;

    border-radius: 999px;

    border: 1px solid rgba(96,165,250,.22);

    background: rgba(59,130,246,.08);

    color: #93c5fd;

    font-size: .70rem;
    font-weight: 800;

    letter-spacing: .06em;
    text-transform: uppercase;
}

.hero-title {
    position: relative;
    z-index: 1;

    color: #f8fafc;

    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 760;

    letter-spacing: -.045em;
    line-height: 1.05;

    margin: 0;
}

.hero-description {
    position: relative;
    z-index: 1;

    max-width: 790px;

    color: #94a3b8;

    font-size: .97rem;
    line-height: 1.7;

    margin: 14px 0 0;
}

.hero-tags {
    position: relative;
    z-index: 1;

    display: flex;
    flex-wrap: wrap;

    gap: 8px;

    margin-top: 19px;
}

.hero-tag {
    padding: 6px 10px;

    border-radius: 8px;

    color: #94a3b8;

    background: rgba(148,163,184,.06);

    border: 1px solid rgba(148,163,184,.10);

    font-size: .72rem;
}


/* ===========================================================
   SECTION
   =========================================================== */

.section-wrap {
    margin: .8rem 0 .8rem;
}

.section-kicker {
    color: #60a5fa;

    font-size: .68rem;
    font-weight: 800;

    letter-spacing: .11em;
    text-transform: uppercase;

    margin-bottom: 4px;
}

.section-title {
    color: #f1f5f9;

    font-size: 1.17rem;
    font-weight: 720;

    letter-spacing: -.02em;
}

.section-description {
    color: #64748b;

    font-size: .80rem;

    margin-top: 3px;
}


/* ===========================================================
   KPI
   =========================================================== */

.kpi-card {
    min-height: 145px;

    padding: 19px 20px;

    background:
        linear-gradient(
            145deg,
            rgba(18,27,44,.96),
            rgba(11,17,29,.96)
        );

    border: 1px solid rgba(148,163,184,.12);
    border-radius: 17px;

    box-shadow:
        0 12px 32px rgba(0,0,0,.14);

    transition:
        transform .18s ease,
        border-color .18s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);

    border-color:
        rgba(96,165,250,.30);
}

.kpi-top {
    display: flex;

    align-items: center;
    justify-content: space-between;

    gap: 10px;
}

.kpi-label {
    color: #64748b;

    font-size: .68rem;
    font-weight: 800;

    letter-spacing: .06em;
    text-transform: uppercase;
}

.kpi-icon {
    width: 36px;
    height: 36px;

    flex: 0 0 36px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background:
        rgba(59,130,246,.09);

    border:
        1px solid rgba(96,165,250,.14);

    color: #bfdbfe;

    font-size: 17px;
}

.kpi-value {
    color: #f8fafc;

    font-size: 1.55rem;
    font-weight: 750;

    letter-spacing: -.035em;

    margin-top: 17px;

    line-height: 1.1;

    overflow-wrap: anywhere;
}

.kpi-caption {
    color: #64748b;

    font-size: .72rem;

    margin-top: 7px;
}


/* ===========================================================
   STREAMLIT COMPONENTS
   =========================================================== */

div[data-testid="stPlotlyChart"] {
    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,.60),
            rgba(10,15,25,.65)
        );

    border:
        1px solid rgba(148,163,184,.10);

    border-radius: 16px;

    padding: 7px;
}

[data-testid="stDataFrame"] {
    border:
        1px solid rgba(148,163,184,.10);

    border-radius: 14px;

    overflow: hidden;
}

.stButton > button {
    width: 100%;

    border-radius: 10px;

    border:
        1px solid rgba(148,163,184,.16);

    background:
        rgba(30,41,59,.60);

    color: #cbd5e1;

    font-weight: 600;
}

.stButton > button:hover {
    border-color:
        rgba(96,165,250,.35);

    color: #f8fafc;
}

[data-testid="stExpander"] {
    border:
        1px solid rgba(148,163,184,.10);

    border-radius: 14px;

    background:
        rgba(15,23,42,.35);
}


/* ===========================================================
   FOOTER
   =========================================================== */

.footer {
    text-align: center;

    color: #475569;

    font-size: .72rem;
    line-height: 1.8;

    padding: 30px 0 7px;
}

.footer-name {
    color: #94a3b8;
    font-weight: 600;
}


/* ===========================================================
   MOBILE
   =========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-top: 4rem;
    }

    .hero {
        padding: 23px 21px;
    }

    .hero-title {
        font-size: 2rem;
    }

    .kpi-card {
        min-height: auto;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. DATABASE CONFIGURATION
# ============================================================

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SQLITE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "ecommerce.db",
)

NEON_DB_URL = os.getenv(
    "DATABASE_URL"
)

if not NEON_DB_URL:
    try:
        NEON_DB_URL = st.secrets[
            "DATABASE_URL"
        ]
    except (KeyError, FileNotFoundError):
        NEON_DB_URL = None


# ============================================================
# 4. HELPERS
# ============================================================

def format_currency(value):
    if pd.isna(value):
        return "Rs. 0"

    if value >= 10_000_000:
        return (
            f"Rs. "
            f"{value / 10_000_000:.2f} Cr"
        )

    if value >= 100_000:
        return (
            f"Rs. "
            f"{value / 100_000:.2f} L"
        )

    if value >= 1_000:
        return (
            f"Rs. "
            f"{value / 1_000:.1f}K"
        )

    return f"Rs. {value:,.0f}"


def format_number(value):
    if pd.isna(value):
        return "0"

    return f"{int(value):,}"


def section_header(
    kicker,
    title,
    description,
):
    html = (
        '<div class="section-wrap">'
        f'<div class="section-kicker">{kicker}</div>'
        f'<div class="section-title">{title}</div>'
        f'<div class="section-description">{description}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def metric_card(
    icon,
    label,
    value,
    caption,
):
    html = (
        '<div class="kpi-card">'
        '<div class="kpi-top">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-icon">{icon}</div>'
        '</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-caption">{caption}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def apply_chart_style(
    fig,
    height=360,
):
    fig.update_layout(
        height=height,

        margin=dict(
            l=25,
            r=25,
            t=60,
            b=25,
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#94a3b8",
            family="Inter, sans-serif",
            size=12,
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="#334155",
            font_color="#f8fafc",
        ),

        legend=dict(
            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="right",
            x=1,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,

        linecolor=
        "rgba(148,163,184,0.12)",

        tickfont=dict(
            color="#64748b"
        ),

        title_font=dict(
            color="#64748b"
        ),
    )

    fig.update_yaxes(
        gridcolor=
        "rgba(148,163,184,0.08)",

        zeroline=False,

        linecolor=
        "rgba(148,163,184,0.12)",

        tickfont=dict(
            color="#64748b"
        ),

        title_font=dict(
            color="#64748b"
        ),
    )

    return fig


# ============================================================
# 5. MULTI-DBMS DATA FEDERATION
# ============================================================

@st.cache_data(
    ttl=600,
    show_spinner=False,
)
def load_data():

    # --------------------------------------------------------
    # SQLITE — PRODUCT MASTER
    # --------------------------------------------------------

    if not os.path.exists(
        SQLITE_PATH
    ):
        raise FileNotFoundError(
            "Database SQLite tidak ditemukan: "
            f"{SQLITE_PATH}"
        )

    sqlite_connection = (
        sqlite3.connect(
            SQLITE_PATH
        )
    )

    try:
        df_products = (
            pd.read_sql_query(
                """
                SELECT
                    product_id,
                    category,
                    price,
                    discount
                FROM products
                """,
                sqlite_connection,
            )
        )

    finally:
        sqlite_connection.close()

    # --------------------------------------------------------
    # POSTGRESQL — TRANSACTIONS
    # --------------------------------------------------------

    if not NEON_DB_URL:
        raise ValueError(
            "DATABASE_URL tidak ditemukan. "
            "Tambahkan DATABASE_URL ke file .env "
            "untuk local development atau "
            "Streamlit Secrets untuk deployment."
        )

    postgres_url = (
        NEON_DB_URL.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1,
        )
    )

    engine = create_engine(
        postgres_url,
        pool_pre_ping=True,
    )

    try:
        df_transactions = (
            pd.read_sql_query(
                """
                SELECT
                    transaction_id,
                    user_id,
                    product_id,
                    final_price,
                    payment_method,
                    purchase_date
                FROM transactions
                """,
                engine,
            )
        )

    finally:
        engine.dispose()

    # --------------------------------------------------------
    # DATA FEDERATION
    # --------------------------------------------------------

    df_merged = pd.merge(
        df_transactions,
        df_products,

        on="product_id",

        how="inner",

        validate="many_to_one",
    )

    df_merged[
        "purchase_date"
    ] = pd.to_datetime(
        df_merged[
            "purchase_date"
        ],
        errors="coerce",
    )

    for column in [
        "final_price",
        "price",
        "discount",
    ]:
        df_merged[
            column
        ] = pd.to_numeric(
            df_merged[column],
            errors="coerce",
        )

    df_merged = (
        df_merged.dropna(
            subset=[
                "purchase_date",
                "final_price",
                "category",
                "payment_method",
            ]
        )
    )

    return df_merged


# ============================================================
# 6. LOAD DATA
# ============================================================

try:
    with st.spinner(
        "Menghubungkan Neon PostgreSQL "
        "dan SQLite..."
    ):
        df = load_data()

except Exception as error:
    st.error(
        "Gagal memuat data Multi-DBMS."
    )

    st.exception(
        error
    )

    st.stop()


if df.empty:
    st.warning(
        "Data hasil federasi kosong. "
        "Jalankan "
        "`python database/seed_data.py` "
        "terlebih dahulu."
    )

    st.stop()


# ============================================================
# 7. FILTER DEFAULTS / SESSION STATE
# ============================================================

categories = sorted(
    df["category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

payment_methods = sorted(
    df["payment_method"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

min_date = (
    df["purchase_date"]
    .min()
    .date()
)

max_date = (
    df["purchase_date"]
    .max()
    .date()
)


if (
    "category_filter"
    not in st.session_state
):
    st.session_state.category_filter = (
        "Semua Kategori"
    )


if (
    "payment_filter"
    not in st.session_state
):
    st.session_state.payment_filter = (
        "Semua Metode"
    )


if (
    "date_filter"
    not in st.session_state
):
    st.session_state.date_filter = (
        min_date,
        max_date,
    )


def reset_filters():

    st.session_state.category_filter = (
        "Semua Kategori"
    )

    st.session_state.payment_filter = (
        "Semua Metode"
    )

    st.session_state.date_filter = (
        min_date,
        max_date,
    )


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    brand_html = (
        '<div class="sidebar-brand">'

        '<div class="sidebar-logo">'
        '◈'
        '</div>'

        '<div>'

        '<p class="sidebar-title">'
        'Commerce Intelligence'
        '</p>'

        '<p class="sidebar-subtitle">'
        'Hybrid Multi-DBMS Analytics'
        '</p>'

        '</div>'

        '</div>'
    )

    st.markdown(
        brand_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">'
        'Filters'
        '</div>',
        unsafe_allow_html=True,
    )

    selected_category = (
        st.selectbox(
            "Kategori produk",
            [
                "Semua Kategori"
            ] + categories,
            key="category_filter",
        )
    )

    selected_payment = (
        st.selectbox(
            "Metode pembayaran",
            [
                "Semua Metode"
            ] + payment_methods,
            key="payment_filter",
        )
    )

    date_range = st.date_input(
        "Rentang tanggal",

        min_value=min_date,
        max_value=max_date,

        key="date_filter",
    )

    st.button(
        "↻ Reset filter",

        use_container_width=True,

        on_click=reset_filters,
    )

    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">'
        'Architecture'
        '</div>',
        unsafe_allow_html=True,
    )

    architecture_html = (
        '<div class="architecture-card">'

        '<div class="architecture-title">'
        'Data Infrastructure'
        '</div>'

        '<div class="architecture-row">'

        '<span class="architecture-label">'
        'Transactions'
        '</span>'

        '<span class="architecture-value">'
        '<span class="status-dot"></span>'
        'Neon PostgreSQL'
        '</span>'

        '</div>'

        '<div class="architecture-row">'

        '<span class="architecture-label">'
        'Product master'
        '</span>'

        '<span class="architecture-value">'
        '<span class="status-dot"></span>'
        'SQLite'
        '</span>'

        '</div>'

        '<div class="architecture-row">'

        '<span class="architecture-label">'
        'Federation'
        '</span>'

        '<span class="architecture-value">'
        'Pandas'
        '</span>'

        '</div>'

        '<div class="architecture-row">'

        '<span class="architecture-label">'
        'Visualization'
        '</span>'

        '<span class="architecture-value">'
        'Plotly'
        '</span>'

        '</div>'

        '</div>'
    )

    st.markdown(
        architecture_html,
        unsafe_allow_html=True,
    )

    st.caption(
        "Transaksi dan master produk "
        "dibaca dari dua DBMS berbeda "
        "lalu digabungkan berdasarkan "
        "product_id."
    )

    # --------------------------------------------------------
    # DEVELOPER IDENTITY
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">'
        'Project'
        '</div>',
        unsafe_allow_html=True,
    )

    developer_html = (
        '<div class="developer-card">'

        '<div class="developer-label">'
        'Developed by'
        '</div>'

        '<div class="developer-name">'
        'Adhitya Daffa Rhamadhani'
        '</div>'

        '<div class="developer-project">'
        'Academic Data Visualization Project'
        '</div>'

        '</div>'
    )

    st.markdown(
        developer_html,
        unsafe_allow_html=True,
    )


# ============================================================
# 9. APPLY FILTERS
# ============================================================

df_filtered = df.copy()


if (
    selected_category
    != "Semua Kategori"
):
    df_filtered = df_filtered[
        df_filtered["category"]
        == selected_category
    ]


if (
    selected_payment
    != "Semua Metode"
):
    df_filtered = df_filtered[
        df_filtered["payment_method"]
        == selected_payment
    ]


if (
    isinstance(
        date_range,
        (tuple, list),
    )
    and len(date_range) == 2
):
    start_date, end_date = (
        date_range
    )

    df_filtered = df_filtered[
        (
            df_filtered[
                "purchase_date"
            ].dt.date
            >= start_date
        )
        &
        (
            df_filtered[
                "purchase_date"
            ].dt.date
            <= end_date
        )
    ]


if df_filtered.empty:
    st.warning(
        "Tidak ada data untuk "
        "kombinasi filter yang dipilih."
    )

    st.stop()


# ============================================================
# 10. HERO
# ============================================================

hero_html = (
    '<div class="hero">'

    '<div class="eyebrow">'
    '◉ Multi-DBMS Analytics'
    '</div>'

    '<h1 class="hero-title">'
    'E-Commerce Intelligence Dashboard'
    '</h1>'

    '<p class="hero-description">'

    'Dashboard analitik interaktif yang '
    'mengintegrasikan data transaksi '
    'dari Neon PostgreSQL dengan master '
    'produk dari SQLite melalui data '
    'federation di tingkat aplikasi '
    'menggunakan Pandas.'

    '</p>'

    '<div class="hero-tags">'

    '<span class="hero-tag">'
    'PostgreSQL · Cloud'
    '</span>'

    '<span class="hero-tag">'
    'SQLite · Embedded'
    '</span>'

    '<span class="hero-tag">'
    'Pandas · Federation'
    '</span>'

    '<span class="hero-tag">'
    'Plotly · Interactive'
    '</span>'

    '</div>'

    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# ============================================================
# 11. KPI OVERVIEW
# ============================================================

section_header(
    "Overview",

    "Ringkasan performa",

    "Indikator utama berdasarkan "
    "filter yang sedang aktif.",
)


total_revenue = (
    df_filtered[
        "final_price"
    ].sum()
)

total_transactions = (
    df_filtered[
        "transaction_id"
    ].nunique()
)

unique_customers = (
    df_filtered[
        "user_id"
    ].nunique()
)

average_order_value = (
    df_filtered[
        "final_price"
    ].mean()
)


kpi_1, kpi_2, kpi_3, kpi_4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with kpi_1:
    metric_card(
        "↗",
        "Total Revenue",
        format_currency(
            total_revenue
        ),
        "Nilai penjualan setelah diskon",
    )


with kpi_2:
    metric_card(
        "◎",
        "Transactions",
        format_number(
            total_transactions
        ),
        "Jumlah transaksi",
    )


with kpi_3:
    metric_card(
        "♙",
        "Customers",
        format_number(
            unique_customers
        ),
        "Pelanggan unik",
    )


with kpi_4:
    metric_card(
        "◇",
        "Avg. Transaction",
        format_currency(
            average_order_value
        ),
        "Rata-rata nilai transaksi",
    )


# ============================================================
# 12. SALES PERFORMANCE
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

section_header(
    "Performance",

    "Tren & performa penjualan",

    "Perubahan pendapatan dari waktu "
    "ke waktu dan kontribusi kategori.",
)


left_chart, right_chart = (
    st.columns(
        [1.6, 1],
        gap="medium",
    )
)


# ------------------------------------------------------------
# REVENUE TREND
# ------------------------------------------------------------

with left_chart:

    daily_sales = (
        df_filtered

        .assign(
            date=
            df_filtered[
                "purchase_date"
            ].dt.date
        )

        .groupby(
            "date",
            as_index=False,
        )

        .agg(
            revenue=(
                "final_price",
                "sum",
            ),

            transactions=(
                "transaction_id",
                "nunique",
            ),
        )

        .sort_values(
            "date"
        )
    )

    fig_daily = px.area(
        daily_sales,

        x="date",
        y="revenue",

        labels={
            "date": "",
            "revenue":
            "Revenue (Rs.)",
        },
    )

    fig_daily.update_traces(
        line=dict(
            color="#60a5fa",
            width=2.5,
        ),

        fillcolor=
        "rgba(59,130,246,0.12)",

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: "
            "Rs. %{y:,.2f}"
            "<extra></extra>"
        ),
    )

    fig_daily = apply_chart_style(
        fig_daily,
        height=390,
    )

    fig_daily.update_layout(
        title=dict(
            text="Revenue Trend",

            font=dict(
                size=15,
                color="#e2e8f0",
            ),

            x=0.02,
        )
    )

    st.plotly_chart(
        fig_daily,

        use_container_width=True,

        config={
            "displayModeBar": False,
        },
    )


# ------------------------------------------------------------
# REVENUE BY CATEGORY
# ------------------------------------------------------------

with right_chart:

    category_sales = (
        df_filtered

        .groupby(
            "category",
            as_index=False,
        )

        .agg(
            revenue=(
                "final_price",
                "sum",
            )
        )

        .sort_values(
            "revenue",
            ascending=True,
        )
    )

    fig_category = px.bar(
        category_sales,

        x="revenue",
        y="category",

        orientation="h",

        labels={
            "revenue":
            "Revenue (Rs.)",

            "category": "",
        },
    )

    fig_category.update_traces(
        marker_color="#8b5cf6",

        marker_line_width=0,

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Revenue: "
            "Rs. %{x:,.2f}"
            "<extra></extra>"
        ),
    )

    fig_category = apply_chart_style(
        fig_category,
        height=390,
    )

    fig_category.update_layout(
        title=dict(
            text=
            "Revenue by Category",

            font=dict(
                size=15,
                color="#e2e8f0",
            ),

            x=0.02,
        )
    )

    st.plotly_chart(
        fig_category,

        use_container_width=True,

        config={
            "displayModeBar": False,
        },
    )


# ============================================================
# 13. PAYMENT & DISCOUNT
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

section_header(
    "Customer & Pricing",

    "Perilaku pembayaran & diskon",

    "Distribusi metode pembayaran "
    "dan hubungan diskon dengan "
    "nilai transaksi.",
)


# Slightly wider payment chart to avoid cramped content.
payment_col, discount_col = (
    st.columns(
        [0.9, 1.85],
        gap="medium",
    )
)


# ------------------------------------------------------------
# PAYMENT METHOD MIX
# ------------------------------------------------------------

with payment_col:

    payment_data = (
        df_filtered[
            "payment_method"
        ]

        .value_counts()

        .rename_axis(
            "payment_method"
        )

        .reset_index(
            name="transactions"
        )
    )

    fig_payment = px.pie(
        payment_data,

        names="payment_method",
        values="transactions",

        hole=0.68,

        color_discrete_sequence=[
            "#60a5fa",
            "#8b5cf6",
            "#22c55e",
            "#f59e0b",
            "#ec4899",
        ],
    )

    # Only percentage is shown on the donut.
    # Payment names are placed in the legend.
    fig_payment.update_traces(
        textposition="inside",

        textinfo="percent",

        textfont=dict(
            size=12,
            color="#f8fafc",
        ),

        hovertemplate=(
            "<b>%{label}</b><br>"
            "Transactions: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),

        marker=dict(
            line=dict(
                color="#0b111d",
                width=3,
            )
        ),
    )

    fig_payment = apply_chart_style(
        fig_payment,
        height=430,
    )

    fig_payment.update_layout(
        title=dict(
            text=
            "Payment Method Mix",

            font=dict(
                size=15,
                color="#e2e8f0",
            ),

            x=0.02,
        ),

        showlegend=True,

        legend=dict(
            orientation="h",

            yanchor="top",
            y=-0.04,

            xanchor="center",
            x=0.5,

            font=dict(
                size=10,
                color="#94a3b8",
            ),

            title=None,
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=75,
        ),
    )

    st.plotly_chart(
        fig_payment,

        use_container_width=True,

        config={
            "displayModeBar": False,
        },
    )


# ------------------------------------------------------------
# DISCOUNT VS FINAL PRICE
# ------------------------------------------------------------

with discount_col:

    fig_discount = px.scatter(
        df_filtered,

        x="discount",
        y="final_price",

        color="category",

        opacity=0.68,

        labels={
            "discount":
            "Discount (%)",

            "final_price":
            "Final Price (Rs.)",

            "category":
            "Category",
        },
    )

    fig_discount.update_traces(
        marker=dict(
            size=7,

            line=dict(
                width=0.3,

                color=
                "rgba(255,255,255,0.25)",
            ),
        )
    )

    fig_discount = apply_chart_style(
        fig_discount,
        height=430,
    )

    fig_discount.update_layout(
        title=dict(
            text=
            "Discount vs Final Price",

            font=dict(
                size=15,
                color="#e2e8f0",
            ),

            x=0.02,
        ),

        legend=dict(
            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="right",
            x=1,

            font=dict(
                size=10,
            ),
        ),

        margin=dict(
            l=30,
            r=25,
            t=80,
            b=35,
        ),
    )

    st.plotly_chart(
        fig_discount,

        use_container_width=True,

        config={
            "displayModeBar": False,
        },
    )


# ============================================================
# 14. ANALYTICAL INSIGHTS
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

section_header(
    "Insights",

    "Snapshot analitik",

    "Ringkasan cepat dari data "
    "yang sedang ditampilkan.",
)


category_revenue = (
    df_filtered

    .groupby(
        "category"
    )["final_price"]

    .sum()
)


best_category = (
    category_revenue.idxmax()
)


most_used_payment = (
    df_filtered[
        "payment_method"
    ]

    .mode()

    .iloc[0]
)


average_discount = (
    df_filtered[
        "discount"
    ].mean()
)


highest_transaction = (
    df_filtered[
        "final_price"
    ].max()
)


insight_1, insight_2, insight_3, insight_4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with insight_1:
    metric_card(
        "★",

        "Top Category",

        best_category,

        "Kategori dengan revenue tertinggi",
    )


with insight_2:
    metric_card(
        "◉",

        "Popular Payment",

        most_used_payment,

        "Metode pembayaran paling sering",
    )


with insight_3:
    metric_card(
        "%",

        "Avg. Discount",

        f"{average_discount:.1f}%",

        "Rata-rata diskon produk",
    )


with insight_4:
    metric_card(
        "↑",

        "Highest Transaction",

        format_currency(
            highest_transaction
        ),

        "Nilai transaksi terbesar",
    )


# ============================================================
# 15. FEDERATED DATASET
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

section_header(
    "Federated Dataset",

    "Data hasil integrasi Multi-DBMS",

    (
        "Preview transaksi Neon PostgreSQL "
        "yang telah digabungkan dengan "
        "master produk SQLite berdasarkan "
        "product_id."
    ),
)


display_columns = [
    "transaction_id",
    "user_id",
    "product_id",
    "category",
    "price",
    "discount",
    "final_price",
    "payment_method",
    "purchase_date",
]


table_df = (
    df_filtered[
        display_columns
    ]

    .sort_values(
        "purchase_date",
        ascending=False,
    )

    .head(100)

    .copy()
)


table_df[
    "purchase_date"
] = (
    table_df[
        "purchase_date"
    ]

    .dt.strftime(
        "%d %b %Y"
    )
)


st.dataframe(
    table_df,

    use_container_width=True,

    hide_index=True,

    height=390,

    column_config={

        "transaction_id":
        st.column_config.NumberColumn(
            "Transaction ID",
            format="%d",
        ),

        "user_id":
        "User ID",

        "product_id":
        "Product ID",

        "category":
        "Category",

        "price":
        st.column_config.NumberColumn(
            "Original Price",
            format="Rs. %.2f",
        ),

        "discount":
        st.column_config.NumberColumn(
            "Discount",
            format="%.1f%%",
        ),

        "final_price":
        st.column_config.NumberColumn(
            "Final Price",
            format="Rs. %.2f",
        ),

        "payment_method":
        "Payment Method",

        "purchase_date":
        "Purchase Date",
    },
)


# ============================================================
# 16. DATA PIPELINE
# ============================================================

with st.expander(
    "ⓘ Bagaimana data pada dashboard ini diproses?"
):

    st.markdown(
        """
**1. Neon PostgreSQL (Cloud)**  
Menyimpan data transaksi yang terdiri dari pengguna, produk,
nilai transaksi, metode pembayaran, dan tanggal pembelian.

**2. SQLite (Local Embedded)**  
Menyimpan master produk yang berisi kategori produk,
harga asli, dan persentase diskon.

**3. Data Federation dengan Pandas**  
Data dari PostgreSQL dan SQLite dibaca secara terpisah.
Keduanya kemudian digabungkan pada tingkat aplikasi
berdasarkan `product_id`.

**4. Analisis dan Visualisasi**  
Data hasil federasi dianalisis menggunakan Pandas dan
ditampilkan melalui Streamlit serta visualisasi interaktif
Plotly.
        """
    )


# ============================================================
# 17. FOOTER
# ============================================================

footer_html = (
    '<div class="footer">'

    'E-Commerce Hybrid Multi-DBMS Analytics'

    '&nbsp;·&nbsp;'

    'Neon PostgreSQL + SQLite + Pandas + Streamlit'

    '<br>'

    '<span class="footer-name">'
    'Developed by Adhitya Daffa Rhamadhani'
    '</span>'

    '&nbsp;·&nbsp;'

    '2026'

    '</div>'
)


st.markdown(
    footer_html,
    unsafe_allow_html=True,
)