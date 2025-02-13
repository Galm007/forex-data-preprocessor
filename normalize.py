import pandas as pd
import numpy as np


def normalize_data(data: pd.DataFrame):
    normalize_datetime(data, "DATETIME")
    normalize_price(data, "OPEN")
    normalize_price(data, "HIGH")
    normalize_price(data, "LOW")
    normalize_price(data, "CLOSE")
    normalize_volume(data, "VOLUME")
    normalize_derivative(data, "CLOSE DERIVATIVE")
    normalize_derivative(data, "VOLUME DERIVATIVE")
    normalize_ma(data, "EMA(500)")
    normalize_ma(data, "EMA(200)")
    normalize_ma(data, "EMA(100)")
    normalize_ma(data, "EMA(50)")
    normalize_ma(data, "EMA(25)")
    normalize_ma(data, "EMA(8)")
    normalize_stddev(data, "STDDEV(20)")
    normalize_macd_signal(data, "MACD_SIGNAL(12, 26, 9)")


def normalize_datetime(data: pd.DataFrame, column_name: str):
    SECS_IN_DAY = 24.0 * 60.0 * 60.0
    arr = []
    for time in data[column_name]:
        secs = time.hour * 3600.0 + time.minute * 60.0 + time.second
        arr.append(secs / SECS_IN_DAY)
    data[column_name] = arr


def normalize_price(data: pd.DataFrame, column_name: str):
    minimum = min(data[column_name])
    maximum = max(data[column_name])
    diff = maximum - minimum

    arr = []
    for price in data[column_name]:
        arr.append((price - minimum) / diff)
    data[column_name] = arr


def normalize_volume(data: pd.DataFrame, column_name: str):
    maximum = max(data[column_name])

    arr = []
    for volume in data[column_name]:
        arr.append(volume / maximum)
    data[column_name] = arr


def normalize_derivative(data: pd.DataFrame, column_name: str):
    minimum = np.nanmin(data[column_name])
    maximum = np.nanmax(data[column_name])
    diff = maximum - minimum

    arr = []
    for value in data[column_name]:
        if np.isnan(value):
            arr.append(np.nan)
            continue
        arr.append(((value - minimum) / diff) * 2.0 - 1.0)
    data[column_name] = arr


def normalize_ma(data: pd.DataFrame, column_name: str):
    minimum = np.nanmin(data[column_name])
    maximum = np.nanmax(data[column_name])
    diff = maximum - minimum

    arr = []
    for price in data[column_name]:
        if np.isnan(price):
            arr.append(np.nan)
            continue
        arr.append((price - minimum) / diff)
    data[column_name] = arr


def normalize_stddev(data: pd.DataFrame, column_name: str):
    maximum = np.nanmax(data[column_name])

    arr = []
    for value in data[column_name]:
        arr.append(value / maximum)
    data[column_name] = arr


def normalize_macd_signal(data: pd.DataFrame, column_name: str):
    minimum = np.nanmin(data[column_name])
    maximum = np.nanmax(data[column_name])
    diff = maximum - minimum

    arr = []
    for value in data[column_name]:
        arr.append((value - minimum) / diff * 2.0 - 1.0)
    data[column_name] = arr
