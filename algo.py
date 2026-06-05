import pandas as pd

df = pd.read_csv('orders.csv')

print(df.head())

buyers_list = df['buyer_name'].unique().tolist()

datetime_date = pd.to_datetime(df['order_date'], format='%Y-%m-%d')

