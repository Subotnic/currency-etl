import clickhouse_connect
from datetime import datetime
import uuid

def load_to_clickhouse(data):

    client = clickhouse_connect.get_client(
        host='clickhouse',
        port=8123,
        username='default',
        password='admin',
    )

    rows = [
        (
            uuid.UUID(r['id']),
            datetime.strptime(r['date'], "%Y-%m-%d").date(),
            r['usd'],
            r['euro'],
            datetime.fromisoformat(r['created']),
            r['updated']
        )
        for r in data
    ]

    client.insert(
        'currency',
        rows,
        column_names =[
            'id',
            'date',
            'usd',
            'euro',
            'created',
            'updated'  
        ]
    )