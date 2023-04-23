import pandas as pd

from .data_attributes import DataAttributes


def convert_all_df_rows_to_dict(df: pd.DataFrame) -> list[dict]:
    new_df = df.reset_index().rename(columns={"Datetime": "date"})
    data = [new_df.iloc[i].to_dict() for i in range(len(df))]
    return [convert_df_row_to_dict(data) for data in data]


def convert_df_row_to_dict(data: dict[str, float]) -> dict:
    data = {k.lower(): v for k, v in data.items()}

    required_attributes = [attr.name for attr in DataAttributes]
    return {k: v for k, v in data.items() if k in required_attributes}
