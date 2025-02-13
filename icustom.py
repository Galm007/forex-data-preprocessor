import pandas as pd
import numpy as np
import math

# TODO: Speed up stddev algorithm


def sma(data: pd.DataFrame, period: int, shift: int):
    name = f"SMA({period})"
    if name in data:
        return data[name].iloc[shift]

    sum = 0
    for i in range(period):
        sum += data["CLOSE"].iloc[shift - i]
    return sum / period


def sma_filldata(data: pd.DataFrame, period: int) -> None:
    arr = [np.nan for _ in range(period - 1)]
    sum = 0

    for i in range(period):
        sum += data["CLOSE"].iloc[i]
    arr.append(sum / period)

    for i in range(len(data) - period):
        sum += data["CLOSE"].iloc[period + i]
        sum -= data["CLOSE"].iloc[i]
        arr.append(sum / period)

    data[f"SMA({period})"] = arr


def ema_filldata(data: pd.DataFrame, period: int) -> None:
    arr = [np.nan for _ in range(period - 1)]

    prev = sma(data, period, period - 1)
    arr.append(prev)

    for i in range(len(data) - period):
        k = 2 / (period + 1)
        ema = data["CLOSE"].iloc[period + i] * k + prev * (1 - k)
        arr.append(ema)
        prev = ema

    data[f"EMA({period})"] = arr


def macd_filldata(
    data: pd.DataFrame, fast_ema_period: int, slow_ema_period: int
) -> None:
    fast_ema_name = f"EMA({fast_ema_period})"
    slow_ema_name = f"EMA({slow_ema_period})"

    ema_filldata(data, fast_ema_period)
    ema_filldata(data, slow_ema_period)

    arr = [np.nan for _ in range(slow_ema_period - 1)]

    for i in range(len(data) - slow_ema_period + 1):
        fast_ema = data[fast_ema_name].iloc[slow_ema_period - 1 + i]
        slow_ema = data[slow_ema_name].iloc[slow_ema_period - 1 + i]
        arr.append(fast_ema - slow_ema)

    data.drop(columns=[fast_ema_name, slow_ema_name])
    data[f"MACD({fast_ema_period}, {slow_ema_period})"] = arr


def macd_signal_filldata(
    data: pd.DataFrame, fast_ema_period: int, slow_ema_period: int, signal_period: int
) -> None:
    macd_name = f"MACD({fast_ema_period}, {slow_ema_period})"
    macd_filldata(data, fast_ema_period, slow_ema_period)

    arr = [np.nan for _ in range(slow_ema_period + signal_period - 1)]
    sum = 0

    for i in range(signal_period):
        sum += data[macd_name].iloc[slow_ema_period + i]
    arr.append(sum / signal_period)

    for i in range(len(data) - slow_ema_period - signal_period):
        sum += data[macd_name].iloc[slow_ema_period + signal_period + i]
        sum -= data[macd_name].iloc[slow_ema_period + i]
        arr.append(sum / signal_period)

    data.drop(columns=[macd_name])
    data[f"MACD_SIGNAL({fast_ema_period}, {slow_ema_period}, {signal_period})"] = arr


def stddev_filldata(data: pd.DataFrame, period: int) -> None:
    sma_name = f"SMA({period})"
    sma_filldata(data, period)

    arr = [np.nan for _ in range(period - 1)]

    for i in range(len(data) - period + 1):
        variance_sum = 0
        for j in range(period - 1):
            variance_sum += (
                data["CLOSE"].iloc[period - 1 + i - j]
                - data[sma_name].iloc[period - 1 + i]
            ) ** 2
        arr.append(math.sqrt(variance_sum / (period - 1)))

    data.drop(columns=[sma_name])
    data[f"STDDEV({period})"] = arr


def derivative_filldata(data: pd.DataFrame, column_name: str):
    column = data[column_name]
    arr = [np.nan]

    for i in range(len(column) - 1):
        arr.append(column.iloc[i + 1] - column.iloc[i])

    data[f"{column_name} DERIVATIVE"] = arr
