import time
from datetime import datetime

import pytz

from src.database.db_utilities.db_funcs import DatabaseConnection
from src.database.models import HistoricalDataTable, TickerSymbols, TimeFrames
from src.external_data.convert_data import convert_all_df_rows_to_dict
from src.external_data.get_data import get_historical_data
from src.utils.config import ProjectConfig, load_project_config


def run(project_config: ProjectConfig) -> None:
    conn = DatabaseConnection(project_config.db_info)
    conn.update_ticker_symbols()
    conn.update_timeframes()

    for symbol in TickerSymbols:
        for tf in TimeFrames:
            ticker_symbol_id = conn.get_ticker_symbol_id(symbol)
            tf_id = conn.get_timeframe_id(tf)
            start_date = conn.calculate_missing_data_start_time(symbol, tf)

            historical_data = get_historical_data(
                symbol, tf, start_date, datetime.now(pytz.timezone("Asia/Tokyo"))
            )
            historical_data.to_csv(f"currency_data/{symbol.value}_{tf.value}")  # del

            db_ready_historical_data = [
                HistoricalDataTable(ticker_symbol_id, tf_id, **data_dict) for data_dict in convert_all_df_rows_to_dict(historical_data)  # type: ignore # noqa: E501
            ]

            conn.delete_final_historical_record(symbol, tf)
            conn.update_historical_data(db_ready_historical_data)

            sleep_time = 30
            print(f"sleeping for {sleep_time}")
            time.sleep(sleep_time)


if __name__ == "__main__":
    run(load_project_config())
