# forex-data-preprocessor
Transforms historical data and indicator values into normalized values to be used by AI

This repo contains historical price data for the EURUSD pair in 3 timeframes (D1, H4, and H1). Use [this site](https://forexsb.com/historical-forex-data) to download the most recent historical data.

How to run:
```
# make sure to put the data csv files in the correct order (D1, H4, then H1)
python preprocessor.py EURUSD_D1.csv EURUSD_H4.csv EURUSD_H1.csv
```
