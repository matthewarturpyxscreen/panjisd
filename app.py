import streamlit as st
import pandas as pd
import base64

# ===================================
# CONFIG
# ===================================
st.set_page_config(page_title="Portal NPSN - Stickman Interactive", layout="wide")

# ===================================
# AUTO FULL WIDTH CSS ENGINE
# ===================================
st.markdown("""
<style>
/* dataframe full width auto */
div[data-testid="stDataFrame"] div[role="table"]{
    width:max-content !important;
    font-size:13px;
}

/* kalau kolom banyak → font lebih kecil */
@media (min-width:1200px){
    div[data-testid="stDataFrame"] table{
        font-size:12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

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
# STICKMAN UI
# ===================================
st.markdown(f"""
<style>
.stApp{{background:#f4f7fb;}}
.navbar{{background:white;padding:18px 25px;border-radius:14px;
box-shadow:0 6px 25px rgba(0,0,0,0.06);margin-bottom:25px;}}
.fight-area{{display:flex;justify-content:center;gap:100px;}}
.stickman{{position:relative;width:140px;height:260px;}}
.head{{width:90px;height:90px;border-radius:50%;position:absolute;
top:0;left:25px;border:4px solid white;object-fit:cover;}}
.body{{position:absolute;top:90px;left:68px;width:4px;height:80px;background:black;}}
.pelvis{{position:absolute;top:165px;left:45px;width:50px;height:4px;background:black;}}
</style>

<div class="navbar"><h3>🎮 Stickman Interactive Mode — Portal Data Sekolah</h3></div>

<div class="fight-area">
<div class="stickman"><img src="data:image/jpeg;base64,{img1}" class="head"><div class="body"></div><div class="pelvis"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img2}" class="head"><div class="body"></div><div class="pelvis"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img3}" class="head"><div class="body"></div><div class="pelvis"></div></div>
<div class="stickman"><img src="data:image/jpeg;base64,{img4}" class="head"><div class="body"></div><div class="pelvis"></div></div>
</div>
""", unsafe_allow_html=True)

# ===================================
# INPUT
# ===================================
st.markdown("### 🔎 Pencarian")
sheet_url = st.text_input("Masukkan Link Spreadsheet")
npsn = st.text_input("Masukkan NPSN")

# ===================================
# AUTO FORMAT DETECTOR ENGINE
# ===================================
@st.cache_data(show_spinner=False)
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

        # auto rename kolom npsn
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
# RESULT + GROUP INSTALASI MODE
# ===================================
if sheet_url:

    if "all_data" not in st.session_state:
        st.session_state.all_data = load_all_sheets(sheet_url)

    data = st.session_state.all_data

    if npsn:

        base_npsn = str(npsn).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil)>0:

            st.success("🟢 DATA DITEMUKAN — AUTO FULL WIDTH MODE")

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):

                st.markdown(f"## 🏫 SEKOLAH NPSN {grp} ({len(df_grp)} Instalasi)")

                st.dataframe(
                    df_grp.drop(columns=["group"]),
                    hide_index=True
                )

        else:
            st.warning("Data tidak ditemukan")
