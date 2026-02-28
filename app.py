import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

# =========================================
# STYLE
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #0d1117;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #c9d1d9;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #161b22; }
::-webkit-scrollbar-thumb { background: #1e6fd6; border-radius: 3px; }

/* ---- HEADER ---- */
.header-wrap {
    display: flex;
    align-items: flex-end;
    gap: 18px;
    padding: 22px 28px;
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #1e6fd6;
    border-radius: 4px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.header-wrap::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 200px; height: 100%;
    background: linear-gradient(135deg, transparent 60%, rgba(30,111,214,0.07));
    pointer-events: none;
}

.header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    color: #f0f6fc;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.2;
}

.header-sub {
    font-size: 12px;
    color: #6e7681;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px;
    margin: 0;
    text-transform: uppercase;
}

.header-badge {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #1e6fd6;
    border: 1px solid #1e3a5f;
    padding: 5px 12px;
    border-radius: 2px;
    background: rgba(30,111,214,0.08);
    white-space: nowrap;
}

/* ---- STAT CARDS ---- */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-top: 2px solid #1e6fd6;
    padding: 18px 20px;
    border-radius: 4px;
    position: relative;
}

.stat-card.green { border-top-color: #238636; }
.stat-card.purple { border-top-color: #8b5cf6; }

.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6e7681;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 6px;
}

.stat-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 30px;
    font-weight: 600;
    color: #f0f6fc;
    line-height: 1;
}

.stat-desc {
    font-size: 12px;
    color: #484f58;
    margin-top: 4px;
}

/* ---- FORM / INPUT OVERRIDE ---- */
div[data-testid="stForm"] {
    background: #161b22;
    border: 1px solid #21262d;
    padding: 20px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.stTextInput > div > div > input,
.stTextInput > label + div > div > input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #1e6fd6 !important;
    box-shadow: 0 0 0 3px rgba(30,111,214,0.15) !important;
}

.stTextInput > label {
    color: #8b949e !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

/* ---- BUTTON ---- */
.stButton > button, .stFormSubmitButton > button {
    background: #1e6fd6 !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 8px 20px !important;
    transition: background 0.15s !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #2680f0 !important;
}

/* ---- DIVIDER ---- */
hr {
    border: none;
    border-top: 1px solid #21262d;
    margin: 20px 0;
}

/* ---- SYNC BAR ---- */
.sync-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #484f58;
    margin-bottom: 18px;
    padding: 8px 14px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 3px;
}

.sync-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #238636;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* ---- RESULT SECTION ---- */
.result-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 18px;
    background: #161b22;
    border: 1px solid #21262d;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #f0f6fc;
    margin-top: 18px;
}

.result-badge {
    font-size: 10px;
    background: rgba(30,111,214,0.15);
    color: #1e6fd6;
    border: 1px solid #1e3a5f;
    padding: 2px 8px;
    border-radius: 10px;
}

.result-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 0 0 4px 4px;
    padding: 0;
    margin-bottom: 20px;
    overflow: hidden;
}

/* ---- TABLE ---- */
.stTable, table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

thead tr {
    background: #0d1117 !important;
}

thead th {
    color: #6e7681 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #21262d !important;
    white-space: nowrap !important;
}

tbody tr {
    border-bottom: 1px solid #161b22 !important;
    transition: background 0.1s !important;
}

tbody tr:hover {
    background: rgba(30,111,214,0.05) !important;
}

tbody td {
    padding: 9px 14px !important;
    color: #c9d1d9 !important;
    white-space: normal !important;
    word-break: break-word !important;
    border: none !important;
}

/* ---- TOAST ---- */
.toast {
    position: fixed;
    top: 22px;
    right: 22px;
    background: #161b22;
    border: 1px solid #238636;
    border-left: 3px solid #238636;
    color: #f0f6fc;
    padding: 14px 20px;
    border-radius: 4px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    z-index: 9999;
    animation: toastIn 0.3s ease, toastOut 0.4s ease 4.5s forwards;
    min-width: 240px;
}

.toast-title {
    font-weight: 600;
    color: #3fb950;
    margin-bottom: 4px;
}

.toast-body { color: #8b949e; }

@keyframes toastIn {
    from { transform: translateX(120%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes toastOut {
    to { transform: translateX(120%); opacity: 0; }
}

/* ---- WARNING / INFO ---- */
.stWarning {
    background: #161b22 !important;
    border: 1px solid #4d2e00 !important;
    color: #d29922 !important;
    border-radius: 3px !important;
}

/* ---- REFRESH COUNTDOWN ---- */
.refresh-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #484f58;
    margin-bottom: 16px;
}

.refresh-prog {
    flex: 1;
    height: 2px;
    background: #21262d;
    border-radius: 1px;
    margin: 0 12px;
    overflow: hidden;
}

.refresh-fill {
    height: 100%;
    background: #1e6fd6;
    border-radius: 1px;
    transition: width 1s linear;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="header-wrap">
    <div>
        <p class="header-sub">// sistem informasi</p>
        <h1 class="header-title">Portal Data Sekolah</h1>
    </div>
    <span class="header-badge">NPSN LOOKUP v2.0</span>
</div>
""", unsafe_allow_html=True)

# =========================================
# SESSION INIT
# =========================================
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = str(uuid.uuid4())

if "active_sheet_url" not in st.session_state:
    st.session_state.active_sheet_url = None

if "last_refresh_time" not in st.session_state:
    st.session_state.last_refresh_time = time.time()

# =========================================
# FORM LOAD DATA
# =========================================
with st.form("sheet_form"):
    sheet_url_input = st.text_input("Link Google Spreadsheet")
    load_button = st.form_submit_button("▶  Load / Refresh Data")

if load_button and sheet_url_input:
    st.session_state.refresh_token = str(uuid.uuid4())
    st.session_state.active_sheet_url = sheet_url_input
    st.session_state.last_refresh_time = time.time()

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
        df.columns = (raw.iloc[header_row]
                      .astype(str)
                      .str.lower()
                      .str.strip()
                      .str.replace(" ", "_"))

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
# LOAD DATA + AUTO REFRESH
# =========================================
REFRESH_INTERVAL = 300  # 5 menit

if st.session_state.active_sheet_url:

    clean_url = build_clean_export_url(st.session_state.active_sheet_url)

    # --- Cek apakah sudah waktunya auto-refresh ---
    elapsed = time.time() - st.session_state.last_refresh_time
    if elapsed >= REFRESH_INTERVAL:
        st.session_state.refresh_token = str(uuid.uuid4())
        st.session_state.last_refresh_time = time.time()
        elapsed = 0

    data = load_all_sheets(clean_url, st.session_state.refresh_token)

    # --- Sync bar ---
    now_str = datetime.now().strftime("%H:%M:%S")
    sisa = max(0, int(REFRESH_INTERVAL - elapsed))
    menit = sisa // 60
    detik = sisa % 60
    pct = int((elapsed / REFRESH_INTERVAL) * 100)

    st.markdown(f"""
    <div class="sync-bar">
        <span class="sync-dot"></span>
        LIVE — Sinkronisasi terakhir: {now_str}
        &nbsp;|&nbsp;
        Refresh berikutnya: {menit:02d}:{detik:02d}
        &nbsp;|&nbsp;
        <span style="color:#1e6fd6">{pct}% cycle</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Stat Cards ---
    total_rows = len(data)
    total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
    total_sheets = data["source_sheet"].nunique()

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-label">Total Baris</div>
            <div class="stat-value">{total_rows:,}</div>
            <div class="stat-desc">semua sheet gabungan</div>
        </div>
        <div class="stat-card green">
            <div class="stat-label">Total Sekolah</div>
            <div class="stat-value">{total_sekolah:,}</div>
            <div class="stat-desc">unique NPSN terdeteksi</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-label">Sheet Aktif</div>
            <div class="stat-value">{total_sheets}</div>
            <div class="stat-desc">sheet memiliki kolom NPSN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # SEARCH
    # =========================================
    npsn_input = st.text_input("Cari NPSN", placeholder="Masukkan NPSN lalu tekan Enter...", key="npsn_box")

    if npsn_input:
        base_npsn = str(npsn_input).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil) > 0:
            st.markdown(f"""
            <div class="toast">
                <div class="toast-title">✓ NPSN Ditemukan</div>
                <div class="toast-body">NPSN {base_npsn} — {len(hasil)} instalasi</div>
            </div>
            """, unsafe_allow_html=True)

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):
                st.markdown(f"""
                <div class="result-header">
                    <span>🏫 NPSN {grp}</span>
                    <span class="result-badge">{len(df_grp)} instalasi</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.table(df_grp.drop(columns=["group"]))
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning(f"NPSN **{base_npsn}** tidak ditemukan dalam database.")

    # =========================================
    # AUTO RERUN setiap 30 detik untuk update countdown
    # =========================================
    time.sleep(30)
    st.rerun()
