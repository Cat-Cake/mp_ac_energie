import os
import sys
import streamlit as st
import pandas as pd
import json
from streamlit_folium import folium_static

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from processing.transform import get_or_prepare_regional_realtime, create_charging_map
from services.service import get_data_eco2mix_regional_tr, get_data_electric_station

st.title("Analyse Énergétique Territoriale - Temps Réel")

tab1, tab2 = st.tabs(["Données temps réel", "Carte des bornes électriques"])

with tab1:
    @st.cache_data
    def load_data():
        data = get_data_eco2mix_regional_tr()
        df = get_or_prepare_regional_realtime(data)
        return df

    df = load_data()

    region = st.selectbox("Choisissez une région", df["libelle_region"].unique())
    df_region = df[df["libelle_region"] == region].copy()
    df_region["label"] = df_region["date_heure"].dt.strftime("%Y-%m-%d %H:%M")
    df_region = df_region.set_index("label")
    st.line_chart(df_region[["consommation", "production_totale"]])

with tab2:
    @st.cache_data
    def load_map_data():
        data = get_data_electric_station()
        return create_charging_map(data)

    st.markdown("Couverture nationale en bornes de recharge")
    map_obj = load_map_data()
    folium_static(map_obj)