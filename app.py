import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time
import re

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
    background: #f0f4fa;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #1e293b;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #e2e8f0; }
::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 3px; }

/* ---- HEADER ---- */
.header-wrap {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px 28px;
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #3b82f6 100%);
    border-radius: 10px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(37,99,235,0.25);
}

.header-wrap::after {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    pointer-events: none;
}

.header-wrap::before {
    content: '';
    position: absolute;
    bottom: -40px; right: 80px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
    pointer-events: none;
}

.header-icon { font-size: 32px; line-height: 1; }

.header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.3px;
    margin: 0;
    line-height: 1.2;
}

.header-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.65);
    font-family: 'IBM Plex Sans', sans-serif;
    margin: 2px 0 0 0;
}

.header-badge {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #fff;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 5px 12px;
    border-radius: 20px;
    background: rgba(255,255,255,0.12);
    white-space: nowrap;
}

/* ---- STAT CARDS ---- */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 22px;
}

.stat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    display: flex;
    align-items: center;
    gap: 16px;
}

.stat-icon {
    width: 46px; height: 46px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.stat-icon.blue   { background: #dbeafe; }
.stat-icon.green  { background: #dcfce7; }
.stat-icon.purple { background: #ede9fe; }

.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 3px;
}

.stat-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 600;
    color: #0f172a;
    line-height: 1;
}

.stat-desc { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* ---- PANEL TITLE ---- */
.panel-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.panel-title .bar {
    display: inline-block;
    width: 3px; height: 14px;
    background: #3b82f6;
    border-radius: 2px;
}

/* ---- FORM / INPUT ---- */
div[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.stTextInput > div > div > input {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #1e293b !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    background: #fff !important;
}

.stTextInput > label {
    color: #64748b !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

/* ---- BUTTON ---- */
.stButton > button, .stFormSubmitButton > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 9px 22px !important;
    transition: all 0.15s !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.2) !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px) !important;
}

/* ---- SYNC BAR ---- */
.sync-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #64748b;
    margin-bottom: 18px;
    padding: 9px 16px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.sync-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 2px rgba(34,197,94,0.25); }
    50% { box-shadow: 0 0 0 5px rgba(34,197,94,0.08); }
}

/* ---- RESULT SECTION ---- */
.result-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 18px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-bottom: 2px solid #3b82f6;
    border-radius: 10px 10px 0 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    margin-top: 18px;
}

.result-badge {
    font-size: 10px;
    background: #dbeafe;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 2px 10px;
    border-radius: 10px;
    font-weight: 600;
}

.result-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ---- SUCCESS BANNER ---- */
.success-banner {
    background: linear-gradient(135deg, #dcfce7, #f0fdf4);
    border: 1px solid #86efac;
    border-left: 4px solid #22c55e;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    box-shadow: 0 2px 8px rgba(34,197,94,0.1);
    animation: bannerIn 0.4s cubic-bezier(0.34,1.56,0.64,1);
}

@keyframes bannerIn {
    from { transform: translateY(-8px); opacity: 0; }
    to   { transform: translateY(0); opacity: 1; }
}

.success-icon { font-size: 22px; line-height: 1; flex-shrink: 0; }

.success-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #15803d;
    margin-bottom: 3px;
}

.success-msg { font-size: 12px; color: #166534; }

/* ---- TABLE ---- */
.stTable, table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

thead tr { background: #f8fafc !important; }

thead th {
    color: #64748b !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #e2e8f0 !important;
    white-space: nowrap !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

tbody tr { border-bottom: 1px solid #f1f5f9 !important; }
tbody tr:hover { background: #f0f7ff !important; }

tbody td {
    padding: 9px 14px !important;
    color: #334155 !important;
    white-space: normal !important;
    word-break: break-word !important;
    border: none !important;
}

/* ---- TOAST ---- */
.toast {
    position: fixed;
    top: 22px;
    right: 22px;
    background: #ffffff;
    border: 1px solid #86efac;
    border-left: 4px solid #22c55e;
    color: #1e293b;
    padding: 14px 20px;
    border-radius: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    z-index: 9999;
    animation: toastIn 0.35s cubic-bezier(0.34,1.56,0.64,1), toastOut 0.4s ease 4.5s forwards;
    min-width: 260px;
}

.toast-title { font-weight: 600; color: #15803d; margin-bottom: 4px; }
.toast-body  { color: #64748b; }

@keyframes toastIn {
    from { transform: translateX(120%); opacity: 0; }
    to   { transform: translateX(0); opacity: 1; }
}
@keyframes toastOut {
    to { transform: translateX(120%); opacity: 0; }
}

/* ---- YOUTUBE PLAYER ---- */
.yt-player-wrap {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

.yt-player-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}

.yt-player-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 8px;
}

.yt-logo {
    background: #ff0000;
    color: white;
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
    letter-spacing: 0.5px;
}

.yt-frame {
    width: 100%;
    aspect-ratio: 16/9;
    border: none;
    display: block;
}

.yt-queue {
    padding: 0 18px 14px 18px;
    background: #ffffff;
}

.yt-queue-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    margin-bottom: 8px;
    padding-top: 12px;
    border-top: 1px solid #f1f5f9;
}

.yt-queue-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    border-radius: 7px;
    font-size: 12px;
    color: #475569;
    margin-bottom: 2px;
    font-family: 'IBM Plex Sans', sans-serif;
}

.yt-queue-item.active {
    background: #dbeafe;
    color: #1d4ed8;
    font-weight: 600;
}

.yt-queue-idx {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #94a3b8;
    width: 18px;
    text-align: center;
    flex-shrink: 0;
}

.yt-queue-item.active .yt-queue-idx { color: #3b82f6; }

.yt-empty {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 10px;
    padding: 24px;
    text-align: center;
    margin-bottom: 18px;
    color: #94a3b8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
}

hr { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="header-wrap">
    <div class="header-icon">🏫</div>
    <div>
        <h1 class="header-title">Portal Data Sekolah</h1>
        <p class="header-sub">Sistem pencarian instalasi berbasis NPSN</p>
    </div>
    <span class="header-badge">NPSN LOOKUP v2.1</span>
</div>
""", unsafe_allow_html=True)

# =========================================
# SESSION INIT
# =========================================
defaults = {
    "refresh_token": str(uuid.uuid4()),
    "active_sheet_url": None,
    "last_refresh_time": time.time(),
    "yt_queue": [],
    "yt_current": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================
# YOUTUBE HELPER
# =========================================
def extract_yt_id(url):
    patterns = [
        r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url.strip())
        if m:
            return m.group(1)
    return None

def get_yt_embed(video_id):
    return (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        f"?autoplay=1&rel=0&modestbranding=1"
    )

# =========================================
# YOUTUBE MEDIA PLAYER
# =========================================
st.markdown("""
<div class="panel-title"><span class="bar"></span>🎵 YouTube Media Player</div>
""", unsafe_allow_html=True)

col_input, col_add, col_prev, col_next, col_clear = st.columns([4, 1.2, 0.9, 0.9, 0.9])

with col_input:
    yt_url = st.text_input(
        "yt_url",
        placeholder="Paste link YouTube atau video ID...",
        label_visibility="collapsed",
        key="yt_url_input"
    )
with col_add:
    add_yt   = st.button("➕ Tambah",  key="btn_add_yt",  use_container_width=True)
with col_prev:
    prev_yt  = st.button("⏮ Prev",    key="btn_prev",    use_container_width=True)
with col_next:
    next_yt  = st.button("⏭ Next",    key="btn_next",    use_container_width=True)
with col_clear:
    clear_yt = st.button("🗑 Clear",   key="btn_clear",   use_container_width=True)

if add_yt and yt_url.strip():
    vid_id = extract_yt_id(yt_url.strip())
    if vid_id:
        st.session_state.yt_queue.append(vid_id)
        st.session_state.yt_current = len(st.session_state.yt_queue) - 1
        st.rerun()
    else:
        st.warning("⚠️ Link YouTube tidak valid. Coba salin langsung dari browser.")

if prev_yt and st.session_state.yt_queue:
    st.session_state.yt_current = max(0, st.session_state.yt_current - 1)
    st.rerun()

if next_yt and st.session_state.yt_queue:
    st.session_state.yt_current = min(
        len(st.session_state.yt_queue) - 1,
        st.session_state.yt_current + 1
    )
    st.rerun()

if clear_yt:
    st.session_state.yt_queue = []
    st.session_state.yt_current = 0
    st.rerun()

# Render Player
queue = st.session_state.yt_queue
idx   = st.session_state.yt_current

if queue:
    current_id = queue[idx]
    embed_url  = get_yt_embed(current_id)
    track_num  = f"{idx + 1} / {len(queue)}"

    queue_html = ""
    for i, vid in enumerate(queue):
        active_cls = "active" if i == idx else ""
        queue_html += f"""
        <div class="yt-queue-item {active_cls}">
            <span class="yt-queue-idx">{i+1}</span>
            <span>{'▶ ' if i == idx else ''}https://youtu.be/{vid}</span>
        </div>"""

    st.markdown(f"""
    <div class="yt-player-wrap">
        <div class="yt-player-header">
            <div class="yt-player-title">
                <span class="yt-logo">YT</span>
                Memutar {track_num}
            </div>
            <span style="font-size:11px;color:#94a3b8;font-family:'IBM Plex Mono',monospace;">
                ID: {current_id}
            </span>
        </div>
        <iframe class="yt-frame"
            src="{embed_url}"
            allow="autoplay; encrypted-media; fullscreen"
            allowfullscreen>
        </iframe>
        <div class="yt-queue">
            <div class="yt-queue-title">Antrian — {len(queue)} video</div>
            {queue_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="yt-empty">
        🎵 &nbsp;Belum ada video di antrian —
        tambahkan link YouTube di atas
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================
# FORM LOAD DATA
# =========================================
st.markdown("""
<div class="panel-title"><span class="bar"></span>📂 Sumber Data Spreadsheet</div>
""", unsafe_allow_html=True)

with st.form("sheet_form"):
    sheet_url_input = st.text_input(
        "Link Google Spreadsheet",
        placeholder="https://docs.google.com/spreadsheets/d/..."
    )
    load_button = st.form_submit_button("▶  Load / Refresh Data")

if load_button and sheet_url_input:
    st.session_state.refresh_token     = str(uuid.uuid4())
    st.session_state.active_sheet_url  = sheet_url_input
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
# CACHE 5 MENIT
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
REFRESH_INTERVAL = 300

if st.session_state.active_sheet_url:

    clean_url = build_clean_export_url(st.session_state.active_sheet_url)
    elapsed   = time.time() - st.session_state.last_refresh_time

    if elapsed >= REFRESH_INTERVAL:
        st.session_state.refresh_token     = str(uuid.uuid4())
        st.session_state.last_refresh_time = time.time()
        elapsed = 0

    data = load_all_sheets(clean_url, st.session_state.refresh_token)

    now_str = datetime.now().strftime("%H:%M:%S")
    sisa    = max(0, int(REFRESH_INTERVAL - elapsed))
    menit   = sisa // 60
    detik   = sisa % 60
    pct     = int((elapsed / REFRESH_INTERVAL) * 100)

    st.markdown(f"""
    <div class="sync-bar">
        <span class="sync-dot"></span>
        <span>LIVE &nbsp;—&nbsp; Sinkronisasi terakhir: <b>{now_str}</b></span>
        &nbsp;|&nbsp;
        <span>Refresh berikutnya: <b>{menit:02d}:{detik:02d}</b></span>
        &nbsp;|&nbsp;
        <span style="color:#2563eb;font-weight:600;">{pct}% cycle</span>
    </div>
    """, unsafe_allow_html=True)

    total_rows    = len(data)
    total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
    total_sheets  = data["source_sheet"].nunique()

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon blue">📋</div>
            <div>
                <div class="stat-label">Total Baris</div>
                <div class="stat-value">{total_rows:,}</div>
                <div class="stat-desc">semua sheet gabungan</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon green">🏫</div>
            <div>
                <div class="stat-label">Total Sekolah</div>
                <div class="stat-value">{total_sekolah:,}</div>
                <div class="stat-desc">unique NPSN terdeteksi</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon purple">📑</div>
            <div>
                <div class="stat-label">Sheet Aktif</div>
                <div class="stat-value">{total_sheets}</div>
                <div class="stat-desc">sheet memiliki kolom NPSN</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- SEARCH ----
    st.markdown("""
    <div class="panel-title" style="margin-bottom:8px;">
        <span class="bar"></span>🔍 Cari Data NPSN
    </div>
    """, unsafe_allow_html=True)

    npsn_input = st.text_input(
        "Cari NPSN",
        placeholder="Masukkan NPSN lalu tekan Enter...",
        key="npsn_box",
        label_visibility="collapsed"
    )

    if npsn_input:
        base_npsn = str(npsn_input).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil) > 0:

            # Toast pojok kanan atas
            st.markdown(f"""
            <div class="toast">
                <div class="toast-title">✅ Data Berhasil Ditemukan!</div>
                <div class="toast-body">NPSN <b>{base_npsn}</b> — {len(hasil)} instalasi</div>
            </div>
            """, unsafe_allow_html=True)

            # Banner inline
            st.markdown(f"""
            <div class="success-banner">
                <div class="success-icon">✅</div>
                <div>
                    <div class="success-title">Pencarian Berhasil!</div>
                    <div class="success-msg">
                        Data NPSN <b>{base_npsn}</b> ditemukan —
                        <b>{len(hasil)} instalasi</b> tersedia.
                        Scroll ke bawah untuk melihat detail lengkap.
                    </div>
                </div>
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
            st.warning(f"⚠️ NPSN **{base_npsn}** tidak ditemukan dalam database.")

    # Auto rerun setiap 30 detik
    time.sleep(30)
    st.rerun()
