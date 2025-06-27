import os
import sys
import streamlit as st
import pandas as pd

from streamlit_folium import folium_static
from st_aggrid import GridOptionsBuilder

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from processing.transform import prepare_production_region_sector, \
    prepare_commercial_exchange, prepare_ecogas_mix, prepare_ecowatt_national_alerts
from processing.map_generator import create_dominant_filiere_map
from processing.loaders import (
    load_data,
    load_map_data,
    load_national_data,
    load_region_main_sector_data,
    load_commercial_exchange_2024_data,
    load_ecogas_data,
    load_gas_emission_data,
    load_ecowatt_national_alerts
)

st.set_page_config(
    layout="wide",
    page_title="Analyse énergétique territoriale",
)

st.title("Analyse Énergétique Territoriale")

tab1, tab2, tab3, tab4 = st.tabs(["Données temps réel", "Cartes", "Données 2024", "Environnement"])

with (tab1):
    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Actualiser les données"):
            st.toast("Cache vidé, rechargement…")
            st.cache_data.clear()
            st.rerun()

    with st.status("Chargement des données…", expanded=True) as status:
        st.write("Chargement des données régionales... 1/8")
        df = load_data()

        st.write("Chargement des bornes électriques... 2/8")
        map_obj = load_map_data()

        st.write("Chargement de la production nationale... 3/8")
        national_data = load_national_data()

        st.write("Chargement des productions régionales... 4/8")
        data2 = load_region_main_sector_data()

        st.write("Chargement des échanges commerciaux... 5/8")
        data_commercial = load_commercial_exchange_2024_data()

        st.write("Chargement des signaux Ecogaz... 6/8")
        data_ecogas = load_ecogas_data()

        st.write("Chargement des gaz à effet de serre... 7/8")
        data_gas_emissions = load_gas_emission_data()

        st.write("Chargement des données écoWatt... 8/8")
        data_ecowatt_national = load_ecowatt_national_alerts()

        status.update(label="Toutes les données sont chargées", state="complete")

    region = st.selectbox("Choisissez une région", df["libelle_region"].unique())
    df_region = df[df["libelle_region"] == region].copy()
    df_region["label"] = df_region["date_heure"].dt.strftime("%Y-%m-%d %H:%M")
    df_region = df_region.set_index("label")
    st.line_chart(df_region[["consommation", "production_totale"]])

    df_ecogas = prepare_ecogas_mix(data_ecogas)

    df_2025 = df_ecogas[df_ecogas["gas_day"].dt.year == 2025]
    color_counts = df_2025["color"].value_counts().reset_index()
    color_counts.columns = ["Niveau Ecogaz", "Nombre de jours"]

    st.subheader("Répartition des niveaux Ecogaz sur 2025")
    st.info("""
    **Légende des niveaux Ecogaz** :

    - **Green** : La situation est normale, les réserves de gaz sont suffisantes.  
    - **Yellow** : Situation sous surveillance, incitation à réduire la consommation.  
    - **Orange** : Tension forte sur l’approvisionnement, recommandations de sobriété renforcées.  
    - **Red** : Niveau critique, risque de coupure, mesures exceptionnelles possibles.
    """)
    st.dataframe(color_counts)
    st.bar_chart(data=color_counts.set_index("Niveau Ecogaz"))

    df_alertes = data_ecowatt_national
    st.subheader("Alertes EcoWatt France – par jour")
    st.info("""
    Seules les heures avec un signal **orange (3)** ou **rouge (4)** sont comptabilisées.  
    Chaque point correspond au **nombre d’heures critiques dans la journée**.
    """)
    st.line_chart(data=df_alertes.set_index("date")[["nb_alertes_jour"]])

    df2 = prepare_production_region_sector(data2)

with tab2:
    st.markdown("Couverture nationale en bornes de recharge")
    folium_static(map_obj)

    st.subheader("Filière dominante par région 2024")
    geo_path = "data/regions.geojson"
    map_obj = create_dominant_filiere_map(df2, geo_path)
    folium_static(map_obj)

with tab3:
    df_exchange = prepare_commercial_exchange(data_commercial)
    df_2024 = df_exchange[df_exchange["date"].dt.year == 2024]

    st.subheader("Balance commerciale France - Électricité (2024)")
    if not df_2024.empty:
        total_export = df_2024["total_export"].sum()
        total_import = df_2024["total_import"].sum()
        balance_nette = total_export - total_import

        col1, col2, col3 = st.columns(3)
        col1.metric("Export (MWh)", f"{total_export:,.0f}")
        col2.metric("Import (MWh)", f"{abs(total_import):,.0f}")
        col3.metric("Balance nette", f"{balance_nette:,.0f} MWh")
    else:
        st.warning("Données non disponibles")

    df_national = pd.DataFrame(national_data)

    st.subheader("Production nationale annuelle par filièree 2013-2024")
    st.dataframe(df_national, use_container_width=True)
    grid_options = GridOptionsBuilder.from_dataframe(df_national).build()

    df2["production_solaire"] = pd.to_numeric(df2["production_solaire"], errors="coerce")

    top_solaire = (
        df2[df2["annee"] == df2["annee"].max()]
        .sort_values(by="production_solaire", ascending=False)
        .head(5)[["region", "production_solaire"]]
    )

    st.subheader("Top 5 régions productrices en solaire (2024)")
    top_solaire = top_solaire.set_index("region")
    st.bar_chart(top_solaire, use_container_width=True)
with (tab4):
    df_gas_emissions = pd.DataFrame(data_gas_emissions)

    st.subheader("Bilan d'émissions de gaz à effet de serre par scope et opérateur")
    grid_options = GridOptionsBuilder.from_dataframe(df_gas_emissions).build()
    st.info("""
    **Scope 1** : Émissions directes de GES (gaz à effet de serre) issues des sources contrôlées par l'opérateur.  
    **Scope 2** : Émissions indirectes de gaz à effet de serre (GES) liées à l’achat et à la consommation d’énergie par l’opérateur pour ses activités, notamment l’électricité, la chaleur ou la vapeur.
    """)
    df_gas_emissions = df_gas_emissions.drop(columns=["edition"], errors="ignore")
    df_gas_emissions = df_gas_emissions.rename(columns={
        "annee": "Année",
        "operateur": "Opérateur",
        "scope_1_en_kt_eq_co2": "Scope 1 (kt CO2e)",
        "scope_2_en_kt_eq_co2": "Scope 2 (kt CO2e)",
        "total_scope_1_et_2_en_kt_eq_co2": "Total (Scopes 1+2) (kt CO2e)"
    })
    st.dataframe(df_gas_emissions, use_container_width=True)