import streamlit as st
import pandas as pd

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

# =========================================
# STYLE IMPROVED
# =========================================
st.markdown("""
<style>

.stApp {
    background:#f4f6f9;
}

/* HEADER */
.header-box {
    background:white;
    padding:18px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

/* STAT CARD */
.stat-card {
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    text-align:center;
}

/* SUCCESS POPUP */
.success-box {
    background:#e6f4ea;
    border-left:6px solid #22c55e;
    padding:15px;
    border-radius:8px;
    margin-bottom:15px;
    font-weight:500;
}

/* RESULT CARD */
.result-card {
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

/* TABLE CLEAN */
table {
    width:100% !important;
    table-layout:fixed !important;
}

td, th {
    white-space:normal !important;
    word-wrap:break-word !important;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR MEDIA PLAYER (TIDAK DIUBAH)
# =========================================
with st.sidebar:
    st.title("🎬 Media Player")
    media_link = st.text_input("Masukkan Link YouTube / Playlist")

    if media_link:
        embed_url = None

        if "list=" in media_link:
            playlist_id = media_link.split("list=")[-1].split("&")[0]
            embed_url = f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&rel=0"

        elif "watch?v=" in media_link:
            video_id = media_link.split("watch?v=")[-1].split("&")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"

        elif "youtu.be/" in media_link:
            video_id = media_link.split("youtu.be/")[-1].split("?")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"

        if embed_url:
            st.components.v1.iframe(embed_url, height=250, scrolling=False)

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="header-box">
<h2>Dashboard Data Sekolah</h2>
<p>Sistem pencarian instalasi sekolah berbasis NPSN</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# INPUT AREA DENGAN BUTTON SEARCH
# =========================================
colA, colB, colC = st.columns([3,2,1])

with colA:
    sheet_url = st.text_input("Link Spreadsheet")

with colB:
    npsn_input = st.text_input("Cari NPSN", key="npsn_box")

with colC:
    search_btn = st.button("Search")

# =========================================
# AUTO FORMAT DETECTOR (TIDAK DIUBAH)
# =========================================
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

# =========================================
# SEARCH LOGIC (TIDAK MENGUBAH FUNGSI)
# =========================================
if sheet_url:

    data = load_all_sheets(sheet_url)

    if search_btn and npsn_input:

        base_npsn = str(npsn_input).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil)>0:

            # SUCCESS POPUP
            st.markdown(
                '<div class="success-box">✅ Data berhasil ditemukan</div>',
                unsafe_allow_html=True
            )

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):

                st.markdown(f"### 🏫 Sekolah NPSN {grp} ({len(df_grp)} Instalasi)")

                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                st.table(df_grp.drop(columns=["group"]))

                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("Data tidak ditemukan")

        # AUTO CLEAR INPUT
        st.session_state.npsn_box = ""
