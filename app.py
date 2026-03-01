import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import io
import requests

st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

# ─────────────────────────────────────────
# SESSION INIT
# ─────────────────────────────────────────
for k, v in {
    "refresh_token":      str(uuid.uuid4()),
    "active_url":         None,
    "dark_mode":          False,
    "cached_data":        None,
    "cached_token":       None,
    "npsn_index":         None,
    "last_search_key":    None,
    "last_search_result": None,
    "html_cache":         {},
    "load_time":          None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

DM = st.session_state.dark_mode

T = {
    "bg":       "#0f172a" if DM else "#f0f4ff",
    "surface":  "#1e293b" if DM else "#ffffff",
    "surface2": "#273449" if DM else "#eef2ff",
    "border":   "#334155" if DM else "#c7d2fe",
    "text":     "#f1f5f9" if DM else "#1e1b4b",
    "text2":    "#94a3b8" if DM else "#4338ca",
    "text3":    "#64748b" if DM else "#818cf8",
    "accent":   "#6366f1" if DM else "#4f46e5",
    "accent2":  "#818cf8" if DM else "#6366f1",
    "inp_bg":   "#0f172a" if DM else "#f8faff",
    "row_alt":  "#273449" if DM else "#f5f7ff",
    "row_hov":  "#1e3a5f" if DM else "#eef2ff",
    "th_bg":    "#111827" if DM else "#e0e7ff",
    "g1":       "#3730a3" if DM else "#4f46e5",
    "g2":       "#6366f1" if DM else "#818cf8",
    "stat_b":   "#1e3a5f" if DM else "#e0e7ff",
    "stat_g":   "#14532d" if DM else "#d1fae5",
    "stat_p":   "#3b0764" if DM else "#ede9fe",
    "sb_bg":    "#1e293b" if DM else "#ffffff",
    "sb_bdr":   "#334155" if DM else "#c7d2fe",
}

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
*{{box-sizing:border-box}}
body,.stApp{{background:{T['bg']};font-family:'Space Grotesk',sans-serif;color:{T['text']}}}
::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-thumb{{background:{T['accent']};border-radius:2px}}

[data-testid="stSidebar"]{{background:{T['sb_bg']}!important;border-right:1px solid {T['sb_bdr']}!important}}
[data-testid="stSidebar"]>div{{padding:14px 12px!important}}

.hdr{{display:flex;align-items:center;gap:14px;padding:18px 24px;
  background:linear-gradient(135deg,{T['g1']},{T['g2']});
  border-radius:14px;margin-bottom:20px;box-shadow:0 6px 24px rgba(99,102,241,.3)}}
.hdr-title{{font-size:20px;font-weight:700;color:#fff;letter-spacing:-.2px}}
.hdr-sub{{font-size:11px;color:rgba(255,255,255,.6);margin-top:2px}}
.hdr-badge{{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:10px;
  color:#fff;border:1px solid rgba(255,255,255,.3);padding:4px 10px;
  border-radius:20px;background:rgba(255,255,255,.12)}}

.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}}
.stat{{background:{T['surface']};border:1px solid {T['border']};border-radius:12px;
  padding:16px 18px;display:flex;align-items:center;gap:12px}}
.stat-ico{{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:18px;flex-shrink:0}}
.stat-ico.b{{background:{T['stat_b']}}}
.stat-ico.g{{background:{T['stat_g']}}}
.stat-ico.p{{background:{T['stat_p']}}}
.stat-lbl{{font-size:10px;text-transform:uppercase;letter-spacing:.8px;
  color:{T['text3']};font-family:'JetBrains Mono',monospace}}
.stat-val{{font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:600;color:{T['text']}}}
.stat-sub{{font-size:11px;color:{T['text3']};margin-top:1px}}

.plbl{{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;
  letter-spacing:1px;color:{T['text2']};margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.plbl-bar{{width:3px;height:12px;background:{T['accent']};border-radius:2px;display:inline-block}}

.sync{{display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;
  font-size:11px;color:{T['text2']};padding:8px 14px;margin-bottom:16px;
  background:{T['surface']};border:1px solid {T['border']};border-radius:8px}}
.sync-dot{{width:7px;height:7px;border-radius:50%;background:#10b981;
  animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 2px rgba(16,185,129,.2)}}50%{{box-shadow:0 0 0 5px rgba(16,185,129,.05)}}}}

div[data-testid="stForm"]{{background:transparent!important;border:none!important;padding:0!important}}
.stTextInput>div>div>input{{background:{T['inp_bg']}!important;border:2px solid {T['border']}!important;
  color:{T['text']}!important;border-radius:10px!important;
  font-family:'JetBrains Mono',monospace!important;font-size:13px!important;padding:10px 14px!important}}
.stTextInput>div>div>input:focus{{border-color:{T['accent']}!important;
  box-shadow:0 0 0 3px rgba(99,102,241,.15)!important}}
.stTextInput>label{{color:{T['text2']}!important;font-size:10px!important;
  font-family:'JetBrains Mono',monospace!important;text-transform:uppercase!important;letter-spacing:.8px!important}}

.stButton>button,.stFormSubmitButton>button{{
  background:linear-gradient(135deg,{T['g1']},{T['g2']})!important;
  color:#fff!important;border:none!important;border-radius:8px!important;
  font-family:'JetBrains Mono',monospace!important;font-size:11px!important;
  font-weight:600!important;padding:9px 16px!important;transition:all .15s!important;
  box-shadow:0 2px 8px rgba(99,102,241,.25)!important}}
.stButton>button:hover,.stFormSubmitButton>button:hover{{
  transform:translateY(-1px)!important;box-shadow:0 4px 14px rgba(99,102,241,.35)!important}}

.rcard{{background:{T['surface']};border:1px solid {T['border']};
  border-radius:12px;overflow:hidden;margin-bottom:16px}}
.rcard-hdr{{display:flex;align-items:center;gap:8px;padding:12px 16px;
  background:{T['surface2']};border-bottom:2px solid {T['accent']}}}
.rcard-title{{font-size:13px;font-weight:600;color:{T['text']}}}
.rcard-badge{{font-size:10px;background:rgba(99,102,241,.15);color:{T['accent2']};
  border:1px solid rgba(99,102,241,.25);padding:2px 9px;border-radius:10px;font-weight:600}}
.rcard-sheet{{margin-left:auto;font-size:10px;color:{T['text3']};font-family:'JetBrains Mono',monospace}}

.notif{{background:{"rgba(16,185,129,.12)" if DM else "#ecfdf5"};
  border:2px solid #10b981;border-radius:12px;padding:14px 18px;margin-bottom:16px;
  display:flex;align-items:center;gap:12px;
  animation:nin .35s cubic-bezier(.34,1.5,.64,1)}}
@keyframes nin{{from{{transform:translateY(-8px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
.notif-title{{font-weight:700;font-size:14px;color:{"#34d399" if DM else "#059669"}}}
.notif-detail{{font-size:11px;color:{"#6ee7b7" if DM else "#065f46"};
  font-family:'JetBrains Mono',monospace;margin-top:2px}}
.notif-badge{{margin-left:auto;background:{"rgba(16,185,129,.2)" if DM else "#a7f3d0"};
  color:{"#34d399" if DM else "#065f46"};padding:5px 12px;border-radius:16px;
  font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;white-space:nowrap}}

.nf{{background:{T['surface']};border:2px dashed {T['border']};border-radius:12px;
  padding:28px;text-align:center;color:{T['text3']}}}
.nf h4{{color:{T['text']};font-size:13px;margin-bottom:4px;font-weight:600}}
.nf p{{font-size:11px}}

.dm-wrap{{display:flex;align-items:center;justify-content:space-between;
  padding:8px 12px;background:{T['surface2']};border:1px solid {T['border']};
  border-radius:8px;margin-bottom:10px}}
.dm-lbl{{font-family:'JetBrains Mono',monospace;font-size:11px;color:{T['text2']};font-weight:600}}
hr{{border:none;border-top:1px solid {T['border']};margin:12px 0}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def export_url(url):
    if "docs.google.com" not in url:
        return url
    try:
        sid = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=xlsx"
    except Exception:
        return url


@st.cache_data(show_spinner=False)
def fetch_and_parse(clean_url, token):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    resp = requests.get(clean_url, timeout=30)
    resp.raise_for_status()
    excel = pd.ExcelFile(io.BytesIO(resp.content), engine="openpyxl")

    def read_sheet(name):
        raw = pd.read_excel(excel, sheet_name=name, header=None)
        for i in range(min(15, len(raw))):
            if any("npsn" in v for v in raw.iloc[i].astype(str).str.lower().tolist()):
                df = raw.iloc[i+1:].copy()
                df.columns = (raw.iloc[i].astype(str).str.lower()
                              .str.strip().str.replace(" ", "_"))
                for c in df.columns:
                    if "npsn" in c:
                        df = df.rename(columns={c: "npsn"})
                        break
                if "npsn" not in df.columns:
                    return None
                df["source_sheet"] = name
                return df.reset_index(drop=True)
        return None

    results = []
    with ThreadPoolExecutor(max_workers=min(8, len(excel.sheet_names))) as ex:
        for fut in as_completed({ex.submit(read_sheet, s): s for s in excel.sheet_names}):
            r = fut.result()
            if r is not None:
                results.append(r)
    if not results:
        return pd.DataFrame()
    data = pd.concat(results, ignore_index=True)
    # Hemat RAM 50-80% untuk data besar
    for col in data.select_dtypes(include="object").columns:
        try:
            data[col] = data[col].astype("category")
        except Exception:
            pass
    return data


def make_table(df, dark):
    bg      = "#1e293b" if dark else "#ffffff"
    bg2     = "#111827" if dark else "#e0e7ff"
    bdr     = "#334155" if dark else "#c7d2fe"
    txt     = "#f1f5f9" if dark else "#1e1b4b"
    th_c    = "#818cf8" if dark else "#4338ca"
    row_alt = "#273449" if dark else "#f5f7ff"
    row_hov = "#1e3a5f" if dark else "#eef2ff"
    acc     = "#6366f1" if dark else "#4f46e5"

    cols = df.columns.tolist()
    ths  = "".join(
        f'<th style="padding:8px 10px;background:{bg2};color:{th_c};font-size:10px;'
        f'font-family:JetBrains Mono,monospace;text-transform:uppercase;letter-spacing:.8px;'
        f'font-weight:600;border-bottom:2px solid {acc};white-space:nowrap;text-align:left">'
        f'{c.replace("_", " ")}</th>'
        for c in cols
    )

    records = df.fillna("").astype(str).to_dict("records")
    rows = []
    for i, r in enumerate(records):
        bg_row = bg if i % 2 == 0 else row_alt
        tds = "".join(
            f'<td style="padding:7px 10px;font-size:12px;color:{txt};'
            f'border-bottom:1px solid {bdr};word-break:break-word;'
            f'white-space:normal;vertical-align:top;max-width:180px">{v}</td>'
            for v in r.values()
        )
        rows.append(
            f'<tr style="background:{bg_row}" '
            f'onmouseover="this.style.background=\'{row_hov}\'" '
            f'onmouseout="this.style.background=\'{bg_row}\'">{tds}</tr>'
        )

    return (
        f'<div style="overflow:visible;width:100%">'
        f'<table style="width:100%;border-collapse:collapse;table-layout:fixed;background:{bg}">'
        f'<thead><tr>{ths}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        f'</table></div>'
    )


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="dm-wrap">
      <span class="dm-lbl">{"🌙 Dark" if DM else "☀️ Light"} Mode</span>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀️ Light", key="btn_light", use_container_width=True):
            st.session_state.dark_mode = False
            st.rerun()
    with c2:
        if st.button("🌙 Dark", key="btn_dark", use_container_width=True):
            st.session_state.dark_mode = True
            st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
      color:{T['text3']};line-height:1.9">
      <b style="color:{T['text2']}">Portal Data Sekolah</b><br>
      NPSN Lookup v4.0<br>
      Search cache: aktif<br>
      Update data: klik Load
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
  <div style="font-size:30px">🏫</div>
  <div>
    <div class="hdr-title">Portal Data Sekolah</div>
    <div class="hdr-sub">Pencarian instalasi berbasis NPSN — cepat &amp; akurat</div>
  </div>
  <span class="hdr-badge">NPSN LOOKUP v4.0</span>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# FORM LOAD
# ─────────────────────────────────────────
st.markdown('<div class="plbl"><span class="plbl-bar"></span>📂 Sumber Data</div>',
            unsafe_allow_html=True)

with st.form("load_form"):
    url_input = st.text_input("Link Google Spreadsheet",
                    placeholder="https://docs.google.com/spreadsheets/d/...")
    load_btn  = st.form_submit_button("▶  Load / Refresh Data")

if load_btn and url_input.strip():
    st.session_state.refresh_token      = str(uuid.uuid4())
    st.session_state.active_url         = url_input.strip()
    st.session_state.cached_token       = None
    st.session_state.last_search_key    = None
    st.session_state.last_search_result = None
    st.session_state.html_cache         = {}


# ─────────────────────────────────────────
# LOAD & DISPLAY
# ─────────────────────────────────────────
if st.session_state.active_url:
    clean = export_url(st.session_state.active_url)
    token = st.session_state.refresh_token

    if st.session_state.cached_token != token or st.session_state.cached_data is None:
        with st.spinner("⏳ Memuat data..."):
            data = fetch_and_parse(clean, token)
        st.session_state.cached_data    = data
        st.session_state.cached_token   = token
        # Build O(1) dict index
        npsn_series = data["npsn"].astype(str).str.strip()
        idx_map = {}
        for i, val in enumerate(npsn_series):
            base_k = val.split("_")[0]
            idx_map.setdefault(base_k, []).append(i)
        st.session_state.npsn_index = idx_map
        st.session_state.load_time      = datetime.now().strftime("%H:%M:%S")
        st.session_state.html_cache     = {}
    else:
        data = st.session_state.cached_data

    load_t = st.session_state.load_time or "-"
    st.markdown(f"""
    <div class="sync">
      <span class="sync-dot"></span>
      <span>DATA AKTIF &nbsp;—&nbsp; Dimuat: <b>{load_t}</b></span>
      &nbsp;|&nbsp;
      <span style="color:{T['text3']}">Klik <b>Load / Refresh</b> untuk update terbaru</span>
    </div>""", unsafe_allow_html=True)

    n_rows   = len(data)
    n_school = data["npsn"].astype(str).str.split("_").str[0].nunique()
    n_sheets = data["source_sheet"].nunique()

    st.markdown(f"""
    <div class="stats">
      <div class="stat"><div class="stat-ico b">📋</div>
        <div><div class="stat-lbl">Total Baris</div>
        <div class="stat-val">{n_rows:,}</div>
        <div class="stat-sub">semua sheet</div></div></div>
      <div class="stat"><div class="stat-ico g">🏫</div>
        <div><div class="stat-lbl">Total Sekolah</div>
        <div class="stat-val">{n_school:,}</div>
        <div class="stat-sub">unique NPSN</div></div></div>
      <div class="stat"><div class="stat-ico p">📑</div>
        <div><div class="stat-lbl">Sheet Aktif</div>
        <div class="stat-val">{n_sheets}</div>
        <div class="stat-sub">berkolom NPSN</div></div></div>
    </div>""", unsafe_allow_html=True)

    # ── SEARCH ──
    st.markdown('<div class="plbl"><span class="plbl-bar"></span>🔍 Cari Data NPSN</div>',
                unsafe_allow_html=True)
    q = st.text_input("npsn_q", placeholder="Masukkan NPSN lalu Enter...",
                      label_visibility="collapsed", key="npsn_q")

    if q:
        base = q.strip().split("_")[0]
        skey = (base, token)

        if st.session_state.last_search_key != skey:
            idx_map = st.session_state.npsn_index
            rows    = idx_map.get(base, [])
            st.session_state.last_search_result = data.iloc[rows] if rows else data.iloc[[]]
            st.session_state.last_search_key     = skey

        hasil = st.session_state.last_search_result

        if len(hasil) > 0:
            st.markdown(f"""
            <div class="notif">
              <div style="font-size:26px">✅</div>
              <div>
                <div class="notif-title">🎉 Pencarian Berhasil!</div>
                <div class="notif-detail">
                  NPSN <b>{base}</b> &nbsp;•&nbsp;
                  <b>{len(hasil)} instalasi</b> ditemukan &nbsp;•&nbsp;
                  {datetime.now().strftime("%H:%M:%S")}
                </div>
              </div>
              <div class="notif-badge">✓ {len(hasil)} Data</div>
            </div>""", unsafe_allow_html=True)

            tmp = hasil.copy()
            tmp["_grp"] = tmp["npsn"].astype(str).str.split("_").str[0]

            for grp, grp_df in tmp.groupby("_grp"):
                sheets_info = " · ".join(grp_df["source_sheet"].unique())
                display_df  = grp_df.drop(columns=["_grp"]).reset_index(drop=True)

                hkey = (grp, DM, token)
                if hkey not in st.session_state.html_cache:
                    st.session_state.html_cache[hkey] = make_table(display_df, DM)
                tbl = st.session_state.html_cache[hkey]

                st.markdown(f"""
                <div class="rcard">
                  <div class="rcard-hdr">
                    <span class="rcard-title">🏫 NPSN {grp}</span>
                    <span class="rcard-badge">{len(grp_df)} instalasi</span>
                    <span class="rcard-sheet">📄 {sheets_info}</span>
                  </div>
                  {tbl}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="nf">
              <div style="font-size:30px;margin-bottom:8px">🔍</div>
              <h4>Data Tidak Ditemukan</h4>
              <p>NPSN <b>{base}</b> tidak ada dalam database.</p>
            </div>""", unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="nf" style="padding:36px">
      <div style="font-size:30px;margin-bottom:8px">📋</div>
      <h4>Belum Ada Data</h4>
      <p>Masukkan URL Google Spreadsheet lalu klik <b>Load / Refresh Data</b>.</p>
    </div>""", unsafe_allow_html=True)
