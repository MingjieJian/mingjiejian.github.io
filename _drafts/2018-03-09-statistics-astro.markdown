---
layout:     post
title:      "统计与天文的阅读笔记"
subtitle:   "更新自己未老先衰的心"
date:       2018-03-09
author:     "mingjie"
header-img: "img/post-bg-jpynb.jpg"
tags:
    - learning

---

### 一切的起源：[这个知乎回答](https://www.zhihu.com/question/266225629)

#### 什么是Forward modeling/backward modeling？

根据[这里](https://astronomy.stackexchange.com/questions/19687/what-does-forward-modeling-mean)的回答，正向建模指的是我们先造出一个模型，然后根据这个模型和物理规律算出一些量或者状态。而反向建模指的是我们有观测数据（物理量/状态），通过观测数据寻找一个和合适的模型。

但是这样说的话我体会不到正向建模的重要性，反而我觉得反向建模是数据+正向建模。没有观测数据支撑只是在那建模有什么意义呢？第二我觉得我们很早就开始正向建模了啊，恒星的模型不就是从物理规律和初始状态来的么。


在FW中我们会用到什么样的技术？

#### 什么是Bayesian统计？
http://www.xuyankun.cn/2017/05/13/bayes/

作者首先说概率是说不清的，举了个例子说丢一枚硬币正面朝上的概率不一定是50%的。但是这如何说明这句话的意思呢？
> 什么是概率这个问题似乎人人都觉得自己知道，却有很难说明白。比如说我问你 掷一枚硬币为正面的概率为多少？

我也可以认为这个概率是客观存在的但是我们永远都只能用实验逼近这个数而已。不过先继续看下去吧。

> 掷硬币的例子说明了古典统计学的思想，就是概率是基于大量实验的，也就是**大数定理**。

##### 什么是大数定理？

大数定理其实讲的就是刚刚的东西，我们可以用实验逼近概率这个数。也就是在实验次数很多的情况下，结果的平均值应该无限逼近期望值。其中期望值需要勒贝格可积、不过方差不一定要有限。一个反例是在-90到+90均匀分布的角度的正切值，它的期望无限，自然就不符合大数定理的条件。
对于其他细节[英文维基百科](https://en.wikipedia.org/wiki/Law_of_large_numbers)有很详细的描述。

了解了这个之后接下来作者的提问就好理解了：

> 明天下雨的概率是30%；A地会发生地震的概率是5%；一个人得心脏病的概率是40%…… 这些概率怎么解释呢？

的确古典概率不能解释这些概率。那什么东西能解释呢？就要从贝叶斯公式讲起了。

##### 贝叶斯公式

贝叶斯公式是条件概率的一个推论；只要我们承认$$ P(A \vert B) = \frac{P(A, B)}{P(B)} $$就好办了。$$ P(A, B) = P(A \vert B)P(B) = P(B \vert A)P(A) $$。所以

$$ P(A \vert B) = \frac{P(B \vert A)P(A)}{P(B)} $$

当然还有一种二中择一的形式：

$$ P(B) = P(A, B) + P(\bar{A}, B) = P(B \vert A)P(A) + P(B \vert \bar{A})P(\bar{A}) $$

$$ P(A \vert B) = \frac{P(B \vert A)P(A)}{P(B \vert A)P(A) + P(B \vert \bar{A})P(\bar{A})} $$

将里面的$$ A $$从二中择一推广到连续变量，就得到了究极 贝叶斯公式：

$$ P(A \vert B) = \frac{P(B \vert A)P(A)}{\int_A P(B \vert A)P(A) dA} $$

然后再用参数$$ \theta $$和观测数据$$ x $$分别代替$$ A, B $$，最终的究极 贝叶斯公式 改是这样的：

$$ P(\theta \vert x) = \frac{P(x \vert \theta)P(x)}{\int_\theta P(x \vert \theta)P(\theta) d\theta} $$

好了不改了不改了。但是我们怎么去理解这个公式呢？那些平常说的先验后验又是什么呢？

##### 理解贝叶斯公式

------------
什么是MCMC？

看这里：[David Kipping的视频](https://www.youtube.com/watch?v=vTUwEu53uzs)，[slide](https://github.com/davidkipping)
Sagan workshop是个好东西。

什么是Hierarchical Bayesian modeling？

什么是Gaussian process？

什么是Bootstrap？

天文领域里面有什么例子？

https://arxiv.org/abs/1008.4686 某个人的model fitting介绍。他还有有关MCMC的。


## 如何判断两个样本的平均数是否一致？

[看这里](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)

## 如何判断两个模型哪个更好？

用AIC或者[F-test](http://people.reed.edu/~jones/Courses/P24.pdf)

## 如何通过平均分布产生任意的分布？

[看这里](http://blog.codinglabs.org/articles/methods-for-generating-random-number-distributions.html)
CDF和PDF的关系在[这里](https://zh.wikipedia.org/wiki/%E7%B4%AF%E7%A7%AF%E5%88%86%E5%B8%83%E5%87%BD%E6%95%B0)
