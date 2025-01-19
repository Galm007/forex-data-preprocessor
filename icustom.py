from histdata import HistData
import math

def require_data(data: HistData, icustom: str) -> None:
    if icustom not in data.icustom:
        raise Exception(f"iCustom \"{icustom}\" is required but has not been initialized!")

def sma(data: HistData, timeframe: str, period: int, shift: int) -> float:
    name = f"{timeframe} SMA({period})"
    if name in data.icustom:
        return data.icustom[name][shift]
    
    sum = 0
    for i in range(period):
        sum += data.close[timeframe][shift - i]
    return sum / period

def sma_filldata(data: HistData, timeframe: str, period: int) -> None:
    arr = [-1.0 for _ in range(period - 1)]
    sum = 0

    for i in range(period):
        sum += data.close[timeframe][i]
    arr.append(sum / period)

    for i in range(data.bars(timeframe) - period):
        sum += data.close[timeframe][period + i]
        sum -= data.close[timeframe][i]
        arr.append(sum / period)

    data.icustom[f"{timeframe} SMA({period})"] = arr
    data.update_valid_length(timeframe, data.bars(timeframe) - period + 1)

def ema_filldata(data: HistData, timeframe: str, period: int) -> None:
    arr = [-1.0 for _ in range(period - 1)]

    prev = sma(data, timeframe, period, period - 1)
    arr.append(prev)

    for i in range(data.bars(timeframe) - period):
        k = 2 / (period + 1)
        ema = data.close[timeframe][period + i] * k + prev * (1 - k)
        arr.append(ema)

        prev = ema

    data.icustom[f"{timeframe} EMA({period})"] = arr
    data.update_valid_length(timeframe, data.bars(timeframe) - period + 1)

def macd_filldata(data: HistData, timeframe: str, fast_ema_period: int, slow_ema_period: int) -> None:
    fast_ema_name = f"{timeframe} EMA({fast_ema_period})"
    slow_ema_name = f"{timeframe} EMA({slow_ema_period})"

    ema_filldata(data, timeframe, fast_ema_period)
    ema_filldata(data, timeframe, slow_ema_period)

    arr = [-1.0 for _ in range(slow_ema_period - 1)]

    for i in range(data.bars(timeframe) - slow_ema_period + 1):
        fast_ema = data.icustom[fast_ema_name][slow_ema_period + i - 1]
        slow_ema = data.icustom[slow_ema_name][slow_ema_period + i - 1]
        arr.append(fast_ema - slow_ema)

    data.icustom[f"{timeframe} MACD({fast_ema_period}, {slow_ema_period})"] = arr
    data.update_valid_length(timeframe, data.bars(timeframe) - slow_ema_period + 1)

def macd_signal_filldata(data: HistData, timeframe: str, fast_ema_period: int, slow_ema_period: int, signal_period: int) -> None:
    macd_name = f"{timeframe} MACD({fast_ema_period}, {slow_ema_period})"
    macd_filldata(data, timeframe, fast_ema_period, slow_ema_period)

    arr = [-1.0 for _ in range(slow_ema_period + signal_period - 1)]
    sum = 0

    for i in range(signal_period):
        sum += data.icustom[macd_name][slow_ema_period + i]
    arr.append(sum / signal_period)

    for i in range(data.bars(timeframe) - slow_ema_period - signal_period):
        sum += data.icustom[macd_name][slow_ema_period + signal_period + i]
        sum -= data.icustom[macd_name][slow_ema_period + i]
        arr.append(sum / signal_period)

    data.icustom[f"{timeframe} MACD_SIGNAL({fast_ema_period}, {slow_ema_period}, {signal_period})"] = arr
    data.update_valid_length(timeframe, data.bars(timeframe) - slow_ema_period - signal_period + 2)

def stddev_filldata(data: HistData, timeframe: str, period: int) -> None:
    sma_name = f"{timeframe} SMA({period})"

    sma_filldata(data, timeframe, period)

    arr = [-1.0 for _ in range(period - 1)]

    for i in range(data.bars(timeframe) - period + 1):
        variance_sum = 0

        for j in range(period - 1):
            variance_sum += (data.close[timeframe][period - 1 + i - j] - data.icustom[sma_name][period - 1 + i]) ** 2

        arr.append(math.sqrt(variance_sum / (period - 1)))

    data.icustom[f"{timeframe} STDDEV({period})"] = arr
    data.update_valid_length(timeframe, data.bars(timeframe) - period + 1)

def derivative_filldata(data: HistData, icustom_name: str, buffer: list[float]):
    arr = [-1.0]

    for i in range(len(buffer) - 1):
        arr.append(buffer[i + 1] - buffer[i])

    data.icustom[f"{icustom_name} DERIVATIVE"] = arr
