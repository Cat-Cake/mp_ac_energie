import requests

ODRE_URL_ECO2MIX_REGIONAL_MENSUEL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-cons-def/records"
ODRE_URL_ECO2MIX_REGIONAL_TR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/records"
ODRE_URL_PRODUCTION_NATIONAL_SECTOR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/prod-national-annuel-filiere/records"
ODRE_URL_ELECTRIC_STATION = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records"
ENEDIS_URL_CONSUMPTION_COMMUNE_ACTIVITY = "https://data.enedis.fr/api/explore/v2.1/catalog/datasets/consommation-electrique-par-secteur-dactivite-commune/records"

DEFAULT_PARAMS = {
    'limit': 1000,
}


def get_data(url: str, params: dict = None):
    try:
        response = requests.get(url, params=params or DEFAULT_PARAMS)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"Impossible de récupérer les données depuis {url} : {e}")
        return []


def get_data_eco2mix_regional_tr():
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-date_heure'
        }
        try:
            response = requests.get(ODRE_URL_ECO2MIX_REGIONAL_TR, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
        except requests.RequestException as e:
            print(f"offset {offset} : {e}")
            break

        if not results:
            break

        all_results.extend(results)
        offset += limit

        print(f"→ {len(all_results)} lignes récupérées…")

        if len(results) < limit:
            break

    return all_results


def get_data_electric_station():
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        try:
            response = requests.get(ODRE_URL_ELECTRIC_STATION, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
        except requests.RequestException as e:
            print(f"offset {offset} : {e}")
            break

        if not results:
            break

        all_results.extend(results)
        offset += limit

        print(f"→ {len(all_results)} lignes récupérées…")

        if len(results) < limit:
            break

    return all_results


def get_data_production_national_sector(params=None):
    return get_data(ODRE_URL_PRODUCTION_NATIONAL_SECTOR, params=params)


def get_data_consumption_commune_activity(params=None):
    return get_data(ENEDIS_URL_CONSUMPTION_COMMUNE_ACTIVITY, params=params)
