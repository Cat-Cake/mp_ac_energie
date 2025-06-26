from services.service import (
    get_data_eco2mix_regional_tr,
    get_data_electric_station,
    get_data_production_national_sector,
    get_data_production_regional_sector,
    get_data_commercial_exchange_2024,
    get_data_ecogas_tr,
    get_data_gas_emissions,
    get_data_signal_ecowatt
)
from processing.transform import (
    get_or_prepare_regional_realtime, prepare_ecowatt_national_alerts,
)
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data():
    data = get_data_eco2mix_regional_tr()
    return get_or_prepare_regional_realtime(data)


@st.cache_data(show_spinner=False)
def load_map_data():
    data = get_data_electric_station()
    from processing.map_generator import create_charging_map
    return create_charging_map(data)


@st.cache_data(show_spinner=False)
def load_national_data():
    return get_data_production_national_sector({"limit": 20})


@st.cache_data(show_spinner=False)
def load_region_main_sector_data():
    return get_data_production_regional_sector()


@st.cache_data(show_spinner=False)
def load_commercial_exchange_2024_data():
    return get_data_commercial_exchange_2024()


@st.cache_data(show_spinner=False)
def load_ecogas_data():
    return get_data_ecogas_tr()


@st.cache_data(show_spinner=False)
def load_gas_emission_data():
    return get_data_gas_emissions()


@st.cache_data(show_spinner=False)
def load_ecowatt_national_alerts():
    return prepare_ecowatt_national_alerts(get_data_signal_ecowatt())
