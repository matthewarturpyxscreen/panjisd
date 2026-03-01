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
    "bg":          "#0f172a" if DM else "#eef2ff",
    "surface":     "#1e293b" if DM else "#ffffff",
    "surface2":    "#273449" if DM else "#f0f4ff",
    "border":      "#334155" if DM else "#c7d2fe",
    "text":        "#f1f5f9" if DM else "#1e1b4b",
    "text2":       "#94a3b8" if DM else "#4338ca",
    "text3":       "#64748b" if DM else "#818cf8",
    "accent":      "#6366f1" if DM else "#4f46e5",
    "accent2":     "#818cf8" if DM else "#6366f1",
    "input_bg":    "#0f172a" if DM else "#f5f7ff",
    "thead_bg":    "#111827" if DM else "#e0e7ff",
    "tbody_hover": "#1e3a5f" if DM else "#eef2ff",
    "tbody_bdr":   "#1e293b" if DM else "#e0e7ff",
    "sync_bg":     "#1e293b" if DM else "#ffffff",
    "result_hdr":  "#1e293b" if DM else "#eef2ff",
    "sidebar_bg":  "#1e293b" if DM else "#ffffff",
    "sidebar_bdr": "#334155" if DM else "#c7d2fe",
    "stat_blue":   "#1e3a5f" if DM else "#e0e7ff",
    "stat_green":  "#14532d" if DM else "#d1fae5",
    "stat_purple": "#3b0764" if DM else "#ede9fe",
    "gradient1":   "#3730a3" if DM else "#4f46e5",
    "gradient2":   "#4f46e5" if DM else "#6366f1",
    "gradient3":   "#6366f1" if DM else "#818cf8",
}

# =========================================
# STYLE
# =========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
*,*::before,*::after{{box-sizing:border-box}}
.stApp{{background:{T['bg']};font-family:'Space Grotesk',sans-serif;color:{T['text']}}}
::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-track{{background:{T['surface2']}}}
::-webkit-scrollbar-thumb{{background:{T['accent']};border-radius:3px}}

[data-testid="stSidebar"]{{background:{T['sidebar_bg']}!important;border-right:2px solid {T['sidebar_bdr']}!important}}
[data-testid="stSidebar"]>div{{padding:16px 14px!important}}

/* HEADER */
.header-wrap{{display:flex;align-items:center;gap:16px;padding:20px 28px;
    background:linear-gradient(135deg,{T['gradient1']} 0%,{T['gradient2']} 55%,{T['gradient3']} 100%);
    border-radius:16px;margin-bottom:24px;position:relative;overflow:hidden;
    box-shadow:0 8px 32px rgba(99,102,241,0.35)}}
.header-wrap::before{{content:'';position:absolute;top:-40px;right:-40px;
    width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,0.06);pointer-events:none}}
.header-wrap::after{{content:'';position:absolute;bottom:-30px;right:80px;
    width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,0.04);pointer-events:none}}
.header-icon{{font-size:32px;line-height:1;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.2))}}
.header-title{{font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;
    color:#fff;margin:0;line-height:1.2;letter-spacing:-0.3px}}
.header-sub{{font-size:12px;color:rgba(255,255,255,0.65);margin:3px 0 0 0;font-weight:400}}
.header-badge{{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:10px;
    color:#fff;border:1px solid rgba(255,255,255,0.35);padding:5px 12px;
    border-radius:20px;background:rgba(255,255,255,0.15);white-space:nowrap;letter-spacing:.5px}}

/* STAT CARDS */
.stat-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}}
.stat-card{{background:{T['surface']};border:1px solid {T['border']};border-radius:14px;
    padding:18px 20px;box-shadow:0 2px 12px rgba(99,102,241,0.08);display:flex;align-items:center;gap:14px;
    transition:transform .15s,box-shadow .15s}}
.stat-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(99,102,241,0.15)}}
.stat-icon{{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;
    justify-content:center;font-size:20px;flex-shrink:0}}
.stat-icon.blue{{background:{T['stat_blue']}}}
.stat-icon.green{{background:{T['stat_green']}}}
.stat-icon.purple{{background:{T['stat_purple']}}}
.stat-label{{font-size:10px;text-transform:uppercase;letter-spacing:1px;
    color:{T['text3']};font-family:'JetBrains Mono',monospace;margin-bottom:3px}}
.stat-value{{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:600;color:{T['text']};line-height:1}}
.stat-desc{{font-size:11px;color:{T['text3']};margin-top:3px}}

/* PANEL TITLE */
.panel-title{{font-family:'JetBrains Mono',monospace;font-size:11px;text-transform:uppercase;
    letter-spacing:1.2px;color:{T['text2']};margin:0 0 12px 0;display:flex;align-items:center;gap:8px}}
.panel-title .bar{{display:inline-block;width:4px;height:14px;
    background:linear-gradient(180deg,{T['accent']},{T['accent2']});border-radius:2px}}

/* INPUTS */
div[data-testid="stForm"]{{background:transparent!important;border:none!important;padding:0!important;margin:0!important}}
.stTextInput>div>div>input{{background:{T['input_bg']}!important;border:2px solid {T['border']}!important;
    color:{T['text']}!important;border-radius:10px!important;
    font-family:'JetBrains Mono',monospace!important;font-size:13px!important;padding:10px 14px!important}}
.stTextInput>div>div>input:focus{{border-color:{T['accent']}!important;
    box-shadow:0 0 0 4px rgba(99,102,241,.15)!important}}
.stTextInput>label{{color:{T['text2']}!important;font-size:11px!important;
    font-family:'JetBrains Mono',monospace!important;text-transform:uppercase!important;letter-spacing:.8px!important}}

/* BUTTONS */
.stButton>button,.stFormSubmitButton>button{{
    background:linear-gradient(135deg,{T['gradient1']},{T['gradient2']})!important;
    color:#fff!important;border:none!important;border-radius:10px!important;
    font-family:'JetBrains Mono',monospace!important;font-size:11px!important;
    font-weight:600!important;letter-spacing:.4px!important;
    padding:10px 18px!important;transition:all .2s!important;
    box-shadow:0 2px 8px rgba(99,102,241,0.3)!important}}
.stButton>button:hover,.stFormSubmitButton>button:hover{{
    transform:translateY(-2px)!important;
    box-shadow:0 6px 16px rgba(99,102,241,0.4)!important}}

/* SYNC BAR */
.sync-bar{{display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono',monospace;
    font-size:11px;color:{T['text2']};margin-bottom:18px;padding:10px 16px;
    background:{T['sync_bg']};border:1px solid {T['border']};border-radius:10px;
    box-shadow:0 1px 6px rgba(99,102,241,0.06)}}
.sync-dot{{width:8px;height:8px;border-radius:50%;background:#10b981;animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 2px rgba(16,185,129,.25)}}50%{{box-shadow:0 0 0 6px rgba(16,185,129,.08)}}}}

/* RESULT */
.result-wrap{{background:{T['surface']};border:2px solid {T['border']};
    border-radius:14px;overflow:hidden;margin-bottom:20px;
    box-shadow:0 4px 20px rgba(99,102,241,0.10)}}
.result-hdr{{display:flex;align-items:center;gap:10px;padding:14px 18px;
    background:{T['result_hdr']};border-bottom:2px solid {T['accent']};}}
.result-hdr-title{{font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:600;color:{T['text']}}}
.result-badge{{font-size:10px;background:rgba(99,102,241,0.15);color:{T['accent2']};
    border:1px solid rgba(99,102,241,0.3);padding:3px 10px;border-radius:12px;font-weight:600}}
.result-sheet-info{{margin-left:auto;font-size:10px;color:{T['text3']};font-family:'JetBrains Mono',monospace}}

/* TABLE — full width, no scroll, semua baris tampil */
.stTable, [data-testid="stTable"]{{overflow:visible!important;max-height:none!important}}
.stTable table, table{{
    width:100%!important;border-collapse:collapse!important;
    font-size:13px!important;font-family:'Space Grotesk',sans-serif!important;
    table-layout:auto!important}}
thead tr{{background:{T['thead_bg']}!important}}
thead th{{color:{T['text2']}!important;font-size:10px!important;text-transform:uppercase!important;
    letter-spacing:1px!important;padding:10px 14px!important;
    border-bottom:1px solid {T['border']}!important;white-space:nowrap!important;
    font-family:'JetBrains Mono',monospace!important;font-weight:600!important}}
tbody tr{{border-bottom:1px solid {T['tbody_bdr']}!important}}
tbody tr:last-child{{border-bottom:none!important}}
tbody tr:hover{{background:{T['tbody_hover']}!important}}
tbody td{{padding:10px 14px!important;color:{T['text']}!important;
    white-space:normal!important;word-break:break-word!important;border:none!important}}

/* SUCCESS NOTIFICATION — lebih cerah & mencolok */
.success-notification{{
    background:linear-gradient(135deg,
        {"rgba(16,185,129,0.15)" if DM else "#ecfdf5"},
        {"rgba(16,185,129,0.08)" if DM else "#d1fae5"});
    border:2px solid {"#10b981" if DM else "#10b981"};
    border-radius:14px;padding:16px 20px;margin-bottom:20px;
    display:flex;align-items:center;gap:14px;
    animation:notifIn .4s cubic-bezier(.34,1.56,.64,1);
    box-shadow:0 4px 20px rgba(16,185,129,0.2)}}
@keyframes notifIn{{from{{transform:translateY(-10px) scale(.97);opacity:0}}to{{transform:translateY(0) scale(1);opacity:1}}}}
.notif-icon{{font-size:32px;line-height:1;animation:iconPop .5s cubic-bezier(.34,1.8,.64,1) .1s both}}
@keyframes iconPop{{from{{transform:scale(0);opacity:0}}to{{transform:scale(1);opacity:1}}}}
.notif-content{{flex:1}}
.notif-title{{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:700;
    color:{"#34d399" if DM else "#059669"};margin-bottom:3px}}
.notif-detail{{font-size:12px;color:{"#6ee7b7" if DM else "#065f46"};font-family:'JetBrains Mono',monospace}}
.notif-badge{{background:{"rgba(16,185,129,0.2)" if DM else "#a7f3d0"};
    color:{"#34d399" if DM else "#065f46"};padding:6px 14px;border-radius:20px;
    font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;white-space:nowrap}}

/* TOAST pojok kanan */
.toast{{position:fixed;top:24px;right:24px;background:{T['surface']};
    border:2px solid #10b981;color:{T['text']};
    padding:14px 18px;border-radius:14px;
    box-shadow:0 12px 40px rgba(16,185,129,.3);
    font-family:'JetBrains Mono',monospace;font-size:11px;z-index:9999;
    animation:toastIn .4s cubic-bezier(.34,1.56,.64,1),toastOut .4s ease 4.5s forwards;min-width:250px}}
.toast-icon{{font-size:22px;float:left;margin-right:10px;margin-top:2px}}
.toast-title{{font-weight:700;color:#10b981;margin-bottom:3px;font-size:12px}}
.toast-body{{color:{T['text2']}}}
@keyframes toastIn{{from{{transform:translateX(130%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
@keyframes toastOut{{to{{transform:translateX(130%);opacity:0}}}}

/* NOT FOUND */
.not-found{{background:{T['surface']};border:2px dashed {T['border']};border-radius:14px;
    padding:32px;text-align:center;color:{T['text3']}}}
.not-found h4{{color:{T['text']};font-size:14px;margin-bottom:6px;font-weight:600}}
.not-found p{{font-size:12px}}

hr{{border:none;border-top:1px solid {T['border']};margin:16px 0}}

/* SIDEBAR */
.sb-section-title{{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;
    letter-spacing:1px;color:{T['text3']};margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.sb-bar{{display:inline-block;width:3px;height:12px;
    background:linear-gradient(180deg,#ff4444,#ff6b6b);border-radius:2px}}
.yt-empty{{text-align:center;padding:20px 10px;color:{T['text3']};
    font-family:'JetBrains Mono',monospace;font-size:10px;
    border:2px dashed {T['border']};border-radius:10px;background:{T['surface2']};line-height:1.7}}

/* DARK MODE TOGGLE */
.dm-toggle-wrap{{display:flex;align-items:center;justify-content:space-between;
    padding:10px 14px;background:{T['surface2']};border:1px solid {T['border']};
    border-radius:10px;margin-bottom:12px}}
.dm-label{{font-family:'JetBrains Mono',monospace;font-size:11px;
    color:{T['text2']};font-weight:600}}
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
# YT PLAYER — YouTube IFrame API
# Auto-next, mute→unmute, click to skip
# =========================================
def build_yt_player(queue, start_idx, dark=False, floating=False):
    if not queue:
        return ""

    q_json = json.dumps(queue)
    bg     = "#111827" if dark else "#ffffff"
    bg2    = "#0d1117" if dark else "#eef2ff"
    bdr    = "#1f2937" if dark else "#c7d2fe"
    txt    = "#f1f5f9" if dark else "#1e1b4b"
    txt2   = "#9ca3af" if dark else "#4338ca"
    txt3   = "#4b5563" if dark else "#818cf8"
    actbg  = "#1e3a5f" if dark else "#e0e7ff"
    actc   = "#818cf8" if dark else "#4f46e5"
    hovbg  = "#1f2937" if dark else "#eef2ff"

    wrap_style = (
        "position:fixed;bottom:22px;right:22px;width:315px;"
        "z-index:9998;box-shadow:0 20px 60px rgba(0,0,0,.5);"
        "animation:floatIn .3s cubic-bezier(.34,1.2,.64,1);"
    ) if floating else "width:100%;"

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:transparent;font-family:'JetBrains Mono',monospace;overflow:hidden}}
@keyframes floatIn{{from{{transform:translateY(16px) scale(.97);opacity:0}}to{{transform:translateY(0) scale(1);opacity:1}}}}

.wrap{{background:{bg};border:2px solid {bdr};border-radius:14px;overflow:hidden;{wrap_style}}}

/* Header */
.hdr{{display:flex;align-items:center;justify-content:space-between;
    padding:9px 13px;background:{bg2};border-bottom:2px solid {bdr}}}
.hdr-l{{display:flex;align-items:center;gap:7px;font-size:11px;font-weight:600;color:{txt}}}
.yt-badge{{background:linear-gradient(135deg,#ff0000,#ff4444);color:#fff;
    font-size:8px;font-weight:700;padding:2px 6px;border-radius:4px;letter-spacing:.5px}}
.ctr{{font-size:10px;color:{txt2};font-weight:600}}

/* Controls */
.ctrl-bar{{display:flex;align-items:center;justify-content:center;gap:8px;
    padding:6px 12px;background:{bg2};border-top:1px solid {bdr}}}
.ctrl-btn{{background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);
    color:{actc};border-radius:6px;padding:4px 10px;cursor:pointer;
    font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
    transition:all .15s;display:flex;align-items:center;gap:4px}}
.ctrl-btn:hover{{background:rgba(99,102,241,0.25);transform:translateY(-1px)}}
.ctrl-btn:active{{transform:translateY(0)}}
.vol-wrap{{display:flex;align-items:center;gap:5px;margin-left:auto;font-size:9px;color:{txt3}}}
.vol-slider{{width:55px;accent-color:{actc}}}

/* YT player */
#yt-player{{width:100%;display:block;background:#000}}
#yt-player iframe{{width:100%!important;height:100%!important;display:block!important}}

/* Queue */
.q-wrap{{max-height:148px;overflow-y:auto;background:{bg}}}
.q-wrap::-webkit-scrollbar{{width:3px}}
.q-wrap::-webkit-scrollbar-thumb{{background:{bdr};border-radius:2px}}
.q-label{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:{txt3};
    padding:7px 13px 4px;border-top:1px solid {bdr};font-weight:600}}
.q-item{{display:flex;align-items:center;gap:7px;padding:6px 13px;
    font-size:10px;color:{txt2};cursor:pointer;transition:background .1s;user-select:none}}
.q-item:hover{{background:{hovbg};color:{actc}}}
.q-item.active{{background:{actbg};color:{actc};font-weight:600}}
.q-num{{width:14px;text-align:right;flex-shrink:0;font-size:9px;color:{txt3}}}
.q-item.active .q-num{{color:{actc}}}
.q-ic{{flex-shrink:0;font-size:9px;width:10px}}
.q-url{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:190px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <div class="hdr-l"><span class="yt-badge">▶ YT</span> Media Player</div>
    <span class="ctr" id="ctr">— / —</span>
  </div>

  <div id="yt-player" style="aspect-ratio:16/9"></div>

  <div class="ctrl-bar">
    <button class="ctrl-btn" onclick="prevTrack()">⏮ Prev</button>
    <button class="ctrl-btn" onclick="togglePlay()" id="btn-play">⏸ Pause</button>
    <button class="ctrl-btn" onclick="nextTrack()">Next ⏭</button>
    <div class="vol-wrap">
      🔊<input type="range" class="vol-slider" id="vol-slider" min="0" max="100" value="80"
        oninput="setVolume(this.value)">
    </div>
  </div>

  <div class="q-wrap">
    <div class="q-label" id="q-label">Queue</div>
    <div id="q-list"></div>
  </div>
</div>

<script>
var Q       = {q_json};
var cur     = {start_idx};
var player  = null;
var apiReady = false;
var isPlaying = true;

(function(){{
  var s  = document.createElement('script');
  s.src  = 'https://www.youtube.com/iframe_api';
  s.async = true;
  document.head.appendChild(s);
}})();

function onYouTubeIframeAPIReady() {{
  apiReady = true;
  player = new YT.Player('yt-player', {{
    height: '100%',
    width:  '100%',
    videoId: Q[cur],
    playerVars: {{
      autoplay:       1,
      mute:           1,
      rel:            0,
      modestbranding: 1,
      playsinline:    1,
    }},
    events: {{
      onReady: function(e) {{
        e.target.playVideo();
        updateUI();
        setTimeout(function() {{
          if (player && player.unMute) {{
            player.unMute();
            player.setVolume(80);
            isPlaying = true;
            updatePlayBtn();
          }}
        }}, 800);
      }},
      onStateChange: function(e) {{
        if (e.data === 0) {{ nextTrack(); }}
        isPlaying = (e.data === 1);
        updatePlayBtn();
      }}
    }}
  }});
}}

function nextTrack() {{
  if (!player || !apiReady) return;
  if (cur + 1 < Q.length) {{
    cur++;
    player.loadVideoById(Q[cur]);
    setTimeout(function() {{
      if (player && player.unMute) {{ player.unMute(); player.setVolume(document.getElementById('vol-slider').value); }}
    }}, 300);
    updateUI();
  }}
}}

function prevTrack() {{
  if (!player || !apiReady) return;
  if (cur > 0) {{
    cur--;
    player.loadVideoById(Q[cur]);
    setTimeout(function() {{
      if (player && player.unMute) {{ player.unMute(); player.setVolume(document.getElementById('vol-slider').value); }}
    }}, 300);
    updateUI();
  }}
}}

function togglePlay() {{
  if (!player || !apiReady) return;
  if (isPlaying) {{
    player.pauseVideo();
    isPlaying = false;
  }} else {{
    player.playVideo();
    isPlaying = true;
  }}
  updatePlayBtn();
}}

function updatePlayBtn() {{
  var btn = document.getElementById('btn-play');
  if (btn) btn.textContent = isPlaying ? '⏸ Pause' : '▶ Play';
}}

function setVolume(val) {{
  if (player && player.setVolume) {{ player.setVolume(parseInt(val)); }}
}}

function playTrack(idx) {{
  if (!player || !apiReady) return;
  cur = idx;
  player.loadVideoById(Q[cur]);
  setTimeout(function() {{
    if (player && player.unMute) {{ player.unMute(); player.setVolume(document.getElementById('vol-slider').value); }}
  }}, 300);
  isPlaying = true;
  updatePlayBtn();
  updateUI();
}}

function updateUI() {{
  document.getElementById('ctr').textContent = (cur + 1) + ' / ' + Q.length;
  document.getElementById('q-label').textContent = 'Queue — ' + Q.length + ' video';

  var html = '';
  for (var i = 0; i < Q.length; i++) {{
    var cls = i === cur ? 'q-item active' : 'q-item';
    var ic  = i === cur ? '▶' : '';
    html += '<div class="' + cls + '" onclick="playTrack(' + i + ')">'
          + '<span class="q-num">' + (i + 1) + '</span>'
          + '<span class="q-ic">' + ic + '</span>'
          + '<span class="q-url">youtu.be/' + Q[i] + '</span>'
          + '</div>';
  }}
  document.getElementById('q-list').innerHTML = html;

  var el = document.querySelector('.q-item.active');
  if (el) el.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
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
    st.markdown(f"""
    <div class="dm-toggle-wrap">
        <span class="dm-label">{"🌙 Dark Mode" if DM else "☀️ Light Mode"}</span>
    </div>""", unsafe_allow_html=True)
    
    col_dm1, col_dm2 = st.columns(2)
    with col_dm1:
        if st.button("☀️ Light", key="btn_light", use_container_width=True):
            st.session_state.dark_mode = False
            st.rerun()
    with col_dm2:
        if st.button("🌙 Dark", key="btn_dark", use_container_width=True):
            st.session_state.dark_mode = True
            st.rerun()

    st.markdown(f"<hr style='border-top:1px solid {T['border']};margin:12px 0'>", unsafe_allow_html=True)

    # Media Player title
    st.markdown(f"""
    <div class="sb-section-title"><span class="sb-bar"></span>🎵 YouTube Media Player</div>
    """, unsafe_allow_html=True)

    # URL input
    yt_in = st.text_input("yt_in", placeholder="Paste link YouTube...",
                           label_visibility="collapsed", key="yt_input")
    c1, c2 = st.columns([3, 2])
    with c1:
        btn_add = st.button("➕ Tambah", key="btn_add", use_container_width=True)
    with c2:
        btn_float = st.button(
            "✕ Float" if st.session_state.yt_float else "⧉ Float",
            key="btn_float", use_container_width=True
        )

    if btn_add and yt_in.strip():
        vid = extract_yt_id(yt_in.strip())
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
        if st.button("🗑 Hapus Semua", key="btn_clear", use_container_width=True):
            st.session_state.yt_queue   = []
            st.session_state.yt_current = 0
            st.rerun()

    q   = st.session_state.yt_queue
    idx = st.session_state.yt_current

    if not q:
        st.markdown("""<div class="yt-empty">🎵 Belum ada video<br>
        <span style="opacity:.7">Paste link YouTube di atas<br>lalu klik Tambah</span></div>""",
        unsafe_allow_html=True)
    elif st.session_state.yt_float:
        st.markdown(f"""
        <div style="background:{"rgba(99,102,241,0.12)" if DM else "#eef2ff"};
                    border:2px solid {"#1e3a5f" if DM else "#c7d2fe"};
                    border-radius:10px;padding:12px 14px;text-align:center;
                    font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:{"#818cf8" if DM else "#4f46e5"};">
            ⧉ Floating aktif &mdash; {len(q)} video dalam antrian
        </div>""", unsafe_allow_html=True)
    else:
        components.html(build_yt_player(q, idx, dark=DM, floating=False), height=460, scrolling=False)

    st.markdown(f"<hr style='border-top:1px solid {T['border']};margin:12px 0'>", unsafe_allow_html=True)


# =========================================
# FLOATING PLAYER
# =========================================
if st.session_state.yt_float and st.session_state.yt_queue:
    components.html(
        build_yt_player(st.session_state.yt_queue, st.session_state.yt_current,
                        dark=True, floating=True),
        height=460, scrolling=False
    )


# =========================================
# MAIN — HEADER
# =========================================
st.markdown(f"""
<div class="header-wrap">
  <div class="header-icon">🏫</div>
  <div>
    <h1 class="header-title">Portal Data Sekolah</h1>
    <p class="header-sub">Sistem pencarian instalasi berbasis NPSN — Realtime & Akurat</p>
  </div>
  <span class="header-badge">NPSN LOOKUP v3.0</span>
</div>""", unsafe_allow_html=True)


# =========================================
# FORM LOAD DATA
# =========================================
st.markdown(f"""<div class="panel-title"><span class="bar"></span>📂 Sumber Data Google Spreadsheet</div>""",
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
        df = raw.iloc[header_row + 1:].copy()
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
        <span>LIVE — Sinkronisasi: <b>{now_str}</b></span>
        &nbsp;|&nbsp;
        <span>Refresh: <b>{sisa//60:02d}:{sisa%60:02d}</b></span>
        &nbsp;|&nbsp;
        <span style="color:{T['accent']};font-weight:700">{pct}%</span>
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
            <div class="stat-desc">semua sheet</div></div>
        </div>
        <div class="stat-card">
            <div class="stat-icon green">🏫</div>
            <div><div class="stat-label">Total Sekolah</div>
            <div class="stat-value">{total_sekolah:,}</div>
            <div class="stat-desc">unique NPSN</div></div>
        </div>
        <div class="stat-card">
            <div class="stat-icon purple">📑</div>
            <div><div class="stat-label">Sheet Aktif</div>
            <div class="stat-value">{total_sheets}</div>
            <div class="stat-desc">berkolom NPSN</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # =========================================
    # HELPER — render DataFrame sebagai HTML tabel
    # NO horizontal scroll, teks wrap, semua kolom muat
    # =========================================
    def df_to_html(df: pd.DataFrame, dark: bool) -> str:
        bg       = "#1e293b"   if dark else "#ffffff"
        bg2      = "#111827"   if dark else "#e0e7ff"
        bdr      = "#334155"   if dark else "#c7d2fe"
        txt      = "#f1f5f9"   if dark else "#1e1b4b"
        txt_hdr  = "#818cf8"   if dark else "#4338ca"
        row_alt  = "#273449"   if dark else "#f5f7ff"
        row_hov  = "#1e3a5f"   if dark else "#eef2ff"
        acc      = "#6366f1"   if dark else "#4f46e5"

        # build header
        cols = df.columns.tolist()
        ths  = "".join(
            f'<th style="padding:9px 11px;background:{bg2};color:{txt_hdr};'
            f'font-size:10px;font-family:JetBrains Mono,monospace;text-transform:uppercase;'
            f'letter-spacing:.9px;font-weight:600;border-bottom:2px solid {acc};'
            f'white-space:nowrap;text-align:left">{c.replace("_"," ")}</th>'
            for c in cols
        )

        # build rows
        rows_html = ""
        for i, (_, row) in enumerate(df.iterrows()):
            bg_row = bg if i % 2 == 0 else row_alt
            tds = "".join(
                f'<td style="padding:8px 11px;color:{txt};font-size:12px;'
                f'font-family:Space Grotesk,sans-serif;border-bottom:1px solid {bdr};'
                f'word-break:break-word;white-space:normal;vertical-align:top;'
                f'max-width:200px">{str(v) if pd.notna(v) else ""}</td>'
                for v in row
            )
            rows_html += (
                f'<tr style="background:{bg_row}" '
                f'onmouseover="this.style.background=\'{row_hov}\'" '
                f'onmouseout="this.style.background=\'{bg_row}\'">{tds}</tr>'
            )

        return f"""
        <div style="overflow:visible;width:100%">
        <table style="width:100%;border-collapse:collapse;table-layout:fixed;
                      background:{bg};border-radius:0 0 12px 12px;overflow:hidden">
          <colgroup>{"<col>" * len(cols)}</colgroup>
          <thead><tr>{ths}</tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>"""

    # ---- SEARCH ----
    st.markdown(f"""<div class="panel-title"><span class="bar"></span>🔍 Cari Data NPSN</div>""",
                unsafe_allow_html=True)

    npsn_input = st.text_input("Cari NPSN",
        placeholder="Masukkan NPSN lalu tekan Enter...",
        key="npsn_box", label_visibility="collapsed")

    if npsn_input:
        base_npsn = str(npsn_input).strip().split("_")[0]
        hasil = data[data["npsn"].astype(str).str.strip().str.startswith(base_npsn)]

        if len(hasil) > 0:
            # === TOAST pojok kanan ===
            st.markdown(f"""
            <div class="toast">
                <div class="toast-icon">✅</div>
                <div class="toast-title">Data Ditemukan!</div>
                <div class="toast-body">NPSN <b>{base_npsn}</b> — {len(hasil)} instalasi berhasil dimuat</div>
            </div>""", unsafe_allow_html=True)

            # === NOTIFIKASI INLINE BESAR ===
            st.markdown(f"""
            <div class="success-notification">
                <div class="notif-icon">✅</div>
                <div class="notif-content">
                    <div class="notif-title">🎉 Pencarian Berhasil!</div>
                    <div class="notif-detail">
                        NPSN <b>{base_npsn}</b> ditemukan &nbsp;•&nbsp;
                        <b>{len(hasil)} instalasi</b> tersedia &nbsp;•&nbsp;
                        {datetime.now().strftime("%H:%M:%S")}
                    </div>
                </div>
                <div class="notif-badge">✓ {len(hasil)} Data</div>
            </div>""", unsafe_allow_html=True)

            hasil = hasil.copy()
            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):
                sheets_info = " · ".join(df_grp["source_sheet"].unique())
                df_display  = df_grp.drop(columns=["group"]).reset_index(drop=True)

                # Header card
                st.markdown(f"""
                <div class="result-wrap">
                    <div class="result-hdr">
                        <span class="result-hdr-title">🏫 NPSN {grp}</span>
                        <span class="result-badge">{len(df_grp)} instalasi</span>
                        <span class="result-sheet-info">📄 {sheets_info}</span>
                    </div>
                    {df_to_html(df_display, DM)}
                </div>""", unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="not-found">
                <div style="font-size:36px;margin-bottom:10px">🔍</div>
                <h4>Data Tidak Ditemukan</h4>
                <p>NPSN <b>{base_npsn}</b> tidak ada dalam database saat ini.<br>
                Periksa kembali nomor NPSN yang dimasukkan.</p>
            </div>""", unsafe_allow_html=True)

    # Auto-refresh hanya saat interval sudah habis
    if elapsed >= REFRESH_INTERVAL - 1:
        st.rerun()

else:
    st.markdown(f"""
    <div class="not-found" style="padding:40px">
        <div style="font-size:36px;margin-bottom:10px">📋</div>
        <h4>Belum Ada Data</h4>
        <p>Masukkan URL Google Spreadsheet di atas lalu klik <b>Load / Refresh Data</b>.</p>
    </div>""", unsafe_allow_html=True)
