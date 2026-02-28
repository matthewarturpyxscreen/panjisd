import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import uuid
import time
import re
import json

st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

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
    "dark_mode": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

DM = st.session_state.dark_mode

T = {
    "bg":          "#0f172a" if DM else "#f0f4fa",
    "surface":     "#1e293b" if DM else "#ffffff",
    "surface2":    "#273449" if DM else "#f8fafc",
    "border":      "#334155" if DM else "#e2e8f0",
    "text":        "#f1f5f9" if DM else "#1e293b",
    "text2":       "#94a3b8" if DM else "#64748b",
    "text3":       "#64748b" if DM else "#94a3b8",
    "accent":      "#3b82f6",
    "input_bg":    "#0f172a" if DM else "#f8fafc",
    "thead_bg":    "#111827" if DM else "#f8fafc",
    "tbody_hover": "#1e3a5f" if DM else "#f0f7ff",
    "tbody_bdr":   "#1e293b" if DM else "#f1f5f9",
    "sync_bg":     "#1e293b" if DM else "#ffffff",
    "result_hdr":  "#1e293b" if DM else "#f8fafc",
    "sidebar_bg":  "#1e293b" if DM else "#ffffff",
    "sidebar_bdr": "#334155" if DM else "#e2e8f0",
}

# =========================================
# GLOBAL STYLE
# =========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');
*,*::before,*::after{{box-sizing:border-box}}

.stApp{{background:{T['bg']};font-family:'IBM Plex Sans',sans-serif;color:{T['text']}}}
::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-track{{background:{T['surface2']}}}
::-webkit-scrollbar-thumb{{background:{T['accent']};border-radius:3px}}

[data-testid="stSidebar"]{{background:{T['sidebar_bg']}!important;border-right:1px solid {T['sidebar_bdr']}!important}}
[data-testid="stSidebar"] > div{{padding:16px 14px!important}}

.header-wrap{{display:flex;align-items:center;gap:16px;padding:18px 24px;
    background:linear-gradient(135deg,#1d4ed8 0%,#2563eb 60%,#3b82f6 100%);
    border-radius:10px;margin-bottom:20px;position:relative;overflow:hidden;
    box-shadow:0 4px 20px rgba(37,99,235,0.3)}}
.header-wrap::after{{content:'';position:absolute;top:-25px;right:-25px;
    width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,0.07);pointer-events:none}}
.header-icon{{font-size:28px;line-height:1}}
.header-title{{font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;
    color:#fff;margin:0;line-height:1.2}}
.header-sub{{font-size:11px;color:rgba(255,255,255,0.6);margin:2px 0 0 0}}
.header-badge{{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:10px;
    color:#fff;border:1px solid rgba(255,255,255,0.3);padding:4px 10px;
    border-radius:20px;background:rgba(255,255,255,0.12);white-space:nowrap}}

.stat-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}}
.stat-card{{background:{T['surface']};border:1px solid {T['border']};border-radius:10px;
    padding:16px 18px;box-shadow:0 1px 5px rgba(0,0,0,0.08);display:flex;align-items:center;gap:14px}}
.stat-icon{{width:42px;height:42px;border-radius:9px;display:flex;align-items:center;
    justify-content:center;font-size:18px;flex-shrink:0}}
.stat-icon.blue{{background:{"#1e3a5f" if DM else "#dbeafe"}}}
.stat-icon.green{{background:{"#14532d" if DM else "#dcfce7"}}}
.stat-icon.purple{{background:{"#3b0764" if DM else "#ede9fe"}}}
.stat-label{{font-size:10px;text-transform:uppercase;letter-spacing:.8px;
    color:{T['text3']};font-family:'IBM Plex Mono',monospace;margin-bottom:2px}}
.stat-value{{font-family:'IBM Plex Mono',monospace;font-size:24px;font-weight:600;color:{T['text']};line-height:1}}
.stat-desc{{font-size:11px;color:{T['text3']};margin-top:2px}}

.panel-title{{font-family:'IBM Plex Mono',monospace;font-size:11px;text-transform:uppercase;
    letter-spacing:1px;color:{T['text2']};margin:0 0 10px 0;display:flex;align-items:center;gap:7px}}
.panel-title .bar{{display:inline-block;width:3px;height:13px;background:{T['accent']};border-radius:2px}}

div[data-testid="stForm"]{{background:transparent!important;border:none!important;padding:0!important;margin:0!important}}
.stTextInput>div>div>input{{background:{T['input_bg']}!important;border:1px solid {T['border']}!important;
    color:{T['text']}!important;border-radius:8px!important;
    font-family:'IBM Plex Mono',monospace!important;font-size:13px!important}}
.stTextInput>div>div>input:focus{{border-color:{T['accent']}!important;
    box-shadow:0 0 0 3px rgba(59,130,246,.15)!important}}
.stTextInput>label{{color:{T['text2']}!important;font-size:11px!important;
    font-family:'IBM Plex Mono',monospace!important;text-transform:uppercase!important;letter-spacing:.8px!important}}

.stButton>button,.stFormSubmitButton>button{{background:#2563eb!important;color:#fff!important;
    border:none!important;border-radius:8px!important;font-family:'IBM Plex Mono',monospace!important;
    font-size:11px!important;font-weight:600!important;letter-spacing:.4px!important;
    padding:8px 16px!important;transition:all .15s!important;box-shadow:0 2px 6px rgba(37,99,235,.25)!important}}
.stButton>button:hover,.stFormSubmitButton>button:hover{{background:#1d4ed8!important;transform:translateY(-1px)!important}}

.sync-bar{{display:flex;align-items:center;gap:9px;font-family:'IBM Plex Mono',monospace;
    font-size:11px;color:{T['text2']};margin-bottom:16px;padding:8px 14px;
    background:{T['sync_bg']};border:1px solid {T['border']};border-radius:8px}}
.sync-dot{{width:7px;height:7px;border-radius:50%;background:#22c55e;animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 2px rgba(34,197,94,.25)}}50%{{box-shadow:0 0 0 5px rgba(34,197,94,.08)}}}}

.result-header{{display:flex;align-items:center;gap:9px;padding:11px 16px;
    background:{T['result_hdr']};border:1px solid {T['border']};border-bottom:2px solid {T['accent']};
    border-radius:10px 10px 0 0;font-family:'IBM Plex Mono',monospace;
    font-size:12px;font-weight:600;color:{T['text']};margin-top:16px}}
.result-badge{{font-size:10px;background:rgba(59,130,246,0.15);color:#60a5fa;
    border:1px solid rgba(59,130,246,0.3);padding:2px 9px;border-radius:10px;font-weight:600}}
.result-card{{background:{T['surface']};border:1px solid {T['border']};border-top:none;
    border-radius:0 0 10px 10px;margin-bottom:18px;overflow:hidden}}

.success-banner{{background:{"rgba(20,83,45,0.3)" if DM else "linear-gradient(135deg,#dcfce7,#f0fdf4)"};
    border:1px solid {"#166534" if DM else "#86efac"};border-left:4px solid #22c55e;border-radius:10px;
    padding:13px 18px;margin-bottom:14px;display:flex;align-items:flex-start;gap:12px;
    animation:bannerIn .4s cubic-bezier(.34,1.56,.64,1)}}
@keyframes bannerIn{{from{{transform:translateY(-8px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
.success-icon{{font-size:20px;line-height:1;flex-shrink:0}}
.success-title{{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;color:#4ade80;margin-bottom:2px}}
.success-msg{{font-size:11px;color:{"#86efac" if DM else "#166534"}}}

.stTable,table{{width:100%!important;border-collapse:collapse!important;
    font-size:12px!important;font-family:'IBM Plex Sans',sans-serif!important}}
thead tr{{background:{T['thead_bg']}!important}}
thead th{{color:{T['text3']}!important;font-size:10px!important;text-transform:uppercase!important;
    letter-spacing:.8px!important;padding:9px 12px!important;
    border-bottom:1px solid {T['border']}!important;white-space:nowrap!important;
    font-family:'IBM Plex Mono',monospace!important}}
tbody tr{{border-bottom:1px solid {T['tbody_bdr']}!important}}
tbody tr:hover{{background:{T['tbody_hover']}!important}}
tbody td{{padding:8px 12px!important;color:{T['text']}!important;
    white-space:normal!important;word-break:break-word!important;border:none!important}}

.toast{{position:fixed;top:20px;right:20px;background:{T['surface']};
    border:1px solid #166534;border-left:4px solid #22c55e;color:{T['text']};
    padding:12px 18px;border-radius:10px;box-shadow:0 8px 28px rgba(0,0,0,.25);
    font-family:'IBM Plex Mono',monospace;font-size:11px;z-index:9999;
    animation:toastIn .35s cubic-bezier(.34,1.56,.64,1),toastOut .4s ease 4.5s forwards;min-width:240px}}
.toast-title{{font-weight:600;color:#4ade80;margin-bottom:3px}}
.toast-body{{color:{T['text2']}}}
@keyframes toastIn{{from{{transform:translateX(120%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
@keyframes toastOut{{to{{transform:translateX(120%);opacity:0}}}}

hr{{border:none;border-top:1px solid {T['border']};margin:16px 0}}

.yt-empty{{text-align:center;padding:20px 10px;color:{T['text3']};
    font-family:'IBM Plex Mono',monospace;font-size:10px;
    border:1px dashed {T['border']};border-radius:8px;
    background:{T['surface2']}}}

.sb-section-title{{font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;
    letter-spacing:1px;color:{T['text3']};margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.sb-red-bar{{display:inline-block;width:3px;height:12px;background:#ff0000;border-radius:2px}}
</style>
""", unsafe_allow_html=True)


# =========================================
# YT HELPER
# =========================================
def extract_yt_id(url):
    for p in [r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", r"^([A-Za-z0-9_-]{11})$"]:
        m = re.search(p, url.strip())
        if m:
            return m.group(1)
    return None


# =========================================
# YT PLAYER HTML — pakai YouTube IFrame API resmi
# onStateChange(0) = video ended → auto next
# Tidak ada tombol custom, kontrol dari YT sendiri
# =========================================
def build_yt_player(queue, start_idx, dark=False, floating=False):
    if not queue:
        return ""

    q_json   = json.dumps(queue)
    bg       = "#111827" if dark else "#ffffff"
    bg2      = "#0f172a" if dark else "#f8fafc"
    border   = "#1f2937" if dark else "#e2e8f0"
    text     = "#f1f5f9" if dark else "#1e293b"
    text2    = "#6b7280" if dark else "#64748b"
    text3    = "#4b5563" if dark else "#94a3b8"
    act_bg   = "#1e3a5f" if dark else "#dbeafe"
    act_c    = "#60a5fa" if dark else "#1d4ed8"
    hov_bg   = "#1f2937" if dark else "#f0f7ff"

    float_style = """
        position:fixed;bottom:22px;right:22px;width:320px;
        z-index:9998;box-shadow:0 20px 60px rgba(0,0,0,0.45);
        animation:floatIn .3s cubic-bezier(.34,1.2,.64,1);
    """ if floating else "width:100%;"

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:transparent;font-family:'IBM Plex Mono',monospace}}
@keyframes floatIn{{from{{transform:translateY(20px) scale(.97);opacity:0}}to{{transform:translateY(0) scale(1);opacity:1}}}}

.wrap{{background:{bg};border:1px solid {border};border-radius:12px;overflow:hidden;{float_style}}}
.hdr{{display:flex;align-items:center;justify-content:space-between;
    padding:9px 12px;background:{bg2};border-bottom:1px solid {border}}}
.hdr-l{{display:flex;align-items:center;gap:7px;font-size:11px;font-weight:600;color:{text}}}
.yt-badge{{background:#ff0000;color:#fff;font-size:8px;font-weight:700;padding:2px 5px;border-radius:3px}}
.counter{{font-size:10px;color:{text2}}}

/* Player container — YT iframe masuk sini via API */
#player{{width:100%;aspect-ratio:16/9;background:#000;display:block}}
#player iframe{{width:100%!important;height:100%!important}}

.queue-wrap{{max-height:160px;overflow-y:auto;background:{bg}}}
.queue-wrap::-webkit-scrollbar{{width:3px}}
.queue-wrap::-webkit-scrollbar-thumb{{background:{border};border-radius:2px}}
.qlabel{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:{text3};
    padding:7px 12px 4px;border-top:1px solid {border}}}
.qitem{{display:flex;align-items:center;gap:7px;padding:5px 12px;
    font-size:10px;color:{text2};cursor:pointer;transition:background .1s;user-select:none}}
.qitem:hover{{background:{hov_bg};color:{act_c}}}
.qitem.active{{background:{act_bg};color:{act_c};font-weight:600}}
.qnum{{width:14px;text-align:center;flex-shrink:0;color:{text3};font-size:9px}}
.qitem.active .qnum{{color:{act_c}}}
.qurl{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.play-ic{{flex-shrink:0;font-size:9px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <div class="hdr-l">
      <span class="yt-badge">YT</span>
      <span id="hdr-title">Now Playing</span>
    </div>
    <span class="counter" id="counter">— / —</span>
  </div>

  <!-- YouTube IFrame API akan inject iframe ke sini -->
  <div id="player"></div>

  <div class="queue-wrap">
    <div class="qlabel" id="qlabel">Antrian</div>
    <div id="queue-list"></div>
  </div>
</div>

<!-- Load YouTube IFrame API resmi -->
<script src="https://www.youtube.com/iframe_api"></script>
<script>
var QUEUE   = {q_json};
var current = {start_idx};
var player  = null;
var ready   = false;

// Dipanggil otomatis oleh YT API saat siap
function onYouTubeIframeAPIReady() {{
  player = new YT.Player('player', {{
    videoId: QUEUE[current],
    playerVars: {{
      autoplay: 1,
      rel: 0,
      modestbranding: 1,
      // enablejsapi otomatis aktif via IFrame API
    }},
    events: {{
      onReady:       onPlayerReady,
      onStateChange: onPlayerStateChange,
    }}
  }});
}}

function onPlayerReady(e) {{
  ready = true;
  updateUI();
  e.target.playVideo();
}}

function onPlayerStateChange(e) {{
  // YT.PlayerState.ENDED = 0
  if (e.data === YT.PlayerState.ENDED) {{
    if (current + 1 < QUEUE.length) {{
      current++;
      player.loadVideoById(QUEUE[current]);
      updateUI();
    }}
  }}
}}

function playTrack(idx) {{
  if (!ready) return;
  current = idx;
  player.loadVideoById(QUEUE[current]);
  updateUI();
}}

function updateUI() {{
  document.getElementById('counter').textContent = (current+1) + ' / ' + QUEUE.length;
  document.getElementById('qlabel').textContent  = 'Antrian — ' + QUEUE.length + ' video';

  var html = '';
  for (var i = 0; i < QUEUE.length; i++) {{
    var cls  = i === current ? 'qitem active' : 'qitem';
    var icon = i === current ? '<span class="play-ic">▶</span>' : '';
    html += '<div class="' + cls + '" onclick="playTrack(' + i + ')">'
          + '<span class="qnum">' + (i+1) + '</span>'
          + icon
          + '<span class="qurl">youtu.be/' + QUEUE[i] + '</span>'
          + '</div>';
  }}
  document.getElementById('queue-list').innerHTML = html;

  // Scroll active item ke view
  var el = document.querySelector('.qitem.active');
  if (el) el.scrollIntoView({{block:'nearest', behavior:'smooth'}});
}}

updateUI();
</script>
</body>
</html>"""


# =========================================
# SIDEBAR
# =========================================
with st.sidebar:
    # Dark / Light toggle
    dm_label = "🌙 Dark" if DM else "☀️ Light"
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                    color:{T['text2']};padding-top:7px;font-weight:600;">
            {dm_label} Mode
        </div>""", unsafe_allow_html=True)
    with c2:
        if st.button("Toggle", key="dm_toggle", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown(f"<hr style='border-top:1px solid {T['border']};margin:10px 0'>",
                unsafe_allow_html=True)

    # YT label
    st.markdown(f"""
    <div class="sb-section-title">
        <span class="sb-red-bar"></span>🎵 Media Player
    </div>""", unsafe_allow_html=True)

    # URL input + tombol tambah
    yt_url_in = st.text_input("yt_in", placeholder="Paste link YouTube...",
                               label_visibility="collapsed", key="yt_input")
    cc1, cc2 = st.columns([3, 2])
    with cc1:
        btn_add   = st.button("➕ Tambah",  key="btn_add",   use_container_width=True)
    with cc2:
        float_lbl = "✕ Float" if st.session_state.yt_float else "⧉ Float"
        btn_float = st.button(float_lbl, key="btn_float", use_container_width=True)

    if btn_add and yt_url_in.strip():
        vid = extract_yt_id(yt_url_in.strip())
        if vid:
            st.session_state.yt_queue.append(vid)
            st.session_state.yt_current = len(st.session_state.yt_queue) - 1
            st.rerun()
        else:
            st.warning("⚠️ Link tidak valid.")

    if btn_float:
        st.session_state.yt_float = not st.session_state.yt_float
        st.rerun()

    if st.session_state.yt_queue:
        if st.button("🗑 Hapus Semua", key="btn_clear_all", use_container_width=True):
            st.session_state.yt_queue   = []
            st.session_state.yt_current = 0
            st.rerun()

    q   = st.session_state.yt_queue
    idx = st.session_state.yt_current

    if not q:
        st.markdown("""
        <div class="yt-empty">
            🎵 Belum ada video<br>
            <span style="opacity:.6">tambahkan link di atas</span>
        </div>""", unsafe_allow_html=True)

    elif st.session_state.yt_float:
        # Tampilkan info floating aktif
        st.markdown(f"""
        <div style="background:{"rgba(59,130,246,0.12)" if DM else "#eff6ff"};
                    border:1px solid {"#1e3a5f" if DM else "#bfdbfe"};
                    border-radius:8px;padding:10px 12px;text-align:center;
                    font-family:'IBM Plex Mono',monospace;font-size:10px;
                    color:{"#60a5fa" if DM else "#1d4ed8"};">
            ⧉ Floating aktif<br>
            <span style="opacity:.7">{len(q)} video di antrian</span>
        </div>""", unsafe_allow_html=True)

    else:
        # Render player di sidebar
        html = build_yt_player(q, idx, dark=DM, floating=False)
        components.html(html, height=380, scrolling=False)

    st.markdown(f"<hr style='border-top:1px solid {T['border']};margin:10px 0'>",
                unsafe_allow_html=True)


# =========================================
# FLOATING PLAYER
# =========================================
if st.session_state.yt_float and st.session_state.yt_queue:
    html_float = build_yt_player(
        st.session_state.yt_queue,
        st.session_state.yt_current,
        dark=True,
        floating=True
    )
    # Render sebagai komponen fixed — height kecil, overflow visible via CSS position:fixed
    components.html(html_float, height=420, scrolling=False)


# =========================================
# MAIN — HEADER
# =========================================
st.markdown(f"""
<div class="header-wrap">
    <div class="header-icon">🏫</div>
    <div>
        <h1 class="header-title">Portal Data Sekolah</h1>
        <p class="header-sub">Sistem pencarian instalasi berbasis NPSN</p>
    </div>
    <span class="header-badge">NPSN LOOKUP v2.4</span>
</div>""", unsafe_allow_html=True)

# =========================================
# FORM LOAD DATA
# =========================================
st.markdown(f"""<div class="panel-title"><span class="bar"></span>📂 Sumber Data</div>""",
            unsafe_allow_html=True)

with st.form("sheet_form"):
    sheet_url_input = st.text_input("Link Google Spreadsheet",
        placeholder="https://docs.google.com/spreadsheets/d/...")
    load_button = st.form_submit_button("▶  Load / Refresh Data")

if load_button and sheet_url_input:
    st.session_state.refresh_token     = str(uuid.uuid4())
    st.session_state.active_sheet_url  = sheet_url_input
    st.session_state.last_refresh_time = time.time()


def build_clean_export_url(url):
    if "docs.google.com" not in url:
        return url
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    except:
        return url


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
        <span style="color:{T['accent']};font-weight:600">{pct}% cycle</span>
    </div>""", unsafe_allow_html=True)

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
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="panel-title"><span class="bar"></span>🔍 Cari Data NPSN</div>""",
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
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="success-banner">
                <div class="success-icon">✅</div>
                <div>
                    <div class="success-title">Pencarian Berhasil!</div>
                    <div class="success-msg">
                        Data NPSN <b>{base_npsn}</b> ditemukan —
                        <b>{len(hasil)} instalasi</b> tersedia.
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]
            for grp, df_grp in hasil.groupby("group"):
                st.markdown(f"""
                <div class="result-header">
                    <span>🏫 NPSN {grp}</span>
                    <span class="result-badge">{len(df_grp)} instalasi</span>
                </div>""", unsafe_allow_html=True)
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.table(df_grp.drop(columns=["group"]))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ NPSN **{base_npsn}** tidak ditemukan dalam database.")

    time.sleep(30)
    st.rerun()
