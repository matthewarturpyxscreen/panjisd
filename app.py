import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time
import re

st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

# =========================================
# GLOBAL STYLE
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');
*,*::before,*::after{box-sizing:border-box}

.stApp{background:#f0f4fa;font-family:'IBM Plex Sans',sans-serif;color:#1e293b}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#e2e8f0}
::-webkit-scrollbar-thumb{background:#3b82f6;border-radius:3px}

/* SIDEBAR */
[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid #e2e8f0!important}
[data-testid="stSidebar"] > div{padding:16px 14px!important}

/* HEADER */
.header-wrap{
    display:flex;align-items:center;gap:16px;
    padding:18px 24px;
    background:linear-gradient(135deg,#1d4ed8 0%,#2563eb 60%,#3b82f6 100%);
    border-radius:10px;margin-bottom:20px;position:relative;overflow:hidden;
    box-shadow:0 4px 20px rgba(37,99,235,0.25);
}
.header-wrap::after{
    content:'';position:absolute;top:-25px;right:-25px;
    width:120px;height:120px;border-radius:50%;
    background:rgba(255,255,255,0.07);pointer-events:none;
}
.header-icon{font-size:28px;line-height:1}
.header-title{font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;
    color:#fff;margin:0;line-height:1.2}
.header-sub{font-size:11px;color:rgba(255,255,255,0.6);margin:2px 0 0 0}
.header-badge{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:10px;
    color:#fff;border:1px solid rgba(255,255,255,0.3);padding:4px 10px;
    border-radius:20px;background:rgba(255,255,255,0.12);white-space:nowrap}

/* STAT CARDS */
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}
.stat-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
    padding:16px 18px;box-shadow:0 1px 5px rgba(0,0,0,0.05);
    display:flex;align-items:center;gap:14px}
.stat-icon{width:42px;height:42px;border-radius:9px;
    display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.stat-icon.blue{background:#dbeafe}.stat-icon.green{background:#dcfce7}.stat-icon.purple{background:#ede9fe}
.stat-label{font-size:10px;text-transform:uppercase;letter-spacing:.8px;
    color:#94a3b8;font-family:'IBM Plex Mono',monospace;margin-bottom:2px}
.stat-value{font-family:'IBM Plex Mono',monospace;font-size:24px;font-weight:600;
    color:#0f172a;line-height:1}
.stat-desc{font-size:11px;color:#94a3b8;margin-top:2px}

/* PANEL TITLE */
.panel-title{font-family:'IBM Plex Mono',monospace;font-size:11px;
    text-transform:uppercase;letter-spacing:1px;color:#64748b;
    margin:0 0 10px 0;display:flex;align-items:center;gap:7px}
.panel-title .bar{display:inline-block;width:3px;height:13px;
    background:#3b82f6;border-radius:2px}

/* INPUT */
div[data-testid="stForm"]{background:transparent!important;border:none!important;padding:0!important;margin:0!important}
.stTextInput>div>div>input{background:#f8fafc!important;border:1px solid #e2e8f0!important;
    color:#1e293b!important;border-radius:8px!important;
    font-family:'IBM Plex Mono',monospace!important;font-size:13px!important}
.stTextInput>div>div>input:focus{border-color:#3b82f6!important;
    box-shadow:0 0 0 3px rgba(59,130,246,.12)!important;background:#fff!important}
.stTextInput>label{color:#64748b!important;font-size:11px!important;
    font-family:'IBM Plex Mono',monospace!important;text-transform:uppercase!important;letter-spacing:.8px!important}

/* BUTTON */
.stButton>button,.stFormSubmitButton>button{background:#2563eb!important;color:#fff!important;
    border:none!important;border-radius:8px!important;
    font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;
    font-weight:600!important;letter-spacing:.4px!important;padding:8px 16px!important;
    transition:all .15s!important;box-shadow:0 2px 6px rgba(37,99,235,.2)!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#1d4ed8!important;transform:translateY(-1px)!important}

/* SYNC BAR */
.sync-bar{display:flex;align-items:center;gap:9px;font-family:'IBM Plex Mono',monospace;
    font-size:11px;color:#64748b;margin-bottom:16px;padding:8px 14px;
    background:#fff;border:1px solid #e2e8f0;border-radius:8px;
    box-shadow:0 1px 4px rgba(0,0,0,.04)}
.sync-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;
    animation:pulse 2s infinite;flex-shrink:0}
@keyframes pulse{0%,100%{box-shadow:0 0 0 2px rgba(34,197,94,.25)}
    50%{box-shadow:0 0 0 5px rgba(34,197,94,.08)}}

/* RESULT */
.result-header{display:flex;align-items:center;gap:9px;padding:11px 16px;
    background:#f8fafc;border:1px solid #e2e8f0;border-bottom:2px solid #3b82f6;
    border-radius:10px 10px 0 0;font-family:'IBM Plex Mono',monospace;
    font-size:12px;font-weight:600;color:#1e293b;margin-top:16px}
.result-badge{font-size:10px;background:#dbeafe;color:#1d4ed8;
    border:1px solid #bfdbfe;padding:2px 9px;border-radius:10px;font-weight:600}
.result-card{background:#fff;border:1px solid #e2e8f0;border-top:none;
    border-radius:0 0 10px 10px;margin-bottom:18px;overflow:hidden;
    box-shadow:0 2px 7px rgba(0,0,0,.04)}

/* SUCCESS BANNER */
.success-banner{background:linear-gradient(135deg,#dcfce7,#f0fdf4);
    border:1px solid #86efac;border-left:4px solid #22c55e;border-radius:10px;
    padding:13px 18px;margin-bottom:14px;display:flex;align-items:flex-start;gap:12px;
    box-shadow:0 2px 7px rgba(34,197,94,.1);animation:bannerIn .4s cubic-bezier(.34,1.56,.64,1)}
@keyframes bannerIn{from{transform:translateY(-8px);opacity:0}to{transform:translateY(0);opacity:1}}
.success-icon{font-size:20px;line-height:1;flex-shrink:0}
.success-title{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
    color:#15803d;margin-bottom:2px}
.success-msg{font-size:11px;color:#166534}

/* TABLE */
.stTable,table{width:100%!important;border-collapse:collapse!important;
    font-size:12px!important;font-family:'IBM Plex Sans',sans-serif!important}
thead tr{background:#f8fafc!important}
thead th{color:#64748b!important;font-size:10px!important;text-transform:uppercase!important;
    letter-spacing:.8px!important;padding:9px 12px!important;
    border-bottom:1px solid #e2e8f0!important;white-space:nowrap!important;
    font-family:'IBM Plex Mono',monospace!important}
tbody tr{border-bottom:1px solid #f1f5f9!important}
tbody tr:hover{background:#f0f7ff!important}
tbody td{padding:8px 12px!important;color:#334155!important;
    white-space:normal!important;word-break:break-word!important;border:none!important}

/* TOAST */
.toast{position:fixed;top:20px;right:20px;background:#fff;
    border:1px solid #86efac;border-left:4px solid #22c55e;color:#1e293b;
    padding:12px 18px;border-radius:10px;
    box-shadow:0 8px 28px rgba(0,0,0,.12);
    font-family:'IBM Plex Mono',monospace;font-size:11px;z-index:9999;
    animation:toastIn .35s cubic-bezier(.34,1.56,.64,1),toastOut .4s ease 4.5s forwards;min-width:240px}
.toast-title{font-weight:600;color:#15803d;margin-bottom:3px}
.toast-body{color:#64748b}
@keyframes toastIn{from{transform:translateX(120%);opacity:0}to{transform:translateX(0);opacity:1}}
@keyframes toastOut{to{transform:translateX(120%);opacity:0}}

hr{border:none;border-top:1px solid #e2e8f0;margin:16px 0}

/* ===== SIDEBAR YOUTUBE PLAYER ===== */
.yt-sidebar-wrap{
    background:#f8fafc;border:1px solid #e2e8f0;
    border-radius:10px;overflow:hidden;margin-bottom:14px}
.yt-sb-header{display:flex;align-items:center;justify-content:space-between;
    padding:10px 12px;background:#fff;border-bottom:1px solid #e2e8f0}
.yt-sb-title{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
    color:#1e293b;display:flex;align-items:center;gap:6px}
.yt-logo{background:#ff0000;color:#fff;font-size:8px;font-weight:700;
    padding:2px 5px;border-radius:3px;letter-spacing:.4px}
.yt-counter{font-size:10px;color:#94a3b8;font-family:'IBM Plex Mono',monospace}
.yt-frame-sb{width:100%;aspect-ratio:16/9;border:none;display:block}
.yt-queue-sb{padding:0 10px 10px 10px;max-height:180px;overflow-y:auto}
.yt-queue-label{font-family:'IBM Plex Mono',monospace;font-size:9px;
    text-transform:uppercase;letter-spacing:1px;color:#94a3b8;
    padding:8px 0 5px 0;border-top:1px solid #f1f5f9}
.yt-q-item{display:flex;align-items:center;gap:7px;padding:5px 7px;
    border-radius:6px;font-size:11px;color:#475569;margin-bottom:1px;
    font-family:'IBM Plex Sans',sans-serif;cursor:default}
.yt-q-item.active{background:#dbeafe;color:#1d4ed8;font-weight:600}
.yt-q-num{font-family:'IBM Plex Mono',monospace;font-size:9px;color:#94a3b8;
    width:14px;text-align:center;flex-shrink:0}
.yt-q-item.active .yt-q-num{color:#3b82f6}
.yt-q-url{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px}
.yt-empty-sb{text-align:center;padding:18px 10px;color:#94a3b8;
    font-family:'IBM Plex Mono',monospace;font-size:10px;
    border:1px dashed #cbd5e1;border-radius:8px;margin-bottom:12px}
.yt-nav-row{display:flex;gap:5px;padding:0 10px 10px 10px}
.yt-nav-btn{flex:1;background:#fff;border:1px solid #e2e8f0;border-radius:7px;
    padding:6px 4px;font-size:11px;font-family:'IBM Plex Mono',monospace;
    color:#475569;cursor:pointer;text-align:center;transition:all .12s;font-weight:500}
.yt-nav-btn:hover{background:#dbeafe;color:#1d4ed8;border-color:#bfdbfe}
.yt-nav-btn.danger{color:#ef4444}
.yt-nav-btn.danger:hover{background:#fee2e2;border-color:#fca5a5;color:#dc2626}
.yt-float-toggle{background:#fff;border:1px solid #e2e8f0;border-radius:7px;
    padding:6px 10px;font-size:10px;font-family:'IBM Plex Mono',monospace;
    color:#64748b;cursor:pointer;transition:all .12s;white-space:nowrap}
.yt-float-toggle:hover{background:#ede9fe;color:#7c3aed;border-color:#c4b5fd}
.yt-float-toggle.active{background:#ede9fe;color:#7c3aed;border-color:#c4b5fd;font-weight:600}

/* ===== FLOATING PLAYER ===== */
.yt-floating{
    position:fixed;bottom:24px;right:24px;
    width:300px;
    background:#fff;border:1px solid #e2e8f0;border-radius:12px;
    box-shadow:0 16px 48px rgba(0,0,0,.18);
    z-index:9998;overflow:hidden;
    animation:floatIn .3s cubic-bezier(.34,1.2,.64,1)}
@keyframes floatIn{from{transform:translateY(30px) scale(.95);opacity:0}
    to{transform:translateY(0) scale(1);opacity:1}}
.yt-floating .yt-sb-header{background:#1e293b;border-bottom:1px solid #334155}
.yt-floating .yt-sb-title{color:#f1f5f9}
.yt-floating .yt-counter{color:#64748b}
.yt-floating .yt-nav-row{background:#f8fafc;padding:8px 10px}
.yt-floating .yt-queue-sb{background:#fff;max-height:120px}
.yt-float-close{background:rgba(255,255,255,.1);border:none;border-radius:5px;
    color:#94a3b8;font-size:14px;padding:2px 7px;cursor:pointer;
    font-family:'IBM Plex Mono',monospace;transition:all .1s}
.yt-float-close:hover{background:rgba(239,68,68,.2);color:#ef4444}
</style>
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
    "yt_float": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================
# YT HELPERS
# =========================================
def extract_yt_id(url):
    for p in [r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", r"^([A-Za-z0-9_-]{11})$"]:
        m = re.search(p, url.strip())
        if m:
            return m.group(1)
    return None

def make_playlist_embed(queue, start_idx):
    """
    Buat embed URL dengan playlist= supaya YT punya kontrol next/prev native.
    Video pertama di-load, sisanya jadi playlist.
    """
    if not queue:
        return ""
    vid   = queue[start_idx]
    rest  = [queue[i] for i in range(len(queue)) if i != start_idx]
    pl    = ",".join([vid] + rest)
    return (
        f"https://www.youtube-nocookie.com/embed/{vid}"
        f"?autoplay=1&rel=0&modestbranding=1"
        f"&playlist={pl}&listType=playlist"
    )

# =========================================
# SIDEBAR — YOUTUBE PLAYER
# =========================================
with st.sidebar:
    st.markdown("""
    <div class="panel-title"><span class="bar"></span>🎵 Media Player</div>
    """, unsafe_allow_html=True)

    # Input tambah video
    yt_url_sb = st.text_input(
        "yt_sb",
        placeholder="Paste link YouTube...",
        label_visibility="collapsed",
        key="yt_sb_input"
    )
    c1, c2 = st.columns([3, 2])
    with c1:
        add_yt_sb = st.button("➕ Tambah", key="sb_add", use_container_width=True)
    with c2:
        float_btn = st.button(
            "⧉ Float" if not st.session_state.yt_float else "✕ Float",
            key="sb_float",
            use_container_width=True
        )

    if add_yt_sb and yt_url_sb.strip():
        vid_id = extract_yt_id(yt_url_sb.strip())
        if vid_id:
            st.session_state.yt_queue.append(vid_id)
            st.session_state.yt_current = len(st.session_state.yt_queue) - 1
            st.rerun()
        else:
            st.warning("Link tidak valid.")

    if float_btn:
        st.session_state.yt_float = not st.session_state.yt_float
        st.rerun()

    queue = st.session_state.yt_queue
    idx   = st.session_state.yt_current

    # ---- Player compact di sidebar (sembunyikan jika floating) ----
    if queue and not st.session_state.yt_float:
        embed_url  = make_playlist_embed(queue, idx)
        track_num  = f"{idx + 1}/{len(queue)}"

        queue_html = ""
        for i, vid in enumerate(queue):
            active_cls = "active" if i == idx else ""
            queue_html += f"""
            <div class="yt-q-item {active_cls}">
                <span class="yt-q-num">{i+1}</span>
                <span class="yt-q-url">{'▶ ' if i==idx else ''}{vid}</span>
            </div>"""

        st.markdown(f"""
        <div class="yt-sidebar-wrap">
            <div class="yt-sb-header">
                <div class="yt-sb-title">
                    <span class="yt-logo">YT</span> Now Playing
                </div>
                <span class="yt-counter">{track_num}</span>
            </div>
            <iframe class="yt-frame-sb"
                src="{embed_url}"
                allow="autoplay; encrypted-media; fullscreen"
                allowfullscreen>
            </iframe>
            <div class="yt-queue-sb">
                <div class="yt-queue-label">Antrian — {len(queue)} video</div>
                {queue_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Prev / Next / Clear
        n1, n2, n3 = st.columns(3)
        with n1:
            if st.button("⏮", key="sb_prev", use_container_width=True):
                st.session_state.yt_current = max(0, idx - 1)
                st.rerun()
        with n2:
            if st.button("⏭", key="sb_next", use_container_width=True):
                st.session_state.yt_current = min(len(queue)-1, idx + 1)
                st.rerun()
        with n3:
            if st.button("🗑", key="sb_clear", use_container_width=True):
                st.session_state.yt_queue   = []
                st.session_state.yt_current = 0
                st.rerun()

    elif not queue:
        st.markdown("""
        <div class="yt-empty-sb">
            🎵 Belum ada video<br>tambahkan link di atas
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.yt_float and queue:
        st.markdown(f"""
        <div style="background:#ede9fe;border:1px solid #c4b5fd;border-radius:8px;
                    padding:10px 12px;text-align:center;font-family:'IBM Plex Mono',monospace;
                    font-size:10px;color:#7c3aed;margin-bottom:12px;">
            ⧉ Mode floating aktif<br>
            <span style="color:#94a3b8">{len(queue)} video di antrian</span>
        </div>
        """, unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        with n1:
            if st.button("⏮", key="sb_prev_f", use_container_width=True):
                st.session_state.yt_current = max(0, idx - 1)
                st.rerun()
        with n2:
            if st.button("⏭", key="sb_next_f", use_container_width=True):
                st.session_state.yt_current = min(len(queue)-1, idx + 1)
                st.rerun()
        with n3:
            if st.button("🗑", key="sb_clear_f", use_container_width=True):
                st.session_state.yt_queue   = []
                st.session_state.yt_current = 0
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

# =========================================
# FLOATING PLAYER (inject di main)
# =========================================
if st.session_state.yt_float and st.session_state.yt_queue:
    queue     = st.session_state.yt_queue
    idx       = st.session_state.yt_current
    embed_url = make_playlist_embed(queue, idx)
    track_num = f"{idx+1}/{len(queue)}"

    queue_html = ""
    for i, vid in enumerate(queue):
        active_cls = "active" if i == idx else ""
        queue_html += f"""
        <div class="yt-q-item {active_cls}">
            <span class="yt-q-num">{i+1}</span>
            <span class="yt-q-url">{'▶ ' if i==idx else ''}{vid}</span>
        </div>"""

    st.markdown(f"""
    <div class="yt-floating">
        <div class="yt-sb-header" style="background:#1e293b;border-bottom:1px solid #334155;">
            <div class="yt-sb-title" style="color:#f1f5f9;">
                <span class="yt-logo">YT</span> Floating Player
            </div>
            <span class="yt-counter">{track_num}</span>
        </div>
        <iframe class="yt-frame-sb"
            src="{embed_url}"
            allow="autoplay; encrypted-media; fullscreen"
            allowfullscreen>
        </iframe>
        <div class="yt-queue-sb" style="background:#fff;max-height:110px">
            <div class="yt-queue-label">Antrian — {len(queue)} video</div>
            {queue_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# MAIN — HEADER
# =========================================
st.markdown("""
<div class="header-wrap">
    <div class="header-icon">🏫</div>
    <div>
        <h1 class="header-title">Portal Data Sekolah</h1>
        <p class="header-sub">Sistem pencarian instalasi berbasis NPSN</p>
    </div>
    <span class="header-badge">NPSN LOOKUP v2.2</span>
</div>
""", unsafe_allow_html=True)

# =========================================
# FORM LOAD DATA
# =========================================
st.markdown("""<div class="panel-title"><span class="bar"></span>📂 Sumber Data</div>""",
            unsafe_allow_html=True)

with st.form("sheet_form"):
    sheet_url_input = st.text_input("Link Google Spreadsheet",
        placeholder="https://docs.google.com/spreadsheets/d/...")
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
            if any("npsn" in v for v in raw.iloc[i].astype(str).str.lower().tolist()):
                header_row = i
                break
        if header_row is None:
            return None
        df = raw.iloc[header_row+1:].copy()
        df.columns = (raw.iloc[header_row].astype(str).str.lower()
                      .str.strip().str.replace(" ", "_"))
        for c in df.columns:
            if "npsn" in c:
                df = df.rename(columns={c: "npsn"})
                break
        if "npsn" not in df.columns:
            return None
        df["source_sheet"] = sheet_name
        return df.reset_index(drop=True)

    for sheet in excel.sheet_names:
        h = auto_read(sheet)
        if h is not None:
            semua_data.append(h)

    return pd.concat(semua_data, ignore_index=True) if semua_data else pd.DataFrame()

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
    pct     = int((elapsed / REFRESH_INTERVAL) * 100)

    st.markdown(f"""
    <div class="sync-bar">
        <span class="sync-dot"></span>
        <span>LIVE — Sinkronisasi terakhir: <b>{now_str}</b></span>
        &nbsp;|&nbsp;
        <span>Refresh: <b>{sisa//60:02d}:{sisa%60:02d}</b></span>
        &nbsp;|&nbsp;
        <span style="color:#2563eb;font-weight:600">{pct}% cycle</span>
    </div>
    """, unsafe_allow_html=True)

    total_rows    = len(data)
    total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
    total_sheets  = data["source_sheet"].nunique()

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon blue">📋</div>
            <div><div class="stat-label">Total Baris</div>
            <div class="stat-value">{total_rows:,}</div>
            <div class="stat-desc">semua sheet gabungan</div></div>
        </div>
        <div class="stat-card">
            <div class="stat-icon green">🏫</div>
            <div><div class="stat-label">Total Sekolah</div>
            <div class="stat-value">{total_sekolah:,}</div>
            <div class="stat-desc">unique NPSN terdeteksi</div></div>
        </div>
        <div class="stat-card">
            <div class="stat-icon purple">📑</div>
            <div><div class="stat-label">Sheet Aktif</div>
            <div class="stat-value">{total_sheets}</div>
            <div class="stat-desc">sheet memiliki kolom NPSN</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- SEARCH ----
    st.markdown("""<div class="panel-title"><span class="bar"></span>🔍 Cari Data NPSN</div>""",
                unsafe_allow_html=True)

    npsn_input = st.text_input("Cari NPSN",
        placeholder="Masukkan NPSN lalu tekan Enter...",
        key="npsn_box", label_visibility="collapsed")

    if npsn_input:
        base_npsn = str(npsn_input).strip().split("_")[0]
        hasil = data[data["npsn"].astype(str).str.strip().str.startswith(base_npsn)]

        if len(hasil) > 0:
            st.markdown(f"""
            <div class="toast">
                <div class="toast-title">✅ Data Berhasil Ditemukan!</div>
                <div class="toast-body">NPSN <b>{base_npsn}</b> — {len(hasil)} instalasi</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="success-banner">
                <div class="success-icon">✅</div>
                <div>
                    <div class="success-title">Pencarian Berhasil!</div>
                    <div class="success-msg">
                        Data NPSN <b>{base_npsn}</b> ditemukan —
                        <b>{len(hasil)} instalasi</b> tersedia. Lihat detail di bawah.
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

    time.sleep(30)
    st.rerun()
