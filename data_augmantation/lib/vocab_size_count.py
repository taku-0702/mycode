import MeCab
import pandas as pd
from dataclasses import dataclass

# dataclass使うまでもなさそう
@dataclass
class Word:
    hinshi: str
    katsuyokei: str
    count: int = 0

class VocabSizeCounter:
    def __init__(self, sr: pd.Series) -> None:
        self.tagger = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
        self.sr = sr

        self.result = []

    def count_words(self):
        select_conditions = ["名詞", "動詞", "形容詞"]
        surfaces = dict()
        word_count = 0
        
        # 多重ループ避けたい
        for sentence in self.sr:
            node = self.tagger.parseToNode(sentence)
            while node:
                surface = node.surface
                hinshi = node.feature.split(',')[0]
                katsuyokei = node.feature.split(',')[5]
                node = node.next

                if hinshi not in select_conditions:
                    continue
                
                word_count += 1
                if surfaces.get(surface):
                    surfaces[surface].count += 1
                else:
                    surfaces[surface] = Word(hinshi, katsuyokei)
                
                if word_count % 10 == 0:
                    self.result.append([word_count, len(surfaces.keys())])
            
        return pd.DataFrame(self.result, columns=["word_num", "vocab_size"])
