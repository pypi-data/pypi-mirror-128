import math
from typing import List, Iterable, Tuple

import numpy as np


def calc_cos_sim(vector_a: Iterable[float], vector_b: Iterable[float]) -> float:
    """计算两个列向量之间的余弦相似度"""
    num = np.sum(np.array(vector_a) * np.array(vector_b))
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    if denom == 0:  # 任何一个向量的模为0时直接返回0，防止返回Nan
        return 0.0
    cos = num / denom
    return cos


def calc_idf(word: str, all_docs: List[str]) -> float:
    """计算某个word相对于多篇文章的IDF值"""
    idf = math.log(len(all_docs) / (1 + len([doc for doc in all_docs if word in doc])))
    return idf


def calc_auc(y_true: Iterable[int], y_pred: Iterable[float]):
    """
    针对二分类问题，计算AUC值
    :param y_true: 各样本实际标签
    :param y_pred: 预测出的各样本置信度
    例如：
    y_true = [1] * 3 + [0] * 5
    y_pred = [0.8, 0.7, 0.3, 0.5, 0.6, 0.9, 0.4, 0.2]
    calc_auc(y_true, y_pred)
    输出: 0.6
    """
    rank = [
        l for p, l in sorted(zip(y_pred, y_true), key=lambda x: x[0])
    ]  # 按概率对(概率, 标签)的pair进行升序排序
    # 将label为1的找出来，最大概率对应rank为n，其次为n-1以此类推，最小为1
    i_belongs_positive = [i + 1 for i in range(len(rank)) if rank[i] == 1]
    pos_num = neg_num = 0
    for t in y_true:
        if t == 1:
            pos_num += 1
        else:
            neg_num += 1
    auc = (sum(i_belongs_positive) - (pos_num * (pos_num + 1)) / 2) / (
        pos_num * neg_num
    )
    return auc


def calc_precision_recall_f1(
    y_true: Iterable[int], y_pred: Iterable[int]
) -> Tuple[float, float, float]:
    """
    针对二分类问题，计算精确率、召回率和F1值
    :param y_true: 各样本实际标签
    :param y_pred: 各样本预测标签
    """
    tp, fp, fn = 0, 0, 0
    for t, p in zip(y_true, y_pred):
        if t == p == 1:
            tp += 1
        elif t == 0 and p == 1:
            fp += 1
        elif t == 1 and p == 0:
            fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 / (1 / precision + 1 / recall)
    return precision, recall, f1
