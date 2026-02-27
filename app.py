import streamlit as st
import pandas as pd

# ===================================
# CONFIG
# ===================================
st.set_page_config(
    page_title="Portal Data Sekolah",
    layout="wide"
)

# ===================================
# ENTERPRISE STYLE + MINI PLAYER SAFE MODE
# ===================================
st.markdown("""
<style>

.stApp{
    background:#f4f6f9;
}

/* HEADER */
.header-box{
    background:white;
    padding:18px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

/* STAT CARD */
.stat-card{
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    text-align:center;
}

/* TABLE FIT */
table {
    width: 100% !important;
    table-layout: auto !important;
    border-collapse: collapse !important;
}

th, td {
    padding: 8px !important;
    text-align: left !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    font-size: 14px !important;
}

/* ================= MINI PLAYER ================= */

#mini-player {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 380px;
    height: 240px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    overflow: hidden;
    resize: both;
    z-index: 9999;
}

#mini-header {
    background: #111827;
    color: white;
    padding: 6px 10px;
    cursor: move;
    font-size: 13px;
}

#mini-controls {
    float: right;
}

.mini-btn {
    cursor: pointer;
    margin-left: 8px;
}

#mini-circle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 70px;
    height: 70px;
    background: #111827;
    color: white;
    border-radius: 50%;
    display: none;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    z-index: 9999;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# SIDEBAR
# ===================================
with st.sidebar:
    st.title("📊 Portal Sekolah")
    st.write("Dashboard Data Sekolah")
    st.caption("Enterprise + Mini Player Mode")

# ===================================
# HEADER
# ===================================
st.markdown("""
<div class="header-box">
<h2>Dashboard Data Sekolah</h2>
<p>Sistem pencarian instalasi sekolah berbasis NPSN</p>
</div>
""", unsafe_allow_html=True)

# ===================================
# INPUT
# ===================================
colA, colB = st.columns(2)

with colA:
    sheet_url = st.text_input("Link Spreadsheet")

with colB:
    npsn = st.text_input("Cari NPSN")

st.markdown("### 🎬 Media Player")
media_link = st.text_input("Masukkan Link YouTube / Playlist")

# ===================================
# MINI PLAYER SAFE ENGINE
# ===================================
if media_link:

    embed_url = None

    if "list=" in media_link:
        playlist_id = media_link.split("list=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1"
    elif "watch?v=" in media_link:
        video_id = media_link.split("watch?v=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    elif "youtu.be/" in media_link:
        video_id = media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:
        st.markdown(f"""
        <div id="mini-player">
            <div id="mini-header">
                Media Player
                <span id="mini-controls">
                    <span class="mini-btn" onclick="minimizePlayer()">—</span>
                    <span class="mini-btn" onclick="closePlayer()">✕</span>
                </span>
            </div>
            <iframe width="100%" height="100%"
                src="{embed_url}"
                frameborder="0"
                allow="autoplay; encrypted-media"
                allowfullscreen>
            </iframe>
        </div>

        <div id="mini-circle" onclick="expandPlayer()">
            ▶
        </div>

        <script>
        dragElement(document.getElementById("mini-player"));

        function dragElement(elmnt) {{
            var pos1=0,pos2=0,pos3=0,pos4=0;
            document.getElementById("mini-header").onmousedown = dragMouseDown;

            function dragMouseDown(e) {{
                e=e||window.event;
                e.preventDefault();
                pos3=e.clientX;
                pos4=e.clientY;
                document.onmouseup=closeDragElement;
                document.onmousemove=elementDrag;
            }}

            function elementDrag(e) {{
                e=e||window.event;
                e.preventDefault();
                pos1=pos3-e.clientX;
                pos2=pos4-e.clientY;
                pos3=e.clientX;
                pos4=e.clientY;
                elmnt.style.top=(elmnt.offsetTop-pos2)+"px";
                elmnt.style.left=(elmnt.offsetLeft-pos1)+"px";
            }}

            function closeDragElement() {{
                document.onmouseup=null;
                document.onmousemove=null;
            }}
        }}

        function minimizePlayer(){{
            document.getElementById("mini-player").style.display="none";
            document.getElementById("mini-circle").style.display="flex";
        }}

        function expandPlayer(){{
            document.getElementById("mini-player").style.display="block";
            document.getElementById("mini-circle").style.display="none";
        }}

        function closePlayer(){{
            document.getElementById("mini-player").style.display="none";
            document.getElementById("mini-circle").style.display="none";
        }}
        </script>
        """, unsafe_allow_html=True)

# ===================================
# AUTO FORMAT DETECTOR (TIDAK DIUBAH)
# ===================================
@st.cache_resource
def load_all_sheets(url):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing","/export?format=xlsx")

    excel = pd.ExcelFile(url)
    semua_data=[]

    def auto_read(sheet_name):

        raw = pd.read_excel(excel, sheet_name=sheet_name, header=None)

        header_row=None
        for i in range(min(15,len(raw))):
            row_values=raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row=i
                break

        if header_row is None:
            return None

        df=raw.iloc[header_row+1:].copy()
        df.columns=(raw.iloc[header_row]
                    .astype(str)
                    .str.lower()
                    .str.strip()
                    .str.replace(" ","_"))

        for c in df.columns:
            if "npsn" in c:
                df=df.rename(columns={c:"npsn"})
                break

        if "npsn" not in df.columns:
            return None

        df["source_sheet"]=sheet_name
        return df.reset_index(drop=True)

    for sheet in excel.sheet_names:
        hasil=auto_read(sheet)
        if hasil is not None:
            semua_data.append(hasil)

    if semua_data:
        return pd.concat(semua_data, ignore_index=True)

    return pd.DataFrame()

# ===================================
# DATA LOAD
# ===================================
if sheet_url:

    data = load_all_sheets(sheet_url)

    if npsn:

        base_npsn = str(npsn).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil)>0:

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):

                st.markdown(f"### 🏫 Sekolah NPSN {grp} ({len(df_grp)} Instalasi)")

                st.table(
                    df_grp.drop(columns=["group"])
                )

        else:
            st.warning("Data tidak ditemukan")
