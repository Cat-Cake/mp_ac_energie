import os
import streamlit as st
import folium
import pandas as pd


@st.cache_data
def prepare_regional_mix(data):
    df = pd.DataFrame(data)

    df["date_heure"] = df["date_heure"].str.replace(r"\+.*$", "", regex=True)
    df["date_heure"] = pd.to_datetime(df["date_heure"], errors='coerce')
    df["date_heure"] = df["date_heure"].dt.tz_convert("Europe/Paris")
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


@st.cache_data
def prepare_ecogas_mix(data):
    df = pd.DataFrame(data)

    df["gas_day"] = pd.to_datetime(df["gas_day"], errors="coerce")
    df["indice_de_couleur"] = pd.to_numeric(df["indice_de_couleur"], errors="coerce")

    df = df.sort_values("gas_day")

    df_chart = df[["gas_day", "indice_de_couleur", "color"]].dropna()

    return df_chart


@st.cache_data
def prepare_production_region_sector(data):
    df = pd.DataFrame(data)

    df["annee"] = pd.to_numeric(df["annee"], errors="coerce")

    colonnes_prod = [
        "production_thermique",
        "production_nucleaire",
        "production_eolienne",
        "production_solaire",
        "production_hydraulique",
        "production_bioenergies"
    ]
    df[colonnes_prod] = df[colonnes_prod].apply(pd.to_numeric, errors="coerce")

    df["production_totale"] = df[colonnes_prod].sum(axis=1)

    df["lat"] = df["geo_point_region"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df["lon"] = df["geo_point_region"].apply(lambda x: x.get("lon") if isinstance(x, dict) else None)

    df_region_sector = df.groupby(["region", "annee"], as_index=False).agg({
        **{col: "sum" for col in colonnes_prod + ["production_totale"]},
        "lat": "first",
        "lon": "first"
    })

    return df_region_sector


@st.cache_data
def get_or_prepare_regional_realtime(data, cache_path="data/realtime_cache.parquet"):
    print("➡️ Exemple de ligne :", data[0])
    if os.path.exists(cache_path):
        try:
            df = pd.read_parquet(cache_path)
            if "date_heure" in df.columns:
                print("Chargement depuis le cache.")
                return df
            else:
                print("Colonne 'date_heure' manquante : régénération du cache.")
        except Exception as e:
            print(f"Erreur de lecture du cache : {e}")

    df = prepare_regional_realtime(data)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    df.to_parquet(cache_path)
    print("Nouveau cache enregistré.")
    return df

@st.cache_data
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


@st.cache_data
def prepare_commercial_exchange(data):
    df = pd.DataFrame(data)
    cols_export = ["fr_gb", "fr_ch", "fr_it", "fr_es"]
    cols_import = ["gb_fr", "ch_fr", "it_fr", "es_fr"]

    df[cols_export + cols_import] = df[cols_export + cols_import].apply(pd.to_numeric, errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df[cols_export + cols_import] = df[cols_export + cols_import].apply(pd.to_numeric, errors="coerce")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["total_export"] = df[cols_export].sum(axis=1)
    df["total_import"] = df[cols_import].sum(axis=1)
    df["balance"] = df["total_export"] - df["total_import"]

    return df


@st.cache_data
def prepare_ecowatt_national_alerts(data):
    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    heure_cols = [f"h{h}" for h in range(24)]
    df[heure_cols] = df[heure_cols].apply(pd.to_numeric, errors="coerce")

    df["nb_alertes_jour"] = df[heure_cols].apply(lambda row: (row > 1).sum(), axis=1)

    df_alertes_jour = df[["date", "nb_alertes_jour", "couleur_du_jour"]].copy()
    df_alertes_jour = df_alertes_jour.sort_values("date")

    return df_alertes_jour
