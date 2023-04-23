from collections.abc import Sequence
from datetime import datetime, timedelta

import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import (
    HistoricalDataTable,
    TickerSymbols,
    TickerSymbolsTable,
    TimeFrames,
    TimeFramesTable,
)
from src.utils.config import DbInfo, get_db_url


class DatabaseConnection:
    def __init__(self, db_info: DbInfo) -> None:
        db_url = get_db_url(db_info)
        self.session_maker = sessionmaker(bind=create_engine(db_url))

    def update_ticker_symbols(self) -> None:
        symbols = [entry.ticker_symbol for entry in self.get_db_symbols()]
        symbols_to_add = [symbol for symbol in TickerSymbols if symbol not in symbols]
        with self.session_maker() as session:
            for sym in symbols_to_add:
                session.add(TickerSymbolsTable(sym))
                session.commit()

    def get_db_symbols(self) -> list[TickerSymbolsTable]:
        with self.session_maker() as session:
            return session.query(TickerSymbolsTable).all()

    def update_timeframes(self) -> None:
        time_frames = [entry.time_frame for entry in self.get_db_time_frames()]
        time_frames_to_add = [tf for tf in TimeFrames if tf not in time_frames]
        with self.session_maker() as session:
            for tf in time_frames_to_add:
                session.add(TimeFramesTable(tf))
                session.commit()

    def get_db_time_frames(self) -> list[TimeFramesTable]:
        with self.session_maker() as session:
            return session.query(TimeFramesTable).all()

    def get_ticker_symbol_id(self, symbol: TickerSymbols) -> int | None:
        with self.session_maker() as session:
            db_symbol = (
                session.query(TickerSymbolsTable)
                .filter(TickerSymbolsTable.ticker_symbol == symbol)
                .first()
            )

            if db_symbol is None:
                return None

            return db_symbol.id  # type: ignore

    def get_timeframe_id(self, tf: TimeFrames) -> int | None:
        with self.session_maker() as session:
            db_tf = session.query(TimeFramesTable).filter(TimeFramesTable.time_frame == tf).first()

            if db_tf is None:
                return None

            return db_tf.id  # type: ignore

    def update_historical_data(self, historical_data: Sequence[HistoricalDataTable]) -> None:
        with self.session_maker() as session:
            for item in historical_data:
                session.add(item)
            session.commit()

    def delete_final_historical_record(self, symbol: TickerSymbols, tf: TimeFrames) -> None:
        with self.session_maker() as session:
            last_record = self.get_final_historical_record(symbol, tf)

            if last_record is None:
                return

            session.delete(last_record)
            session.commit()

    def get_final_historical_record(
        self, symbol: TickerSymbols, tf: TimeFrames
    ) -> HistoricalDataTable | None:
        with self.session_maker() as session:
            return (
                session.query(HistoricalDataTable)
                .join(TickerSymbolsTable)
                .join(TimeFramesTable)
                .filter(
                    TickerSymbolsTable.ticker_symbol == symbol, TimeFramesTable.time_frame == tf
                )
                .order_by(HistoricalDataTable.id.desc())
                .first()
            )

    def calculate_missing_data_start_time(self, symbol: TickerSymbols, tf: TimeFrames) -> datetime:
        final_historical_record = self.get_final_historical_record(symbol, tf)
        if final_historical_record is not None:
            return final_historical_record.date  #  type: ignore
        end_date = datetime.now(pytz.timezone("Asia/Tokyo"))
        return end_date - timedelta(days=28)
