import os
import pandas as pd
import argparse

from lib import output_to_file, concatenate_simply
from lib.vocab_size_increase import VocabSizeIncrease

def main(target_filepath, row, record_num, char_code, header) -> int:
    filename = os.path.basename(target_filepath)
    if header:
        df = pd.read_csv(target_filepath, header=0, encoding=char_code)
    else:
        df = pd.read_csv(target_filepath, header=None, encoding=char_code)
        row = int(row)
    
    
    success, df = concatenate_simply.concatenate_df(df, record_num)
    if not success:
        print("データの増量に失敗しました。")
        exit()
    filename = filename.split(".")[0] + f"_{str(record_num)}records" + ".csv"
    
    vsi = VocabSizeIncrease(df[row])
    success, df[row] = vsi.vocab_size_increase()
    if not success:
        print("語彙数の増量に失敗しました。")
        exit()

    output_to_file.output_to_csv(df, filename, char_code)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_filepath", help="対象となるcsvファイルのパスを指定してください")
    parser.add_argument("row_name", help="変換対象の列を指定してください")
    parser.add_argument("record_num", help="作成するデータのレコード数を指定してください", type=int)

    parser.add_argument("-c", "--code", help="文字コードの指定ができます。", default="utf-8")
    parser.add_argument("--no_header", help="ヘッダー行が存在しないときに指定してください", action='store_false')

    args = parser.parse_args()
    
    main(args.target_filepath, args.row_name, args.record_num, args.code, args.no_header)