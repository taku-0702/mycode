import MeCab
import math
import pandas as pd
from dataclasses import dataclass
import random
import pickle
from typing import Tuple

def loadPickle(fileName):
    with open(fileName, mode="rb") as f:
        return pickle.load(f)

# dataclass使うまでもなさそう
@dataclass
class Word:
    hinshi: str
    katsuyokei: str
    count: int = 0

class VocabSizeIncrease:
    def __init__(self, sr: pd.Series, vocab_size_goal=None):
        self.tagger = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
        self.sr = sr
        self.vocab_size_goal = vocab_size_goal

        self.words, self.word_count = self.count_words()

        if self.vocab_size_goal is None:
            self.vocab_size_goal = self.decide_vocab_size_from_word_num()
            print(f"語彙数を{str(len(self.words.keys()))}語から{str(self.vocab_size_goal)}語に増やします。")

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
            
        return surfaces, word_count

    def decide_vocab_size_from_word_num(self):
        print("目標語彙数を単語数から決定します。")
        if self.word_count <= 1000:
            print("元文書の単語数が少なすぎるため、目標語彙数の推定を行えません。")
            return len(set(self.words))

        log_x = math.log(self.word_count)
        # 20210501のデータで多項式回帰 TODO 学習データ増やす
        perdicted_vocab_size = self.word_count * (math.e ** (-0.01237875*(log_x**2) + -0.30082554*log_x + 1.8402359926153995))

        print(int(perdicted_vocab_size))
        perdicted_vocab_size = self.word_count * (math.e ** (-0.01755446*(log_x**2) + -0.16824135*log_x + 1.0489287366343656))
        print(int(perdicted_vocab_size))
        
        return int(perdicted_vocab_size)

    def vocab_size_increase(self) -> Tuple[bool, pd.Series]:
        vocab_size = len(self.words.keys())
        
        if vocab_size >= self.vocab_size_goal:
            print("すでに目標の語彙数に達しています。")
            return (False, self.sr)

        noun_dic = loadPickle("lib/Noun_dic.pickle")
        verb_dic = loadPickle("lib/Verb_dic.pickle")
        adj_dic = loadPickle("lib/Adj_dic.pickle")

        while vocab_size < self.vocab_size_goal:
            """a番目の文書のb番目の単語が2回以上出現する単語ならば、別単語で置き換える"""
            # TODO 
            random_index = random.randrange(0, len(self.sr))
            sentence = self.sr[random_index]
            
            
            table = str.maketrans({
                '\n': '',
                '\u3000': '',
                # 半角スペースだと形態素解析でうまくいかなかったため、全角スペースに変換
                # https://qiita.com/trtd56/items/2f62a390eb8fab92e801
                # ' ':'　'
            })
            sentence = sentence.translate(table)

            parsed_sentence = self.tagger.parse(sentence).split('\n')
            surfaces = [line.split("\t")[0] for line in parsed_sentence[:-2]]
            hinshis = [line.split("\t")[1].split(",")[0] for line in parsed_sentence[:-2]]
            katsuyokeis = [line.split("\t")[1].split(",")[5] for line in parsed_sentence[:-2]]
             
            b = random.randrange(0, len(surfaces))
            select_conditions = ["名詞", "動詞", "形容詞"]
            # TODO bのインデックスアクセスをやめたい
            try:
                if hinshis[b] not in select_conditions or self.words[surfaces[b]].count < 2:
                    continue
            except KeyError: # TODO KeyErrorの原因探る
                continue

            try:
                if hinshis[b] == "名詞":
                    surfaces[b] = random.choice(noun_dic[len(surfaces[b])])
                elif hinshis[b] == "動詞":
                    surfaces[b] = random.choice(verb_dic[len(surfaces[b])][katsuyokeis[b]])
                elif hinshis[b] == "形容詞":
                    surfaces[b] = random.choice(adj_dic[len(surfaces[b])][katsuyokeis[b]])
            except:
                continue

            if self.words.get(surfaces[b]):
                self.words[surfaces[b]].count += 1
            else:
                self.words[surfaces[b]] = Word(hinshis[b], katsuyokeis[b])
        
            new_sentence = "".join(surfaces)
            self.sr[random_index] = new_sentence
            vocab_size = len(self.words.keys())

        return (True, self.sr)
