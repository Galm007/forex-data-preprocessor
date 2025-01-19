from datetime import datetime
from histdata import HistData

def normalize_data(data: HistData) -> HistData:
    normalized_data = data

    timeframes = ["D1", "H4", "H1"]
    for tf in timeframes:
        normalized_data.datetime[tf] = normalize_datetime(data.datetime[tf])
        normalized_data.open[tf] = normalize_price(data, tf, data.open)
        normalized_data.high[tf] = normalize_price(data, tf, data.high)
        normalized_data.low[tf] = normalize_price(data, tf, data.low)
        normalized_data.close[tf] = normalize_price(data, tf, data.close)
        normalized_data.icustom[f"{tf} CLOSE DERIVATIVE"] = normalize_derivative(data, tf, data.icustom[f"{tf} CLOSE DERIVATIVE"])

        normalized_data.volume[tf] = normalize_volume(data, tf)
        normalized_data.icustom[f"{tf} VOLUME DERIVATIVE"] = normalize_derivative(data, tf, data.icustom[f"{tf} VOLUME DERIVATIVE"])

        normalized_data.icustom[f"{tf} EMA(500)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(500)"])
        normalized_data.icustom[f"{tf} EMA(200)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(200)"])
        normalized_data.icustom[f"{tf} EMA(100)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(100)"])
        normalized_data.icustom[f"{tf} EMA(50)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(50)"])
        normalized_data.icustom[f"{tf} EMA(25)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(25)"])
        normalized_data.icustom[f"{tf} EMA(8)"] = normalize_ma(data, tf, data.icustom[f"{tf} EMA(8)"])

        normalized_data.icustom[f"{tf} STDDEV(20)"] = normalize_stddev(data, tf, data.icustom[f"{tf} STDDEV(20)"])
        normalized_data.icustom[f"{tf} MACD_SIGNAL(12, 26, 9)"] = normalize_macd_signal(data, tf, data.icustom[f"{tf} MACD_SIGNAL(12, 26, 9)"])

    return normalized_data

def normalize_datetime(arr: list[str]) -> list[float]:
    SECS_IN_DAY = 24.0 * 60.0 * 60.0
    res = []
    for time in arr:
        dt = datetime.strptime(time.split()[1], "%H:%M")
        secs = dt.hour * 3600.0 + dt.minute * 60.0 + dt.second
        res.append(secs / SECS_IN_DAY)
    return res

def normalize_price(data: HistData, timeframe: str, arr: dict[str, list[float]]) -> list[float]:
    minimum = min(arr[timeframe])
    maximum = max(arr[timeframe])
    diff = maximum - minimum

    res = []
    for price in arr[timeframe]:
        res.append((price - minimum) / diff)
    return res

def normalize_volume(data: HistData, timeframe: str) -> list[float]:
    maximum = max(data.volume[timeframe])

    res = []
    for price in data.volume[timeframe]:
        res.append(price / maximum)
    return res

def normalize_derivative(data: HistData, timeframe: str, arr: list[float]) -> list[float]:
    minimum = min(arr)
    maximum = max(arr)
    diff = maximum - minimum

    res = []
    for value in arr:
        res.append(((value - minimum) / diff) * 2.0 - 1.0)
    return res

def normalize_ma(data: HistData, timeframe: str, arr: list[float]) -> list[float]:
    minimum = min(arr)
    maximum = max(arr)
    diff = maximum - minimum

    res = []
    for price in arr:
        res.append((price - minimum) / diff)
    return res

def normalize_stddev(data: HistData, timeframe: str, arr: list[float]) -> list[float]:
    maximum = max(arr)

    res = []
    for value in arr:
        res.append(value / maximum)
    return res

def normalize_macd_signal(data: HistData, timeframe: str, arr: list[float]) -> list[float]:
    minimum = min(arr)
    maximum = max(arr)
    diff = maximum - minimum

    res = []
    for value in arr:
        res.append((value - minimum) / diff * 2.0 - 1.0)
    return res
