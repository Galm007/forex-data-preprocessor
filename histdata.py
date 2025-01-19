import csv

class HistData:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.datetime = {}
        self.open = {}
        self.high = {}
        self.low = {}
        self.close = {}
        self.volume = {}
        self.valid_length = {}
        self.icustom = {}

    def parse_histdata_file(self, file, timeframe: str) -> None:
        self.datetime[timeframe] = []
        self.open[timeframe] = []
        self.high[timeframe] = []
        self.low[timeframe] = []
        self.close[timeframe] = []
        self.volume[timeframe] = []

        for (datetime, open, high, low, close, volume) in list(csv.reader(file, delimiter=',')):
            self.datetime[timeframe].append(datetime)
            self.open[timeframe].append(float(open))
            self.high[timeframe].append(float(high))
            self.low[timeframe].append(float(low))
            self.close[timeframe].append(float(close))
            self.volume[timeframe].append(int(volume))

        self.valid_length[timeframe] = self.bars(timeframe)

    def bars(self, timeframe: str) -> int:
        return len(self.datetime[timeframe])
    
    def update_valid_length(self, timeframe: str, length: int) -> None:
        self.valid_length[timeframe] = min(self.valid_length[timeframe], length)
