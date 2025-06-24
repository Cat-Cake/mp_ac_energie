import os

import folium
import pandas as pd


def prepare_regional_mix(data):
    df = pd.DataFrame(data)
    print(df.head())

    df["date_heure"] = df["date_heure"].str.replace(r"\+.*$", "", regex=True)
    df["date_heure"] = pd.to_datetime(df["date_heure"], errors='coerce')
    print(f"Dtype of df['date_heure'] after conversion: {df['date_heure'].dtype}")
    df["mois"] = df["date_heure"].dt.to_period("M").dt.to_timestamp()

    colonnes_prod = ["thermique", "nucleaire", "eolien", "solaire", "hydraulique", "bioenergies"]
    colonnes = ["consommation"] + colonnes_prod
    df[colonnes] = df[colonnes].apply(pd.to_numeric, errors="coerce")

    df["production_totale"] = df[colonnes_prod].sum(axis=1)

    df_mensuel = df.groupby(["libelle_region", "mois"])[["consommation", "production_totale"]].sum().reset_index()

    df_mensuel = df_mensuel.rename(columns={
        "mois": "date",
        "consommation": "consommation_totale_mensuelle",
        "production_totale": "production_totale_mensuelle"
    })

    return df_mensuel


def get_or_prepare_regional_realtime(data, cache_path="data/realtime_cache.parquet"):
    if os.path.exists(cache_path):
        print("Chargement depuis le cache...")
        return pd.read_parquet(cache_path)

    df = prepare_regional_realtime(data)

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    df.to_parquet(cache_path)
    print("Données enregistrées en cache.")

    return df


def prepare_regional_realtime(data):
    df = pd.DataFrame(data)

    df["date_heure"] = df["date_heure"].str.replace(r"\+.*$", "", regex=True)
    df["date_heure"] = pd.to_datetime(df["date_heure"], errors="coerce")
    df = df[df["date_heure"].notna()]

    colonnes_prod = ["thermique", "nucleaire", "eolien", "solaire", "hydraulique", "bioenergies"]
    colonnes = ["consommation"] + colonnes_prod

    for col in colonnes:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["production_totale"] = df[colonnes_prod].sum(axis=1)

    df = df.sort_values(["libelle_region", "date_heure"])

    return df[["libelle_region", "date_heure", "consommation", "production_totale"]]


def create_charging_map(data):
    df = pd.DataFrame(data)

    if "geo_point_borne" not in df.columns:
        raise ValueError("Le champ 'geo_point_borne' est manquant dans les données.")

    df = df[df["geo_point_borne"].notna()]
    df["latitude"] = df["geo_point_borne"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df["longitude"] = df["geo_point_borne"].apply(lambda x: x.get("lon") if isinstance(x, dict) else None)

    # Supprimer les lignes incomplètes
    df = df.dropna(subset=["latitude", "longitude"])

    # Créer la carte
    m = folium.Map(location=[46.6, 2.4], zoom_start=6)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            popup=row.get("n_station", "Station inconnue"),
            color="blue",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    return m