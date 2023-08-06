"""
车万翔书P24最大正向匹配算法
"""
from typing import List

LEXICON = set()
MAX_LEN = 0
with open("jaikit/data/lexicon.txt") as f:
    for line in f.readlines():
        word = line.strip()
        LEXICON.add(word)
        if len(word) > MAX_LEN:
            MAX_LEN = len(word)


def fmm_word_seg(text: str) -> List[str]:
    begin = 0
    end = min(begin + MAX_LEN, len(text))
    words = []
    while begin < end:
        word = text[begin:end]
        if word in LEXICON or end - begin == 1:
            words.append(word)
            begin = end
            end = min(begin + MAX_LEN, len(text))
        else:
            end -= 1
    return words
