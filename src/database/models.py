# type: ignore
# ruff: noqa
import enum
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TickerSymbols(enum.Enum):
    EURUSD = "EURUSD=X"
    GBPUSD = "GBPUSD=X"
    BTCUSD = "BTC-USD"


class TimeFrames(enum.Enum):
    hour = "60m"
    day = "1d"


class TickerSymbolsTable(Base):
    __tablename__ = "TickerSymbols"

    id = Column(Integer, primary_key=True)
    ticker_symbol = Column(Enum(TickerSymbols), nullable=False)

    def __init__(self, ticker_symbol: TickerSymbols) -> None:
        self.ticker_symbol = ticker_symbol


class TimeFramesTable(Base):
    __tablename__ = "TimeFrames"

    id = Column(Integer, primary_key=True)
    time_frame = Column(Enum(TimeFrames), nullable=False)

    def __init__(self, time_frame: TimeFrames) -> None:
        self.time_frame = time_frame


class HistoricalDataTable(Base):
    __tablename__ = "HistoricalData"

    id = Column(Integer, primary_key=True)
    ticker_symbol_id = Column(
        Integer, ForeignKey("TickerSymbols.id", ondelete="CASCADE"), nullable=False
    )
    time_frames_id = Column(
        Integer, ForeignKey("TimeFrames.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    def __init__(
        self,
        ticker_symbol_id: int,
        time_frames_id: int,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ) -> None:
        self.ticker_symbol_id = ticker_symbol_id
        self.time_frames_id = time_frames_id
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
