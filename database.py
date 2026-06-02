import pandas as pd
import os

def load_data():
    sales_file = 'sales.csv'
    customers_file = 'customers.csv'
    if not os.path.exists(sales_file) or not os.path.exists(customers_file):
        return None, None
    try:
        sales = pd.read_csv(sales_file)
        customers = pd.read_csv(customers_file)
        sales['date'] = pd.to_datetime(sales['date'])
        sales['revenue'] = sales['quantity'] * sales['price']
        sales['profit'] = sales['revenue'] - (sales['quantity'] * sales['cost'])
        return sales, customers
    except Exception as e:
        return None, None
