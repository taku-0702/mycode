import pickle
from collections import defaultdict

with open("Noun.csv", encoding="shift-jis") as f:
    noun_list = f.read().splitlines()
    noundic = defaultdict(list)
    for noun in noun_list:
        surface = noun.split(",")[0]
        noundic[len(surface)].append(surface)

with open("Verb.csv", encoding="shift-jis") as f:
    verb_list = f.read().splitlines()
    verbdic = defaultdict(dict)
    for verb in verb_list:
        surface = verb.split(",")[0]
        katsuyokei = verb.split(",")[9]
        if verbdic[len(surface)].get(katsuyokei):
            verbdic[len(surface)][katsuyokei].append(surface)
        else:
            verbdic[len(surface)][katsuyokei] = [surface]

with open("Adj.csv", encoding="shift-jis") as f:
    adj_list = f.read().splitlines()
    adjdic = defaultdict(dict)
    for adj in adj_list:
        surface = adj.split(",")[0]
        katsuyokei = adj.split(",")[9]
        if adjdic[len(surface)].get(katsuyokei):
            adjdic[len(surface)][katsuyokei].append(surface)
        else:
            adjdic[len(surface)][katsuyokei] = [surface]

with open('Noun_dic.pickle', 'wb') as f:
    pickle.dump(noundic, f)

with open('Verb_dic.pickle', 'wb') as f:
    pickle.dump(verbdic, f)

with open('Adj_dic.pickle', 'wb') as f:
    pickle.dump(verbdic, f)