---
layout:     post
title:      "加权平均值的误差"
subtitle:   "the error of the weighted mean"
date:       2019-12-06
author:     "mingjie"
header-img: "img/post-contri_func.png"
tags:
    - learning

---

我受不了了。

究竟加权平均值的误差的表达式应该是什么？这个问题困扰了我很久。今天决定用实验去解决它。

## 问题

### 古典描述

我们想测量一个物理量；它有一个真值$$ \hat{x} $$。我们对它进行$$ N $$次测量，每次测量用下标的$$ i $$来表示，也就是$$ x_i $$。因为每次测量的环境都不同（仪器温度变了啊、天气变阴了啊、观测助手抖腿了啊、隔壁猫叫了啊、etc），每次测量的误差$$ \sigma_i $$都不一样。误差是怎么估计的也是一个大问题，但这里就直接给定了。那么当我们用加权平均去估计这个物理量的值的时候，这个估计值的误差是多少？

### 贝叶斯描述

我们测量一个物理量，测了好多次。每次都有一个测量值$$ x_i $$以及它的误差$$ \sigma_i $$。怎么样利用这些测量值和误差给出这个物理量的参数的限制呢？这里没有真值。

## 古典方法

我不会。但是有些地方给出了结论：

先定义权重：

$$ w_i = \frac{1}{\sigma_i^2} $$

那么加权平均值就是

$$ \mu = \frac{\sum w_i x_i}{\sum w_i} $$

1. Weight sample variance

$$ \sigma^2 = \frac{\sum w_i}{(\sum w_i)^2 - \sum w_i^2} \sum w_i (x_i - \mu)^2 $$

来自[维基百科](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Reliability_weights)以及[GNU Project](https://www.gnu.org/software/gsl/doc/html/statistics.html)。

2. From error propagation

$$ \sigma^2 = \frac{1}{\sum 1 / \sigma_i^2} $$

来自[STATISTICS AND THE TREATMENT OF EXPERIMENTAL DATA](https://ned.ipac.caltech.edu/level5/Leo/Stats4_5.html)以及[维基百科](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean)的error of the weighted mean部分。

它们在误差分布比较正常的时候结果是一样的。

## 贝叶斯方法
