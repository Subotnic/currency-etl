from src.extract import get_currency_data
from src.transform import transform_currency

df = get_currency_data("2024-01-01", "2024-01-05")

print("Extract result:")
print(df.head())

data = transform_currency(df)

print("\nTransform result:")
print(data[:2])

