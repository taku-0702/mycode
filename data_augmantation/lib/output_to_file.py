import pandas as pd

def output_to_csv(df: pd.DataFrame, filename: str, char_code="utf-8") -> None:
    df.to_csv(f"output/{filename}", encoding=char_code, index=False)