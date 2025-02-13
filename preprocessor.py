import sys
import pandas as pd
from icustom import *
from normalize import normalize_data

# -- CSV Columns and their normalized ranges
# DATETIME                 (0,1)
# OPEN                     (0,1)
# HIGH                     (0,1)
# LOW                      (0,1)
# CLOSE                    (0,1)
# CLOSE DERIVATIVE         (-1,1)
# VOLUME                   (0,1)
# VOLUME DERIVATIVE        (-1,1)
# EMA(500)                 (0,1)
# EMA(200)                 (0,1)
# EMA(100)                 (0,1)
# EMA(50)                  (0,1)
# EMA(25)                  (0,1)
# EMA(8)                   (0,1)
# EMA(500) DERIVATIVE      (-1,1)
# EMA(200) DERIVATIVE      (-1,1)
# EMA(100) DERIVATIVE      (-1,1)
# EMA(50) DERIVATIVE       (-1,1)
# EMA(25) DERIVATIVE       (-1,1)
# EMA(8) DERIVATIVE        (-1,1)
# STDDEV(20)               (0,1)
# MACD_SIGNAL(12, 26, 9)   (0,1)


def preprocess(data: pd.DataFrame) -> None:
    derivative_filldata(data, "CLOSE")
    derivative_filldata(data, "VOLUME")
    ema_filldata(data, 500)
    ema_filldata(data, 200)
    ema_filldata(data, 100)
    ema_filldata(data, 50)
    ema_filldata(data, 25)
    ema_filldata(data, 8)
    stddev_filldata(data, 20)
    macd_signal_filldata(data, 12, 26, 9)

    normalize_data(data)


if __name__ == "__main__":
    histdata = {}

    for arg in sys.argv[1:]:
        histdata[arg.rsplit(".", 1)[0]] = pd.read_csv(
            arg, names=["DATETIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        )

    for filename, data in histdata.items():
        data["DATETIME"] = pd.to_datetime(data["DATETIME"])
        data["OPEN"] = pd.to_numeric(data["OPEN"])
        data["HIGH"] = pd.to_numeric(data["HIGH"])
        data["LOW"] = pd.to_numeric(data["LOW"])
        data["CLOSE"] = pd.to_numeric(data["CLOSE"])
        data["VOLUME"] = pd.to_numeric(data["VOLUME"])
        preprocess(data)

        data.to_csv(f"{filename}_data.csv", index=False)
        print(f"Generated {filename}_data.csv! ({len(data)} rows)")
