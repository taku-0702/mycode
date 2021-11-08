import os
import pandas as pd
import argparse
import glob

from lib import output_to_file
from lib.vocab_size_count import VocabSizeCounter

def main(target_filepath, row, char_code, header) -> int:
    filename = os.path.basename(target_filepath)
    if header:
        df = pd.read_csv(target_filepath, header=0, encoding=char_code)
    else:
        df = pd.read_csv(target_filepath, header=None, encoding=char_code)
        row = int(row)
    
    filename = "vocabsize_" + filename.split(".")[0] + ".csv"
    
    vsc = VocabSizeCounter(df[row])
    result_df = vsc.count_words()

    output_to_file.output_to_csv(result_df, filename, char_code)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("target_filepath", help="対象となるcsvファイルのパスを指定してください")
    parser.add_argument("row_name", help="語彙数を数える列を指定してください")

    parser.add_argument("-c", "--code", help="文字コードの指定ができます。", default="utf-8")
    parser.add_argument("--no_header", help="ヘッダー行が存在しないときに指定してください", action='store_false')

    args = parser.parse_args()
    
    target_files = glob.glob("target_files/2021*.csv")
    for target_filepath in target_files:
        main(target_filepath, args.row_name, args.code, args.no_header)