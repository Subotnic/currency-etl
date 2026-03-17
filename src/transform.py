import uuid
from datetime import datetime

def transform_currency(df):

    result = []

    for _, row in df.iterrows():

        record = {
            'id': str(uuid.uuid4()),
            'date': row['TIME_PERIOD'],
            'usd': 1,
            'euro': float(row['OBS_VALUE']),
            'created': datetime.utcnow().isoformat(),
            'updated': None
        }

        result.append(record)

    return result