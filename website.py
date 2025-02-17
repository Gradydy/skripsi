import folium as fl
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from streamlit_extras.switch_page_button import switch_page

#API : OpenStreetMap

st.markdown(
    """
<style>
button {
    height: auto;
    margin-top: 28px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


if 'tabel_data' not in st.session_state:
    st.session_state.tabel_data = []
if 'vec_info' not in st.session_state:
    st.session_state.vec_info = []

m = fl.Map(location=[-6.6686773219052, 106.79101353507637], zoom_start=8)


data =  pd.read_excel("lokasi.xlsx", sheet_name="data")
#nama_lokasi = 
df = pd.DataFrame(st.session_state.tabel_data, columns = ['Provinsi','Kota','Kecamatan', 'x', 'y'])
lokasi = data[~data.isin(df).all(axis=1)]
depot = pd.read_excel("lokasi.xlsx", sheet_name="depot")
vehicle = pd.read_excel("combined_data.xlsx",sheet_name="vehicle_info")
#st.write(data)


st.title("INPUT DATA")
col1, col2 = st.columns([3,1])
with col1:
    kolom1, kolom2, kolom3 = st.columns([1,1,1])
    with kolom1:
        provinsi_pilih = st.selectbox('Provinsi', pd.unique(lokasi['Provinsi']))
    with kolom2:
        kota_pilih = st.selectbox('Kota',pd.unique(lokasi['Kota'][lokasi['Provinsi'] == provinsi_pilih]))
    with kolom3:
        kecamatan_pilih = st.selectbox('Pilih Lokasi', pd.unique(lokasi['Kecamatan'][lokasi['Kota']==kota_pilih]))
    row_pilihan = data[data["Kecamatan"] == kecamatan_pilih].iloc[0]
with col2:
    if st.button('Tambah ke Tabel',  use_container_width=True ):
        st.session_state.tabel_data.append(row_pilihan)

#if not st.session_state.tabel_data: 
df = pd.DataFrame(st.session_state.tabel_data, columns = ['Provinsi','Kota','Kecamatan', 'x', 'y'])
df = df.reset_index(drop=True)


for x in range(len(st.session_state.tabel_data)):
    corx = st.session_state.tabel_data[x]["x"]
    cory = st.session_state.tabel_data[x]['y']
    provinsi = st.session_state.tabel_data[x]['Provinsi']
    kota = st.session_state.tabel_data[x]['Kota']
    kecamatan = st.session_state.tabel_data[x]['Kecamatan']
   
    # corx = df["x"][x]
    # cory = df['y'][x]
    # name = df['nama tempat'][x]
    #st.write(df["nama tempat"][x+1], df["x"][x+1], df["y"][x+1])
    fl.Marker(location = [corx,cory], popup=kecamatan, tooltip=kecamatan).add_to(m)


st_folium(m, height=500,width=750)


if not df.empty:
    kol1, kol2 = st.columns([5,1])
    with kol1:
        delete_index = st.selectbox("Pilih Index dari data yang anda ingin hapus",df.index)
    with kol2:
        if st.button("Hapus Data", use_container_width=True):
            del st.session_state.tabel_data[delete_index]
    df = pd.DataFrame(st.session_state.tabel_data, columns = ['Provinsi','Kota','Kecamatan', 'x', 'y'])
    df = df.reset_index(drop=True)
    st.table(df)

with st.expander("Vehicle information",expanded=True):
    temp = pd.DataFrame(columns = ['lokasi','vehicle','vec_num'])
    kolum1, kolum2 = st.columns([1,1])
    with kolum1:
        awal = st.selectbox("Lokasi depot", depot)
    with kolum2:
        jenis_kendaraan = st.selectbox("Jenis Kendaraan",vehicle )
    vec_num = st.slider("Jumlah Kendaraan",0,5,3)
    temp.loc[len(df.index)] = [awal, jenis_kendaraan,vec_num]
    if st.button('Confirm',  use_container_width=True ):
        st.session_state.vec_info = temp
        st.success('Data telah disave', icon="✅")
    #st.write(st.session_state.vec_info)
    