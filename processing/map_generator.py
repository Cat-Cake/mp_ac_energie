import folium
import pandas as pd
import json

from folium.plugins import MarkerCluster


def create_charging_map(data):
    df = pd.DataFrame(data)

    df = df[df["geo_point_borne"].notna()]
    df["latitude"] = df["geo_point_borne"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df["longitude"] = df["geo_point_borne"].apply(lambda x: x.get("lon") if isinstance(x, dict) else None)
    df = df.dropna(subset=["latitude", "longitude"])

    m = folium.Map(location=[46.6, 2.4], zoom_start=6)

    marker_cluster = MarkerCluster().add_to(m)

    for index, row in df.iterrows():
        popup_content = f"""
        <b>Station :</b> {row.get("n_station", "Inconnue")}<br>
        <b>Adresse :</b> {row.get("ad_station", "Non renseignée")}<br>
        <b>Puissance max :</b> {row.get("puiss_max", "N/A")} kW<br>
        <b>Prises :</b> {row.get("type_prise", "N/A")}
        """
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color="green", icon="bolt", prefix="fa")
        ).add_to(marker_cluster)

    return m


def create_dominant_filiere_map(df, geojson_path):
    latest_year = df["annee"].max()
    df_latest = df[df["annee"] == latest_year].copy()

    filieres = [
        "production_thermique",
        "production_nucleaire",
        "production_eolienne",
        "production_solaire",
        "production_hydraulique",
        "production_bioenergies"
    ]

    df_latest["filiere_dominante"] = df_latest[filieres].idxmax(axis=1)
    df_latest["valeur_max"] = df_latest[filieres].max(axis=1)

    filiere_codes = {
        "production_thermique": 1,
        "production_nucleaire": 2,
        "production_eolienne": 3,
        "production_solaire": 4,
        "production_hydraulique": 5,
        "production_bioenergies": 6
    }
    df_latest["filiere_code"] = df_latest["filiere_dominante"].map(filiere_codes)

    with open(geojson_path) as f:
        geojson = json.load(f)

    m = folium.Map(location=[46.6, 2.4], zoom_start=6)

    folium.Choropleth(
        geo_data=geojson,
        name="choropleth",
        data=df_latest,
        columns=["region", "filiere_code"],
        key_on="feature.properties.nom",
        fill_color="Set2",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Filière dominante (voir popup)",
        highlight=True,
    ).add_to(m)

    for _, row in df_latest.iterrows():
        lat = row.get("lat")
        lon = row.get("lon")
        if pd.notna(lat) and pd.notna(lon):
            popup_html = (
                f"<b>{row['region']}</b><br>"
                f"Filière dominante : <b>{row['filiere_dominante'].replace('production_', '').capitalize()}</b><br>"
                f"Production : {row['valeur_max']} MWh"
            )
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    return m