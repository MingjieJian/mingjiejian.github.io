---
layout:     post
title:      "统计三连之一"
subtitle:   "如何拟合"
date:       2018-03-23
author:     "mingjie"
header-img: "img/post-bg-DL-1.jpg"
tags:
    - learning

---

来自David W. Hogg的书。

拟合一条直线不容易。通常的加权最小二乘法拟合的前提是：数据的一个轴的误差可忽略，而另一个各个点的误差可以被已知方差的高斯分布所描述，这不一定能被满足。所以下面所说的内容就提供一个更好的方法。当然怎么更好我还不知道。

### 前言

线性拟合基本上是错而且非必须的。首先两个观测得到的数据真的存在一个线性的、窄的关系的情况很少很少。第二即使它看起来线性，除非有坚实的物理基础，实际上也不一定就线性了。那你拿线性关系去拟合肯定是会带来偏差的。而非必须指的是，你最后的结果一般不是那个斜率和截距；数据点本身可能会更有价值。当然需要利用关系去预测新的数据的情况也有，但是比较少见；这个时候模型本身的正确性就不是很重要了。

在这里我们提供一种合理的拟合方法。

### 理想状态

理想状态当然是数据的一个轴的误差可忽略，而另一个各个点的误差可以被已知方差的高斯分布所描述了。假设我们有$$ N $$个数据点，那么我们可以这么来描述：

$$
\begin{align}
  Y &=
  \begin{bmatrix}
    y_1 \\ y_2 \\ \vdots \\ y_N
  \end{bmatrix}, \\
  X &=
  \begin{bmatrix}
    x_1 & 1 \\ x_2 & 1 \\ \vdots & \vdots \\ x_1 & 1
  \end{bmatrix},\\
  C &=
  \begin{bmatrix}
    \sigma_{y_1}^2 & 0 & \cdots & 0 \\
    0 & \sigma_{y_2}^2 & \cdots & 0 \\
    \vdots \\
    0 & 0 & \cdots & \sigma_{y_N}^2 \\
  \end{bmatrix} \\
  A &=
    \begin{bmatrix}
    m \\ b
    \end{bmatrix} \\
\end{align}
$$

我们要求的是使得$$ \chi^2 $$最小的$$ A $$。因为$$ Y = XA $$，我们先乘上一个$$ C^{-1} $$（加权平均），再乘一个$$ X^T $$（减小维数），就得到了：

$$ A = [X^TC^{-1}X]^{-1} [X^TC^{1}Y] $$

## 预测值的置信区间以及预测区间

[请看这里](https://www.youtube.com/watch?feature=player_embedded&v=qVCQi0KPR0s)
