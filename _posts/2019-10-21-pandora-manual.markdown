---
layout:     post
title:      "PANDORA说明书"
subtitle:   "Let's bake it."
date:       2019-10-21
author:     "mingjie"
header-img: "img/post-contri_func.png"
tags:
    - learning

---

* any words
{:toc}

## Section 9：背景谱线不透明度

PANDORA在计算谱线源函数的时候需要知道bakcground opacity，或者说是background continuum。这应该指的是OASP中的连续吸收系数。这一节主要讲的是连续吸收系数中其他谱线的贡献以及计算方式。

如果是同种元素的谱线，那么PANDORA中的"blended line"机制可以搞定；对于其他的谱线，一般PANDORA会考虑H，He-II，CO的谱线（可以在输出的ATMOSPHERE中进行确认）。

## Section 18：合成频率表

这其实就是合成光谱的频率点；PANDORA有内置的一个表，或者通过指定某些频率，我们可以控制合成光谱的采样点分布。这对于一些宽线（比如CaII H&K）有用。
`XISYM`（长度为`KS`）指定一个通用的轮廓，对所有线都生效；`XIBLU`（长度`KB`）指定蓝半边，
