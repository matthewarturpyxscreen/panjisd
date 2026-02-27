import streamlit as st
import pandas as pd

# ===================================
# CONFIG ENTERPRISE DASHBOARD
# ===================================
st.set_page_config(
    page_title="Portal Data Sekolah",
    layout="wide"
)

# ===================================
# STYLE ENTERPRISE
# ===================================
st.markdown("""
<style>

.stApp{
    background:#f4f6f9;
}

.header-box{
    background:white;
    padding:18px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

.stat-card{
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# SIDEBAR (TAMPILAN ENTERPRISE)
# ===================================
with st.sidebar:
    st.title("📊 Portal Sekolah")
    st.markdown("---")
    st.write("Dashboard Data Sekolah")
    st.write("Pencarian berdasarkan NPSN")
    st.markdown("---")
    st.caption("Enterprise Dashboard Mode")

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
# INPUT AREA
# ===================================
colA, colB = st.columns(2)

with colA:
    sheet_url = st.text_input("Link Spreadsheet")

with colB:
    npsn = st.text_input("Cari NPSN")

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
# LOAD DATA GLOBAL (TURBO ENGINE)
# ===================================
if sheet_url:

    data = load_all_sheets(sheet_url)

    # ===================================
    # STAT CARD ENTERPRISE (TIDAK MENGUBAH FUNGSI)
    # ===================================
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="stat-card"><h3>{len(data)}</h3><p>Total Baris Data</p></div>',unsafe_allow_html=True)

    with col2:
        total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
        st.markdown(f'<div class="stat-card"><h3>{total_sekolah}</h3><p>Total Sekolah</p></div>',unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="stat-card"><h3>{data["source_sheet"].nunique()}</h3><p>Total Sheet</p></div>',unsafe_allow_html=True)

    # ===================================
    # SEARCH RESULT (FUNGSI ASLI TETAP)
    # ===================================
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
