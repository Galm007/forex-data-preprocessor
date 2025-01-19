# forex-data-preprocessor
Transforms historical data and indicator values into normalized values to be used by AI

This repo contains historical price data for the EURUSD pair in 3 timeframes (D1, H4, and H1). Use [this site](https://forexsb.com/historical-forex-data) to download the most recent historical data.

How to run:
```
# make sure to put the data csv files in the correct order (D1, H4, then H1)
python preprocessor.py EURUSD_D1.csv EURUSD_H4.csv EURUSD_H1.csv
```

This program outputs a file named "data.csv" that contains the preprocessed values. This csv file is delimited using '|' and not commas.

Preprocessed values:
```
# DATETIME
# OPEN
# HIGH
# LOW
# CLOSE
# CLOSE DERIVATIVE
# VOLUME
# VOLUME DERIVATIVE
# EMA(500)
# EMA(200)
# EMA(100)
# EMA(50)
# EMA(25)
# EMA(8)
# EMA(500) DERIVATIVE
# EMA(200) DERIVATIVE
# EMA(100) DERIVATIVE
# EMA(50) DERIVATIVE
# EMA(25) DERIVATIVE
# EMA(8) DERIVATIVE
# STDDEV(20)
# MACD_SIGNAL(12, 26, 9)
```

These set of values aim to recreate this trading environment for the AI:
![Screenshot_20250119_024224](https://github.com/user-attachments/assets/4a1bcb15-ada8-493e-9004-3f827cd10bb5)
