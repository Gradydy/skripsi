import folium as fl
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium


st.title("VRP and Tripfare Prediction")

data_input = st.Page(
    page="website.py",
    title = "Data input",
    icon = "🙏",
    default=True
)

statistik_desc = st.Page(
    page="deskriptif_data.py",
    title = "Statistik Deskriptif",
    icon = "❤️",
)

output = st.Page(
    page = "output.py",
    title= "Model Output",
    icon = "👌"
)


pg = st.navigation(pages=[data_input, statistik_desc, output])
pg.run()