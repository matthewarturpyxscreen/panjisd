import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="Portal Data Sekolah", layout="wide")

# =========================================
# STYLE
# =========================================
st.markdown("""
<style>
.stApp { background:#f4f6f9; }

.header-box {
    background:white;
    padding:18px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

.stat-card {
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    text-align:center;
}

.result-card {
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

table {
    width:100% !important;
    table-layout:fixed !important;
}

td, th {
    white-space:normal !important;
    word-wrap:break-word !important;
    font-size:13px;
}

.toast-success {
    position: fixed;
    top: 25px;
    right: 25px;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: white;
    padding: 18px 24px;
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    font-weight: 600;
    z-index: 9999;
    animation: slideIn 0.4s ease, fadeOut 0.5s ease 4s forwards;
}

@keyframes slideIn {
    from {transform: translateX(120%); opacity:0;}
    to {transform: translateX(0); opacity:1;}
}

@keyframes fadeOut {
    to {opacity:0; transform: translateX(120%);}
}

.update-indicator {
    font-size:12px;
    color:#6b7280;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

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
# SESSION INIT
# =========================================
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = str(uuid.uuid4())

if "active_sheet_url" not in st.session_state:
    st.session_state.active_sheet_url = None

# =========================================
# FORM LOAD DATA
# =========================================
with st.form("sheet_form"):
    sheet_url_input = st.text_input("Link Spreadsheet")
    load_button = st.form_submit_button("Load / Refresh Data")

if load_button and sheet_url_input:
    st.session_state.refresh_token = str(uuid.uuid4())
    st.session_state.active_sheet_url = sheet_url_input

# =========================================
# CLEAN GOOGLE EXPORT URL BUILDER
# =========================================
def build_clean_export_url(url):

    if "docs.google.com" not in url:
        return url

    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        clean_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        return clean_url
    except:
        return url

# =========================================
# CACHE TTL 1 JAM + VERSION KEY
# =========================================
@st.cache_data(ttl=3600)
def load_all_sheets(clean_url, refresh_token):

    excel = pd.ExcelFile(clean_url)
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
# LOAD DATA
# =========================================
if st.session_state.active_sheet_url:

    clean_url = build_clean_export_url(st.session_state.active_sheet_url)

    data = load_all_sheets(
        clean_url,
        st.session_state.refresh_token
    )

    st.markdown(
        f'<div class="update-indicator">Sinkronisasi terakhir: {datetime.now().strftime("%H:%M:%S")}</div>',
        unsafe_allow_html=True
    )

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="stat-card"><h3>{len(data)}</h3><p>Total Baris Data</p></div>',unsafe_allow_html=True)

    with col2:
        total_sekolah = data["npsn"].astype(str).str.split("_").str[0].nunique()
        st.markdown(f'<div class="stat-card"><h3>{total_sekolah}</h3><p>Total Sekolah</p></div>',unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="stat-card"><h3>{data["source_sheet"].nunique()}</h3><p>Total Sheet</p></div>',unsafe_allow_html=True)

    # =========================================
    # SEARCH
    # =========================================
    npsn_input = st.text_input("Cari NPSN (Tekan Enter)", key="npsn_box")

    if npsn_input:

        base_npsn = str(npsn_input).strip().split("_")[0]

        hasil = data[
            data["npsn"]
            .astype(str)
            .str.strip()
            .str.startswith(base_npsn)
        ]

        if len(hasil)>0:

            st.markdown(f"""
            <div class="toast-success">
                ✔ NPSN {base_npsn} berhasil ditemukan
                <br>
                Total Instalasi: {len(hasil)}
            </div>
            """, unsafe_allow_html=True)

            hasil["group"] = hasil["npsn"].astype(str).str.split("_").str[0]

            for grp, df_grp in hasil.groupby("group"):
                st.markdown(f"### 🏫 Sekolah NPSN {grp} ({len(df_grp)} Instalasi)")
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.table(df_grp.drop(columns=["group"]))
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("Data tidak ditemukan")

        st.session_state.npsn_box = ""
        st.rerun()
