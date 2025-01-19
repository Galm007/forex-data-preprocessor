import csv
from histdata import HistData
from normalize import normalize_data
import icustom

# -- CSV Columns and their normalized ranges (repeat for timeframes D1, H4, H1 for a total of 22 columns)
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

def export_csv(data: HistData) -> None:
    csv_rows = [[]]
    timeframes = ["D1", "H4", "H1"]

    # label row
    label_row = [
        "DATETIME", "OPEN", "HIGH", "LOW", "CLOSE", "CLOSE DERIVATIVE", "VOLUME", "VOLUME DERIVATIVE",
        "EMA(500)", "EMA(200)", "EMA(100)", "EMA(50)", "EMA(25)", "EMA(8)", 
        "EMA(500) DERIVATIVE", "EMA(200) DERIVATIVE", "EMA(100) DERIVATIVE", "EMA(50) DERIVATIVE", "EMA(25) DERIVATIVE", "EMA(8) DERIVATIVE", 
        "STDDEV(20)", "MACD_SIGNAL(12, 26, 9)"
    ]
    for tf in timeframes:
        csv_rows[0].extend([f"{tf} {label}" for label in label_row])

    # value rows
    for i in range(min(data.valid_length["D1"], data.valid_length["H4"], data.valid_length["H1"])):
        row = []
        for tf in timeframes:
            row.append(data.datetime[tf][-i])
            row.append(data.open[tf][-i])
            row.append(data.high[tf][-i])
            row.append(data.low[tf][-i])
            row.append(data.close[tf][-i])
            row.append(data.icustom[f"{tf} CLOSE DERIVATIVE"][-i])
            row.append(data.volume[tf][-i])
            row.append(data.icustom[f"{tf} VOLUME DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(500)"][-i])
            row.append(data.icustom[f"{tf} EMA(200)"][-i])
            row.append(data.icustom[f"{tf} EMA(100)"][-i])
            row.append(data.icustom[f"{tf} EMA(50)"][-i])
            row.append(data.icustom[f"{tf} EMA(25)"][-i])
            row.append(data.icustom[f"{tf} EMA(8)"][-i])
            row.append(data.icustom[f"{tf} EMA(500) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(200) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(100) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(50) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(25) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} EMA(8) DERIVATIVE"][-i])
            row.append(data.icustom[f"{tf} STDDEV(20)"][-i])
            row.append(data.icustom[f"{tf} MACD_SIGNAL(12, 26, 9)"][-i])

        csv_rows.append(row)

    # write to file
    with open("data.csv", "w", newline="") as file:
        csv.writer(file, delimiter="|").writerows(csv_rows)

def preprocess(data: HistData) -> None:
    timeframes = ["D1", "H4", "H1"]
    for tf in timeframes:
        icustom.derivative_filldata(data, f"{tf} CLOSE", data.close[tf])
        icustom.derivative_filldata(data, f"{tf} VOLUME", data.volume[tf])

        icustom.ema_filldata(data, tf, 500)
        icustom.ema_filldata(data, tf, 200)
        icustom.ema_filldata(data, tf, 100)
        icustom.ema_filldata(data, tf, 50)
        icustom.ema_filldata(data, tf, 25)
        icustom.ema_filldata(data, tf, 8)

        icustom.derivative_filldata(data, f"{tf} EMA(500)", data.icustom[f"{tf} EMA(500)"])
        icustom.derivative_filldata(data, f"{tf} EMA(200)", data.icustom[f"{tf} EMA(200)"])
        icustom.derivative_filldata(data, f"{tf} EMA(100)", data.icustom[f"{tf} EMA(100)"])
        icustom.derivative_filldata(data, f"{tf} EMA(50)", data.icustom[f"{tf} EMA(50)"])
        icustom.derivative_filldata(data, f"{tf} EMA(25)", data.icustom[f"{tf} EMA(25)"])
        icustom.derivative_filldata(data, f"{tf} EMA(8)", data.icustom[f"{tf} EMA(8)"])

        icustom.stddev_filldata(data, tf, 20)

        icustom.macd_signal_filldata(data, tf, 12, 26, 9)

    export_csv(normalize_data(data))

if __name__ == "__main__":
    data = HistData("EURUSD")

    with open("EURUSD_D1.csv", "r") as file:
        data.parse_histdata_file(file, "D1")
    with open("EURUSD_H4.csv", "r") as file:
        data.parse_histdata_file(file, "H4")
    with open("EURUSD_H1.csv", "r") as file:
        data.parse_histdata_file(file, "H1")

    preprocess(data)
