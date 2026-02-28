import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="Portal Data Sekolah — NPSN",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# STYLE — Government Dashboard Aesthetic
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Noto+Serif:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #EEF1F7;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOP STRIPE (bendera merah-putih) ── */
.gov-stripe {
    height: 5px;
    background: linear-gradient(90deg, #CC0001 50%, #ffffff 50%);
    width: 100%;
}

/* ── HEADER BAR ── */
.gov-header {
    background: #0D2B5E;
    padding: 14px 40px;
    display: flex;
    align-items: center;
    gap: 18px;
    border-bottom: 3px solid #F0A500;
}

.gov-header-logo {
    width: 52px;
    height: 52px;
    background: #F0A500;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}

.gov-header-title {
    color: white;
}

.gov-header-title h1 {
    margin: 0;
    font-family: 'Noto Serif', serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: #ffffff;
    line-height: 1.2;
}

.gov-header-title p {
    margin: 2px 0 0 0;
    font-size: 11px;
    color: #94b4e0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.gov-header-right {
    margin-left: auto;
    text-align: right;
}

.gov-header-right .gov-datetime {
    color: #94b4e0;
    font-size: 12px;
}

.gov-header-right .gov-badge {
    display: inline-block;
    background: #F0A500;
    color: #0D2B5E;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 4px;
}

/* ── MAIN CONTENT ── */
.gov-main {
    padding: 28px 40px;
}

/* ── SECTION LABEL ── */
.gov-section-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #0D2B5E;
    border-left: 3px solid #F0A500;
    padding-left: 10px;
    margin-bottom: 14px;
}

/* ── STAT CARDS ── */
.stat-row {
    display: flex;
    gap: 16px;
    margin-bottom: 28px;
}

.stat-card {
    flex: 1;
    background: white;
    border-radius: 8px;
    padding: 20px 22px;
    border-top: 3px solid #0D2B5E;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
}

.stat-card::after {
    content: '';
    position: absolute;
    bottom: -12px;
    right: -12px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #EEF1F7;
}

.stat-card.accent { border-top-color: #F0A500; }
.stat-card.accent2 { border-top-color: #1A6BB5; }

.stat-card .stat-icon {
    font-size: 20px;
    margin-bottom: 8px;
    display: block;
}

.stat-card .stat-value {
    font-family: 'Noto Serif', serif;
    font-size: 32px;
    font-weight: 700;
    color: #0D2B5E;
    line-height: 1;
    margin-bottom: 4px;
}

.stat-card .stat-label {
    font-size: 11px;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── INPUT AREA ── */
.gov-input-panel {
    background: white;
    border-radius: 8px;
    padding: 22px 24px;
    margin-bottom: 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border-left: 4px solid #0D2B5E;
}

/* ── STATUS BAR ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #F0F4FF;
    border: 1px solid #C7D6F5;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    color: #1e3a6e;
    margin-bottom: 20px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── RESULT SECTION ── */
.result-header {
    background: #0D2B5E;
    color: white;
    padding: 12px 18px;
    border-radius: 8px 8px 0 0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
}

.result-body {
    background: white;
    border-radius: 0 0 8px 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    overflow: hidden;
}

.result-meta {
    padding: 10px 18px;
    background: #F8FAFF;
    border-bottom: 1px solid #E5E9F5;
    font-size: 11px;
    color: #6B7280;
    display: flex;
    gap: 20px;
}

.result-meta span { font-weight: 600; color: #0D2B5E; }

/* ── TABLE OVERRIDES ── */
.stDataFrame, .stTable {
    border: none !important;
}

table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

thead th {
    background: #F0F4FF !important;
    color: #0D2B5E !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    padding: 10px 12px !important;
    border-bottom: 2px solid #C7D6F5 !important;
    white-space: nowrap !important;
}

tbody td {
    padding: 9px 12px !important;
    border-bottom: 1px solid #F0F2F8 !important;
    color: #374151 !important;
    white-space: normal !important;
    word-break: break-word !important;
}

tbody tr:hover td { background: #F8FAFF !important; }

/* ── NOT FOUND ── */
.not-found-box {
    background: white;
    border-radius: 8px;
    border-left: 4px solid #EF4444;
    padding: 18px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.not-found-box .nf-icon { font-size: 28px; }
.not-found-box h4 { margin: 0 0 3px; color: #991B1B; font-size: 14px; }
.not-found-box p { margin: 0; font-size: 12px; color: #6B7280; }

/* ── SUCCESS TOAST ── */
.toast-success {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #0D2B5E;
    color: white;
    padding: 14px 20px;
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    font-size: 13px;
    font-weight: 600;
    z-index: 9999;
    border-left: 4px solid #F0A500;
    animation: slideIn 0.35s ease, fadeOut 0.4s ease 4s forwards;
    max-width: 280px;
}

@keyframes slideIn {
    from { transform: translateX(110%); opacity: 0; }
    to   { transform: translateX(0);   opacity: 1; }
}
@keyframes fadeOut {
    to { opacity: 0; transform: translateX(110%); }
}

/* ── FOOTER ── */
.gov-footer {
    background: #0D2B5E;
    color: #94b4e0;
    text-align: center;
    padding: 12px;
    font-size: 11px;
    margin-top: 40px;
    letter-spacing: 0.5px;
}

/* ── AUTO-REFRESH BAR ── */
.refresh-bar-wrap {
    height: 3px;
    background: #E5E9F5;
    border-radius: 99px;
    overflow: hidden;
    margin-bottom: 4px;
}
.refresh-bar {
    height: 100%;
    background: linear-gradient(90deg, #0D2B5E, #1A6BB5);
    border-radius: 99px;
    animation: shrink 300s linear forwards;
}
@keyframes shrink {
    from { width: 100%; }
    to   { width: 0%; }
}

/* ── STREAMLIT WIDGET STYLING ── */
.stTextInput input {
    border: 1px solid #C7D6F5 !important;
    border-radius: 6px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    background: #FAFBFF !important;
    color: #0D2B5E !important;
}
.stTextInput input:focus {
    border-color: #0D2B5E !important;
    box-shadow: 0 0 0 3px rgba(13,43,94,0.12) !important;
}

.stButton button {
    background: #0D2B5E !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 22px !important;
    transition: background 0.2s !important;
}
.stButton button:hover {
    background: #1A6BB5 !important;
}

.stForm { border: none !important; background: transparent !important; }
[data-testid="stForm"] { border: none !important; box-shadow: none !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================
# SESSION INIT
# =========================================
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = str(uuid.uuid4())
if "active_sheet_url" not in st.session_state:
    st.session_state.active_sheet_url = None
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# =========================================
# HEADER
# =========================================
st.markdown('<div class="gov-stripe"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="gov-header">
    <div class="gov-header-logo">🏛️</div>
    <div class="gov-header-title">
        <h1>Portal Data Instalasi Sekolah</h1>
        <p>Sistem Pencarian Berbasis NPSN &nbsp;·&nbsp; Data Terintegrasi</p>
    </div>
    <div class="gov-header-right">
        <div class="gov-datetime">{datetime.now().strftime("%A, %d %B %Y &nbsp;|&nbsp; %H:%M WIB")}</div>
        <div class="gov-badge">🔒 Sistem Internal</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gov-main">', unsafe_allow_html=True)

# =========================================
# FORM LOAD DATA
# =========================================
st.markdown('<div class="gov-section-label">Sumber Data</div>', unsafe_allow_html=True)
st.markdown('<div class="gov-input-panel">', unsafe_allow_html=True)

with st.form("sheet_form"):
    col_url, col_btn = st.columns([5, 1])
    with col_url:
        sheet_url_input = st.text_input(
            "URL Google Spreadsheet",
            placeholder="https://docs.google.com/spreadsheets/d/...",
            label_visibility="collapsed"
        )
    with col_btn:
        load_button = st.form_submit_button("↺  Muat Data")

st.markdown('</div>', unsafe_allow_html=True)

if load_button and sheet_url_input:
    st.session_state.refresh_token = str(uuid.uuid4())
    st.session_state.active_sheet_url = sheet_url_input
    st.session_state.last_refresh = datetime.now()

# =========================================
# URL BUILDER
# =========================================
def build_clean_export_url(url):
    if "docs.google.com" not in url:
        return url
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    except:
        return url

# =========================================
# CACHE TTL 5 MENIT
# =========================================
@st.cache_data(ttl=300)
def load_all_sheets(clean_url, refresh_token):
    excel = pd.ExcelFile(clean_url)
    semua_data = []

    def auto_read(sheet_name):
        raw = pd.read_excel(excel, sheet_name=sheet_name, header=None)
        header_row = None
        for i in range(min(15, len(raw))):
            row_values = raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row = i
                break
        if header_row is None:
            return None
        df = raw.iloc[header_row + 1:].copy()
        df.columns = (
            raw.iloc[header_row]
            .astype(str)
            .str.lower()
            .str.strip()
            .str.replace(" ", "_")
        )
        for c in df.columns:
            if "npsn" in c:
                df = df.rename(columns={c: "npsn"})
                break
        if "npsn" not in df.columns:
            return None
        df["source_sheet"] = sheet_name
        return df.reset_index(drop=True)

    for sheet in excel.sheet_names:
        hasil = auto_read(sheet)
        if hasil is not None:
            semua_data.append(hasil)

    if semua_data:
        return pd.concat(semua_data, ignore_index=True)
    return pd.DataFrame()

# =========================================
# LOAD & DISPLAY DATA
# =========================================
if st.session_state.active_sheet_url:

    clean_url = build_clean_export_url(st.session_state.active_sheet_url)

    try:
        data = load_all_sheets(clean_url, st.session_state.refresh_token)

        # ── Status bar ──
        elapsed = int((datetime.now() - st.session_state.last_refresh).total_seconds())
        next_refresh = max(0, 300 - elapsed)
        m, s = divmod(next_refresh, 60)
        st.markdown(f"""
        <div class="status-bar">
            <div class="status-dot"></div>
            <div>
                <div class="refresh-bar-wrap"><div class="refresh-bar"></div></div>
                Data aktif · Sinkronisasi terakhir: <strong>{st.session_state.last_refresh.strftime("%H:%M:%S")}</strong>
                &nbsp;·&nbsp; Auto-refresh berikutnya: <strong>{m}m {s}s</strong>
                &nbsp;·&nbsp; {len(data):,} baris dimuat dari {data['source_sheet'].nunique()} sheet
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Stat cards ──
        total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()

        st.markdown('<div class="stat-row">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <span class="stat-icon">📋</span>
                <div class="stat-value">{len(data):,}</div>
                <div class="stat-label">Total Baris Data</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card accent">
                <span class="stat-icon">🏫</span>
                <div class="stat-value">{total_sekolah:,}</div>
                <div class="stat-label">Total Sekolah</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card accent2">
                <span class="stat-icon">📑</span>
                <div class="stat-value">{data["source_sheet"].nunique()}</div>
                <div class="stat-label">Total Sheet Aktif</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Search ──
        st.markdown('<div class="gov-section-label">Pencarian Data</div>', unsafe_allow_html=True)
        st.markdown('<div class="gov-input-panel">', unsafe_allow_html=True)
        npsn_input = st.text_input(
            "Masukkan NPSN",
            placeholder="Contoh: 20123456",
            key="npsn_box",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if npsn_input:
            base_npsn = str(npsn_input).strip().split("_")[0]
            hasil = data[
                data["npsn"].astype(str).str.strip().str.startswith(base_npsn)
            ]

            if len(hasil) > 0:
                st.markdown(f"""
                <div class="toast-success">
                    ✔ NPSN {base_npsn} ditemukan<br>
                    <span style="font-weight:400;font-size:11px">{len(hasil)} instalasi tercatat</span>
                </div>
                """, unsafe_allow_html=True)

                hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

                st.markdown('<div class="gov-section-label">Hasil Pencarian</div>', unsafe_allow_html=True)

                for grp, df_grp in hasil.groupby("group"):
                    sheets_used = df_grp["source_sheet"].unique()
                    df_display = df_grp.drop(columns=["group"])

                    st.markdown(f"""
                    <div class="result-header">
                        🏫 NPSN {grp}
                    </div>
                    <div class="result-body">
                        <div class="result-meta">
                            Instalasi ditemukan: <span>{len(df_grp)}</span>
                            &nbsp;&nbsp;·&nbsp;&nbsp;
                            Sheet sumber: <span>{" · ".join(sheets_used)}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.table(df_display)
                    st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="not-found-box">
                    <div class="nf-icon">🔍</div>
                    <div>
                        <h4>Data Tidak Ditemukan</h4>
                        <p>NPSN <strong>{base_npsn}</strong> tidak terdapat dalam database. Pastikan NPSN yang dimasukkan sudah benar.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Gagal memuat data: {e}")

    # ── Auto-refresh setiap 5 menit ──
    time.sleep(300)
    st.session_state.refresh_token = str(uuid.uuid4())
    st.session_state.last_refresh = datetime.now()
    st.rerun()

else:
    st.info("Masukkan URL Google Spreadsheet di atas untuk memulai.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div class="gov-footer">
    Portal Data Instalasi Sekolah &nbsp;·&nbsp; Sistem Informasi Terintegrasi &nbsp;·&nbsp;
    Seluruh data bersifat rahasia dan hanya untuk penggunaan internal
</div>
""", unsafe_allow_html=True)
