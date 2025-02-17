import folium as fl
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor 
import vrp
import pickle
from streamlit_extras.switch_page_button import switch_page



st.title("OUTPUT")
depot = pd.read_excel("lokasi.xlsx", sheet_name="depot")

def convert_list(data,df,):
    result = []
    router =[]
    for string in data:
        numbers = [int(num) for num in string.split(" -> ")]
        result.append(numbers)
    for x in range(len(result)):
        route =  f"Depot {only_depot['lokasi'].iloc[0]} -> "
        for num in result[x]:
            if num is not 0:
                route += f"{df['Kecamatan'][num]} -> "
        route += f"Depot {only_depot['lokasi'].iloc[0]}"
        router.append(route)

    return result, router

@st.dialog("MISSING DATA")
def warning(item):
    st.write(f"data {item} tidak ditemukan")
    if st.button("Kembali"):
        switch_page("home")

if len(st.session_state.tabel_data) == 0:
    warning("Lokasi")
elif  len(st.session_state.vec_info) ==0:
       warning("Informasi Kendaraan")
else: 
    data = pd.DataFrame(st.session_state.tabel_data, columns = ['Provinsi','Kota','Kecamatan', 'x', 'y'])
    temp = st.session_state.vec_info['lokasi']
    vec = st.session_state.vec_info['vehicle']
    vec_num = st.session_state.vec_info['vec_num']
    only_depot = depot[depot['lokasi'] == temp.iloc[0]]

    data.loc[-1] = [only_depot['lokasi'].iloc[0], only_depot['lokasi'].iloc[0], 'Depot',only_depot['x'].iloc[0],only_depot['y'].iloc[0]]
    data.index = data.index + 1
    data.sort_index(inplace=True) 
    rute, dist = vrp.main(data[['x','y']].reset_index(),int(vec_num))
    hasil,route_lokasi = convert_list(rute,data.reset_index())

    m = fl.Map(location=[data["x"].mean(), data['y'].mean()], zoom_start=11)

    color_line = ['red','orange','green','blue','violet']
    for y in range(len(hasil)):
        tempcoor = []
        for x in hasil[y]:
            corx = data["x"].iloc[x]
            cory = data['y'].iloc[x]
            provinsi = data['Provinsi'].iloc[x]
            kota = data['Kota'].iloc[x]
            kecamatan = data['Kecamatan'].iloc[x]
            campur = [corx,cory]

            fl.Marker(location = [corx,cory], popup=kecamatan, tooltip=kecamatan).add_to(m)
            tempcoor.append(campur)

        fl.PolyLine(locations=tempcoor, color=color_line[y], weight=4, opacity=1,tooltip=f"Route Of Vehicle number {y+1}").add_to(m)
    fl.CircleMarker(location = [only_depot['x'],only_depot['y']], popup=kecamatan, tooltip=kecamatan,).add_to(m)
    st_folium(m, height=500,width=750)
    pred = []
    with open('rf_bestmodel.pkl', 'rb') as f:
        model = pickle.load(f)
    for x in range(len(hasil)):
            data_pred = vrp.prep_data_pred(only_depot['lokasi'].iloc[0],vec.iloc[0],dist[x]/20,data['x'].iloc[hasil[x][len(hasil[x])-2]],data['y'].iloc[hasil[x][len(hasil[x])-2]])
            temp = model.predict(data_pred)
            pred.append(temp)

    out_cont = st.container(border=True)
    for x in range(len(pred)):
        
        #st.write(f"Vehicle {x}, {dist[x]}")
        if  dist[x] is not 0:
            out_cont = st.container(border=True)
            predicted_cost = int(pred[x][0])
            out_cont.write(f":{color_line[x]}[Vehicle {x+1}]")
            out_cont.write(f"Distance Traveled : {dist[x]/10} KM, Predicted Cost : Rp {predicted_cost}")
            out_cont.write(f"Route : {route_lokasi[x]}")


