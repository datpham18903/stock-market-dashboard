from pyspark.sql.window import Window
from pyspark.sql.functions import avg
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def calculate_technical_indicators(sdf):
    window_spec = Window.orderBy("Datetime")
    ma_periods = [50, 100, 200]

    for period in ma_periods:
        sdf = sdf.withColumn(
            f"MA{period}", avg("Close").over(window_spec.rowsBetween(-period + 1, 0))
        )

    return sdf


def prepare_prediction_data(sdf):
    close_values = sdf.select("Close").collect()

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_values)

    x_test = []
    for i in range(50, len(scaled_data)):
        x_test.append(scaled_data[i - 50 : i])

    return np.array(x_test), scaler