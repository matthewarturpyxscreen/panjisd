import streamlit as st
import pandas as pd
import base64

# ===================================
# CONFIG
# ===================================
st.set_page_config(page_title="Portal NPSN - Stickman Interactive", layout="wide")

# ===================================
# LOAD FOTO
# ===================================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = img_to_base64("foto1.jpg")
img2 = img_to_base64("foto2.jpg")
img3 = img_to_base64("foto3.jpg")
img4 = img_to_base64("foto4.jpg")

# ===================================
# CSS + STICKMAN
# ===================================
st.markdown(f"""
<style>
.stApp{{background:#f4f7fb;}}

.navbar{{
background:white;padding:18px 25px;border-radius:14px;
box-shadow:0 6px 25px rgba(0,0,0,0.06);margin-bottom:25px;}}

.fight-area{{display:flex;justify-content:center;gap:100px;}}

.stickman{{position:relative;width:140px;height:260px;
animation:bodyMove 0.5s infinite alternate ease-in-out;}}

.head{{width:90px;height:90px;border-radius:50%;position:absolute;
top:0;left:25px;border:4px solid white;object-fit:cover;
box-shadow:0 6px 18px rgba(0,0,0,0.25);
animation:headBounce 0.5s infinite alternate;}}

.body{{position:absolute;top:90px;left:68px;width:4px;height:80px;background:black;}}
.pelvis{{position:absolute;top:165px;left:45px;width:50px;height:4px;background:black;}}

.arm-left{{position:absolute;width:70px;height:4px;background:black;
top:110px;left:-5px;transform-origin:right;
animation:punchLeft 0.4s infinite alternate;}}

.arm-right{{position:absolute;width:70px;height:4px;background:black;
top:110px;left:75px;transform-origin:left;
animation:punchRight 0.4s infinite alternate;}}

.leg-left{{position:absolute;width:70px;height:4px;background:black;
top:180px;left:10px;transform-origin:right;
animation:kickLeft 0.6s infinite alternate;}}

.leg-right{{position:absolute;width:70px;height:4px;background:black;
top:180px;left:60px;transform-origin:left;
animation:kickRight 0.6s infinite alternate;}}

.priorityGlow .head{{ box-shadow:0 0 25px #22c55e; }}
.backupGlow .head{{ box-shadow:0 0 25px #3b82f6; }}

@keyframes bodyMove{{0%{{transform:translateY(0)}}100%{{transform:translateY(-10px)}}}}
@keyframes headBounce{{0%{{transform:translateY(0)}}100%{{transform:translateY(-12px)}}}}
@keyframes punchLeft{{0%{{transform:rotate(-15deg)}}100%{{transform:rotate(60deg)}}}}
@keyframes punchRight{{0%{{transform:rotate(15deg)}}100%{{transform:rotate(-60deg)}}}}
@keyframes kickLeft{{0%{{transform:rotate(10deg)}}100%{{transform:rotate(-45deg)}}}}
@keyframes kickRight{{0%{{transform:rotate(-10deg)}}100%{{transform:rotate(45deg)}}}}
</style>

<div class="navbar">
<h3>🎮 Stickman Interactive Mode — Portal Data Sekolah</h3>
</div>

<div class="fight-area">
<div class="stickman"><img src="data:image/jpeg;base64,{img1}" class="head"><div class="body"></div><div class="pelvis"></div><div class="arm-left"></div><div class="arm-right"></div><div class="leg-left"></div><div class="leg-right"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img2}" class="head"><div class="body"></div><div class="pelvis"></div><div class="arm-left"></div><div class="arm-right"></div><div class="leg-left"></div><div class="leg-right"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img3}" class="head"><div class="body"></div><div class="pelvis"></div><div class="arm-left"></div><div class="arm-right"></div><div class="leg-left"></div><div class="leg-right"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img4}" class="head"><div class="body"></div><div class="pelvis"></div><div class="arm-left"></div><div class="arm-right"></div><div class="leg-left"></div><div class="leg-right"></div></div>
</div>
""", unsafe_allow_html=True)

# ===================================
# PLAYER
# ===================================
st.markdown("### 🎧 Player")
media_link = st.text_input("Masukkan Link YouTube")

if media_link:
    embed_url=None
    if "list=" in media_link:
        playlist_id=media_link.split("list=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1"
    elif "watch?v=" in media_link:
        video_id=media_link.split("watch?v=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    elif "youtu.be/" in media_link:
        video_id=media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:
        st.components.v1.iframe(embed_url,height=520)

# ===================================
# INPUT
# ===================================
st.markdown("### 🔎 Pencarian")

c1,c2,c3 = st.columns([1,2,1])
with c2:
    sheet_url = st.text_input("Masukkan Link Spreadsheet")
    npsn = st.text_input("Masukkan NPSN")

# ===================================
# AUTO FORMAT DETECTOR ENGINE
# ===================================
@st.cache_data(show_spinner=False)
def load_priority_data(url):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing","/export?format=xlsx")

    excel = pd.ExcelFile(url)

    PRIORITY_SHEET="PAKE DATA INI UDAH KE UPDATE!!!"
    BACKUP_SHEET="18/2/2026"

    data={}

    # ========= AUTO HEADER DETECTOR =========
    def auto_read(sheet_name):

        raw = pd.read_excel(excel, sheet_name=sheet_name, header=None)

        header_row=None

        for i in range(min(15,len(raw))):
            row_values = raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row=i
                break

        if header_row is not None:
            df=raw.iloc[header_row+1:].copy()
            df.columns=(raw.iloc[header_row]
                        .astype(str)
                        .str.lower()
                        .str.strip()
                        .str.replace(" ","_"))
        else:
            df=raw.copy()
            df.columns=[f"kolom_{i}" for i in range(len(df.columns))]

        # ===== AUTO DETECT KOLOM NPSN =====
        for c in df.columns:
            if "npsn" in c:
                df=df.rename(columns={c:"npsn"})
                break

        df["source_sheet"]=sheet_name
        df=df.loc[:,~df.columns.duplicated()]

        return df.reset_index(drop=True)

    if PRIORITY_SHEET in excel.sheet_names:
        data["priority"]=auto_read(PRIORITY_SHEET)

    if BACKUP_SHEET in excel.sheet_names:
        data["backup"]=auto_read(BACKUP_SHEET)

    return data

# ===================================
# RESULT
# ===================================
if sheet_url:

    if "priority_data" not in st.session_state:
        st.session_state.priority_data = load_priority_data(sheet_url)

    data = st.session_state.priority_data

    if npsn:

        hasil=None
        source=None

        if "priority" in data and "npsn" in data["priority"].columns:
            temp=data["priority"][data["priority"]["npsn"].astype(str).str.strip()==str(npsn).strip()]
            if len(temp)>0:
                hasil=temp
                source="priority"

        if hasil is None and "backup" in data and "npsn" in data["backup"].columns:
            temp=data["backup"][data["backup"]["npsn"].astype(str).str.strip()==str(npsn).strip()]
            if len(temp)>0:
                hasil=temp
                source="backup"

        if hasil is not None:

            if source=="priority":
                st.success("🟢 DATA UTAMA — Stickman Mode Aktif")

            if source=="backup":
                st.info("🔵 DATA BACKUP — Stickman Mode Aktif")

            st.dataframe(hasil,use_container_width=True,hide_index=True)

        else:
            st.warning("Data tidak ditemukan")
