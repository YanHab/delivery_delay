import pandas as pd
from pathlib import Path


def load_raw_data():

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

    data_customers = pd.read_csv(RAW_DATA_DIR / "olist_customers_dataset.csv")
    data_products = pd.read_csv(RAW_DATA_DIR / "olist_products_dataset.csv")
    data_sellers = pd.read_csv(RAW_DATA_DIR / "olist_sellers_dataset.csv")
    data_geolocation = pd.read_csv(RAW_DATA_DIR / "olist_geolocation_dataset.csv")
    data_orders = pd.read_csv(RAW_DATA_DIR / "olist_orders_dataset.csv")
    data_payments = pd.read_csv(RAW_DATA_DIR / "olist_order_payments_dataset.csv")
    data_order_items = pd.read_csv(RAW_DATA_DIR / "olist_order_items_dataset.csv")




    geo_by_zip = (
        data_geolocation
        .groupby("geolocation_zip_code_prefix", as_index=False)
        .agg(
            customer_lat=("geolocation_lat", "mean"),
            customer_lon=("geolocation_lng", "mean"),
        )
    )

    customers_geo = data_customers.merge(
        geo_by_zip,
        how="left",
        left_on="customer_zip_code_prefix",
        right_on="geolocation_zip_code_prefix",
        validate="many_to_one",
    )


    order_with_products = data_order_items.merge(data_products, on="product_id", how="left",validate="many_to_one",indicator=True)
    orders_with_customers = data_orders.merge(customers_geo, on="customer_id", how="left",validate="many_to_one",indicator=True)
    
    connected_data = (order_with_products.drop(columns="_merge").merge( 
        orders_with_customers.drop(columns="_merge"),
        on="order_id",
        how="left",
        validate="many_to_one",
        indicator=True
    ))

    connected_data = connected_data.drop(columns="_merge")

    date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date",
    
    
    ]



    for column in date_columns:
        connected_data[column] = pd.to_datetime(
            connected_data[column],
            errors="raise",
        )

    return connected_data