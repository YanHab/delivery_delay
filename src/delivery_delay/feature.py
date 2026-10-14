from delivery_delay import preprocessing


def build_features(dt):
    data = dt.copy()

    data["approval_duration_hours"] = (
        data["order_approved_at"] - data["order_purchase_timestamp"]
        ).dt.total_seconds() / 3600


    data["actual_delivery_duration_days"] = (
        data["order_delivered_customer_date"] - data["order_approved_at"]
        ).dt.total_seconds() / 86400


    data["delay_days"] = (
        data["order_delivered_customer_date"].dt.normalize()
        - data["order_estimated_delivery_date"].dt.normalize()
        ).dt.days


    data["shipping_window_days"] = (
        data["shipping_limit_date"]
        - data["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400


    data["purchased_at_weekends"] = (
        data["order_purchase_timestamp"].dt.day_of_week >= 5).astype(int)


    data["estimated_delivery_time"] = (
        data["order_estimated_delivery_date"] - data["order_approved_at"]
        ).dt.total_seconds() / 86400


    
    data["full_estimated_delivery_time"] = (
        data["order_estimated_delivery_date"] - data["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400


    
    data["overdue_days"] = data["delay_days"].clip(lower=0)

    data["is_delay"] = (data["overdue_days"] > 0 ).astype(int)

    return data


def build_dataset_baseline(data):
    numeric_features = [
    "price",
    "freight_value",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "approval_duration_hours",
    "overdue_days",
    "customer_zip_code_prefix", 
    "estimated_delivery_time",
    "full_estimated_delivery_time",
    "purchased_at_weekends",
    "shipping_window_days",
    "customer_lat",
    "customer_lon",
    "order_id",
    "is_delay",
    ]

    categorical_features = [
    "product_category_name",
    "customer_state",
]

    data_baseline = data[numeric_features + categorical_features].copy()
    
       
    data_baseline = data_baseline.drop(columns="overdue_days")
    return data_baseline

    
