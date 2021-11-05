import pandas as pd
from typing import Tuple

def concatenate_df(df: pd.DataFrame, max_row: int) -> Tuple[bool, pd.DataFrame]:
    merged_df = pd.concat([df, df], axis=0)
    while len(merged_df) < max_row:
        merged_df = pd.concat([merged_df, df], axis=0)

    merged_df = merged_df.iloc[:max_row, :]
    merged_df.index = range(0, max_row)
    return (True, merged_df)