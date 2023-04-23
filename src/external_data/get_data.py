from datetime import datetime

import pandas as pd
import yfinance as yf

from src.database.models import TickerSymbols, TimeFrames


def get_historical_data(
    symbol: TickerSymbols, tf: TimeFrames, start_date: datetime, end_date: datetime
) -> pd.DataFrame:
    return yf.download(tickers=symbol.value, start=start_date, end=end_date, interval=tf.value)
