import folium as fl
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor 
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page

@st.dialog("MISSING DATA")
def warning(item):
    st.write(f"data {item} tidak ditemukan")
    if st.button("Kembali"):
        switch_page("home")


st.title("STATISTIK DESKRIPTIF")
pilihan = []
depot = pd.read_excel("lokasi.xlsx", sheet_name="depot")
test = pd.read_csv("combined_data_real.csv",sep = ";")
kolom = test.columns
kolom1, kolom2 = st.columns([4,1])
with kolom1 :
    df = st.file_uploader('Upload CSV dengan separator ";"')
    if df:
        df = pd.read_csv(df, delimiter=";")
        if sorted(kolom) == sorted(df.columns):
            pilihan =True
        else:
            st.markdown("Data yang diberikan salah Mohon berikan data dengan format yang sudah ditentukan")
with kolom2 :
    st.markdown('<style>button[kind="primary"] { margin-top: 12px;height:78px}</style>', unsafe_allow_html=True,)
    if st.button("Gunakan data pada page input data", type="primary"):
        pilihan =False
if pilihan == []:
    st.markdown("Upload CSV yang memiliki nama kolom sebagai berikut :")
    st.table(kolom)


if pilihan == True:
        count = df["vehicle_type"].value_counts()
        coor = df[["coor_x","coor_y"]]
        count2 = df["origin_location"].value_counts()
        #fig = plt.pie(count)
        kol1, kol2 = st.columns([1,1])
        with kol1 :
            bar_vehicle = px.bar(
                count,
                x = count,
                y = count.keys(),
                orientation='h',
                title="Histogram Jenis Vehicle",
            )
            st.plotly_chart(bar_vehicle)
            b = f"<p style='font-size:13px;text-align: center;'>chart di atas menunjukan sebaran dari jenis kendaraan dalam data yang diberikan</p>"
            st.markdown(b,unsafe_allow_html=True)
        with kol2 :
            pie = px.pie(
                count2,
                values= count2,
                names= count2.keys(),
                title="Pie Chart Lokasi Depot"
            )
            st.plotly_chart(pie)
            p = f"<p style='font-size:13px;text-align: center;'>chart di atas menunjukan sebaran dari Lokasi Penjemputan barang dalam data yang diberikan</p>"
            st.markdown(p,unsafe_allow_html=True)
        scat = px.scatter(
            coor,
            x = "coor_x",
            y = "coor_y",
            title="Sebaran koordinat pengantaran",
        )
        st.plotly_chart(scat)
        s = f"<p style='font-size:13px;text-align: center;'>Titik dalam scatterplot dibawah merepresentasikan tujuan pengiriman barang</p>"
        st.markdown(s,unsafe_allow_html=True)
if pilihan == False:
    if len(st.session_state.tabel_data) == 0:
        warning("Lokasi")
    else :
        df = pd.DataFrame(st.session_state.tabel_data, columns = ['Provinsi','Kota','Kecamatan', 'x', 'y'])
        count = df["Provinsi"].value_counts()
        coor = df[["x","y"]]
        count2 = df["Kota"].value_counts()
        kol1, kol2 = st.columns([1,1])
        with kol1 :
            pie = px.pie(
                count,
                values= count,
                names= count.keys(),
                title="Sebaran Provinsi Pie Chart"
            )
            st.plotly_chart(pie)
            p = f"<p style='font-size:13px;text-align: center;'>chart di atas menunjukan sebaran dari Provinsi  Lokasi pengirimiman barang dalam data input</p>"
            st.markdown(p,unsafe_allow_html=True)
        with kol2 :
            bar_vehicle = px.bar(
                count,
                x = count2,
                y = count2.keys(),
                orientation='h',
                title="Histogram sebaran Kota",
            )
            st.plotly_chart(bar_vehicle)
            h = f"<p style='font-size:13px;text-align: center;'>histogram di atas menunjukan sebaran dari Kota Lokasi pengirimiman barang dalam data input</p>"
            st.markdown(h,unsafe_allow_html=True)
        scat = px.scatter(
            coor,
            x = "x",
            y = "y",
            title="Sebaran koordinat pengantaran",
        )
        st.plotly_chart(scat)  
        s = f"<p style='font-size:13px;text-align: center;'>Titik dalam scatterplot dibawah merepresentasikan tujuan pengiriman barang</p>"
        st.markdown(s,unsafe_allow_html=True)   