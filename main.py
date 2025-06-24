import os
import json

from processing.transform import prepare_regional_mix
from services.service import get_data_eco2mix_regional_mensuel

data = get_data_eco2mix_regional_mensuel()
df = prepare_regional_mix(data)

