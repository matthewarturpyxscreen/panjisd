import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="Portal Data Sekolah",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# STYLE
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #F7F8FA;
    font-family: 'DM Sans', sans-serif;
    color: #1C1C28;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOPBAR ── */
.topbar {
    background: #ffffff;
    border-bottom: 1px solid #E8EAF0;
    padding: 0 36px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 100;
}

.topbar-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #3B6FE8;
}

.topbar-title {
    font-size: 14px;
    font-weight: 600;
    color: #1C1C28;
    letter-spacing: -0.2px;
}

.topbar-sep {
    width: 1px;
    height: 16px;
    background: #E8EAF0;
}

.topbar-sub {
    font-size: 12px;
    color: #8B90A0;
}

.topbar-right {
    margin-left: auto;
    font-size: 12px;
    color: #8B90A0;
    font-family: 'DM Mono', monospace;
}

/* ── MAIN WRAPPER ── */
.main-wrap {
    padding: 28px 36px;
    max-width: 1200px;
}

/* ── INPUT CARD ── */
.input-card {
    background: white;
    border-radius: 10px;
    border: 1px solid #E8EAF0;
    padding: 20px 22px;
    margin-bottom: 20px;
}

.input-label {
    font-size: 11px;
    font-weight: 600;
    color: #8B90A0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
}

/* ── STAT ROW ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.stat-card {
    flex: 1;
    background: white;
    border: 1px solid #E8EAF0;
    border-radius: 10px;
    padding: 18px 20px;
}

.stat-num {
    font-size: 28px;
    font-weight: 600;
    color: #1C1C28;
    letter-spacing: -1px;
    font-family: 'DM Mono', monospace;
    line-height: 1;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 11px;
    color: #8B90A0;
    font-weight: 500;
}

/* ── STATUS BAR ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #F0F4FF;
    border-radius: 7px;
    padding: 7px 12px;
    font-size: 11.5px;
    color: #4A5080;
    margin-bottom: 20px;
}

.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3ECA7A;
    flex-shrink: 0;
    animation: blink 2s ease infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.status-bar strong { color: #1C1C28; font-weight: 600; }

/* ── PROGRESS BAR ── */
.prog-wrap {
    flex: 1;
    height: 2px;
    background: #D8DEFF;
    border-radius: 99px;
    overflow: hidden;
    margin-left: 4px;
}
.prog-fill {
    height: 100%;
    background: #3B6FE8;
    border-radius: 99px;
    animation: shrink 300s linear forwards;
}
@keyframes shrink {
    from { width: 100%; }
    to   { width: 0%; }
}

/* ── RESULT ── */
.result-card {
    background: white;
    border: 1px solid #E8EAF0;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 16px;
}

.result-card-header {
    padding: 13px 18px;
    border-bottom: 1px solid #E8EAF0;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #FAFBFF;
}

.result-card-header .npsn-tag {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    color: #3B6FE8;
    background: #EEF3FF;
    padding: 3px 10px;
    border-radius: 5px;
}

.result-card-header .inst-count {
    font-size: 12px;
    color: #8B90A0;
    margin-left: auto;
}

.result-card-meta {
    padding: 8px 18px;
    border-bottom: 1px solid #F0F2F8;
    font-size: 11px;
    color: #8B90A0;
    display: flex;
    gap: 16px;
}

.result-card-meta b { color: #4A5080; }

/* ── TABLE ── */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 12.5px !important;
    font-family: 'DM Sans', sans-serif !important;
}

thead th {
    background: #FAFBFF !important;
    color: #8B90A0 !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.7px !important;
    padding: 9px 14px !important;
    border-bottom: 1px solid #E8EAF0 !important;
    white-space: nowrap !important;
    text-align: left !important;
}

tbody td {
    padding: 9px 14px !important;
    border-bottom: 1px solid #F4F5F8 !important;
    color: #1C1C28 !important;
    white-space: normal !important;
    word-break: break-word !important;
}

tbody tr:last-child td { border-bottom: none !important; }
tbody tr:hover td { background: #FAFBFF !important; }

/* ── NOT FOUND ── */
.not-found {
    background: white;
    border: 1px solid #E8EAF0;
    border-radius: 10px;
    padding: 28px;
    text-align: center;
    color: #8B90A0;
}
.not-found .icon { font-size: 32px; margin-bottom: 8px; }
.not-found h4 { color: #1C1C28; font-size: 14px; margin-bottom: 4px; }
.not-found p { font-size: 12px; }

/* ── TOAST ── */
.toast {
    position: fixed;
    top: 70px;
    right: 24px;
    background: #1C1C28;
    color: white;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    z-index: 9999;
    animation: tin 0.3s ease, tout 0.3s ease 4s forwards;
    display: flex;
    align-items: center;
    gap: 10px;
}

.toast-icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #3ECA7A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    flex-shrink: 0;
}

.toast small { display: block; color: #8B90A0; font-size: 11px; font-weight: 400; }

@keyframes tin  { from { opacity:0; transform: translateY(-8px); } to { opacity:1; transform: translateY(0); } }
@keyframes tout { to   { opacity:0; transform: translateY(-8px); } }

/* ── STREAMLIT OVERRIDES ── */
.stTextInput input {
    border: 1px solid #E8EAF0 !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 9px 13px !important;
    background: #FAFBFF !important;
    color: #1C1C28 !important;
    transition: border-color 0.15s !important;
}
.stTextInput input:focus {
    border-color: #3B6FE8 !important;
    box-shadow: 0 0 0 3px rgba(59,111,232,0.1) !important;
}
.stTextInput label { font-size: 12px !important; color: #8B90A0 !important; }

.stButton button {
    background: #1C1C28 !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 9px 20px !important;
    transition: opacity 0.15s !important;
}
.stButton button:hover { opacity: 0.8 !important; }

[data-testid="stForm"] {
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    background: transparent !important;
}

.stAlert { border-radius: 8px !important; }

/* ── EXPANDER (media player) ── */
.streamlit-expanderHeader {
    background: white !important;
    border: 1px solid #E8EAF0 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #1C1C28 !important;
    padding: 12px 16px !important;
}
.streamlit-expanderContent {
    background: white !important;
    border: 1px solid #E8EAF0 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 12px 16px 16px !important;
}
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
# TOPBAR
# =========================================
st.markdown(f"""
<div class="topbar">
    <div class="topbar-dot"></div>
    <div class="topbar-title">Portal Data Sekolah</div>
    <div class="topbar-sep"></div>
    <div class="topbar-sub">Sistem Pencarian NPSN</div>
    <div class="topbar-right">{datetime.now().strftime("%d %b %Y, %H:%M")}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# =========================================
# YOUTUBE PLAYER
# =========================================
def extract_yt_id(url):
    """Extract YouTube video ID from various URL formats."""
    import re
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

with st.expander("🎵  Media Player", expanded=False):
    yt_url = st.text_input(
        "yt_url",
        placeholder="Paste link YouTube di sini...",
        label_visibility="collapsed",
        key="yt_input"
    )
    if yt_url:
        vid_id = extract_yt_id(yt_url)
        if vid_id:
            st.markdown(f"""
            <div style="border-radius:10px;overflow:hidden;margin-top:10px;border:1px solid #E8EAF0;">
                <iframe
                    width="100%"
                    height="220"
                    src="https://www.youtube.com/embed/{vid_id}?autoplay=1&rel=0"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                    style="display:block;"
                ></iframe>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("URL tidak dikenali. Pastikan link YouTube valid.")

st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

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
# LOAD DATA (cache 5 menit)
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
            .astype(str).str.lower().str.strip().str.replace(" ", "_")
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

    return pd.concat(semua_data, ignore_index=True) if semua_data else pd.DataFrame()

# =========================================
# FORM LOAD DATA
# =========================================
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Sumber Data</div>', unsafe_allow_html=True)

with st.form("sheet_form"):
    col_url, col_btn = st.columns([5, 1])
    with col_url:
        sheet_url_input = st.text_input(
            "url",
            placeholder="Tempel URL Google Spreadsheet di sini...",
            label_visibility="collapsed"
        )
    with col_btn:
        load_button = st.form_submit_button("Muat Data")

st.markdown('</div>', unsafe_allow_html=True)

if load_button and sheet_url_input:
    st.session_state.refresh_token = str(uuid.uuid4())
    st.session_state.active_sheet_url = sheet_url_input
    st.session_state.last_refresh = datetime.now()

# =========================================
# MAIN CONTENT
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
            <div class="live-dot"></div>
            Terakhir dimuat: <strong>{st.session_state.last_refresh.strftime("%H:%M:%S")}</strong>
            &nbsp;·&nbsp; Refresh dalam: <strong>{m}m {s:02d}s</strong>
            <div class="prog-wrap"><div class="prog-fill"></div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Stat cards ──
        total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-num">{len(data):,}</div>
                <div class="stat-label">Total Baris</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-num">{total_sekolah:,}</div>
                <div class="stat-label">Total Sekolah</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-num">{data["source_sheet"].nunique()}</div>
                <div class="stat-label">Sheet Aktif</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

        # ── Search ──
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown('<div class="input-label">Cari NPSN</div>', unsafe_allow_html=True)
        npsn_input = st.text_input(
            "npsn",
            placeholder="Masukkan nomor NPSN, contoh: 20123456",
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
                <div class="toast">
                    <div class="toast-icon">✓</div>
                    <div>
                        NPSN {base_npsn} ditemukan
                        <small>{len(hasil)} instalasi tercatat</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

                for grp, df_grp in hasil.groupby("group"):
                    sheets_used = " · ".join(df_grp["source_sheet"].unique())
                    df_display = df_grp.drop(columns=["group"])

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-card-header">
                            <span class="npsn-tag">{grp}</span>
                            <span class="inst-count">{len(df_grp)} instalasi</span>
                        </div>
                        <div class="result-card-meta">
                            Sheet: <b>{sheets_used}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.table(df_display)

            else:
                st.markdown(f"""
                <div class="not-found">
                    <div class="icon">🔍</div>
                    <h4>Data tidak ditemukan</h4>
                    <p>NPSN <strong>{base_npsn}</strong> tidak ada dalam database. Periksa kembali nomor yang dimasukkan.</p>
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
    st.markdown("""
    <div class="not-found" style="padding:40px">
        <div class="icon">📋</div>
        <h4>Belum ada data</h4>
        <p>Masukkan URL Google Spreadsheet di atas untuk mulai memuat data.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
