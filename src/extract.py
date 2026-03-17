import requests
import pandas as pd
from io import StringIO

def get_currency_data(start_date, end_date):

    url = 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A'

    params = {
        'startPeriod': start_date,
        'endPeriod': end_date,
        'format' : 'csvdata'
    }

    response = requests.get(url, params=params)

    df = pd.read_csv(StringIO(response.text))

    return df