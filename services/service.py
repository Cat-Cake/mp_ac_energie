import requests

ODRE_URL_ECO2MIX_REGIONAL_TR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/records"
ODRE_URL_ECOGAS_TR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/signal-ecogaz/records"
ODRE_URL_ELECTRIC_STATION = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records"
ODRE_URL_PRODUCTION_NATIONAL_SECTOR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/prod-national-annuel-filiere/records"
ODRE_URL_PRODUCTION_REGION_SECTOR = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/prod-region-annuelle-filiere/records"
ODRE_URL_COMMERCIAL_EXCHANGE_2024 = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/imports-exports-commerciaux/records?refine=date%3A%222024%22"
ODRE_URL_GAS_EMISSIONS = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/emissions-ges-operateurs/records"
ODRE_URL_SIGNAL_ECOWATT = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/nouveau_signal_ecowatt/records"

DEFAULT_PARAMS = {
    'limit': 100,
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


def get_data_ecogas_tr():
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        try:
            response = requests.get(ODRE_URL_ECOGAS_TR, params=params)
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


def get_data_production_regional_sector(params=None):
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        try:
            response = requests.get(ODRE_URL_PRODUCTION_REGION_SECTOR, params=params)
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


def get_data_commercial_exchange_2024(params=None):
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        try:
            response = requests.get(ODRE_URL_COMMERCIAL_EXCHANGE_2024, params=params)
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


def get_data_gas_emissions(params=None):
    return get_data(ODRE_URL_GAS_EMISSIONS, params=params)


def get_data_signal_ecowatt(params=None):
    all_results = []
    offset = 0
    limit = 100

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        try:
            response = requests.get(ODRE_URL_SIGNAL_ECOWATT, params=params)
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