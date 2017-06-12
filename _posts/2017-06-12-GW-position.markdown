---
layout:     post
title:      "BAYESTAR：用贝叶斯方法确定引力波事件位置"
subtitle:   "选课手贱的后果"
date:       2017-06-12
author:     "Mingjie"
header-img: "img/post-bg-GW.jpg"
tags:
    - Learning
---

**我不是专门做引力波的，所以以下写的可能有错误，请留意。**

手贱选了物理系的一门引力波课（只要4周！两学分！）；最后要做个报告，看了两周微分几何之后原理方面还是不会，就只能讲观测的了。现在天文方面的引力波观测不外乎两个方面：确定事件的位置和电磁波谱(EM)的跟踪观测。

最早是想讲讲EM观测的策略的，毕竟现在给出90%置信范围区域一般有几百平方度，如果有好的策略尽快找出对应体还是可以的。但是现在情况室各个天文台各自为战，有不同的策略（而且还没有结果）；还看了一篇教你如何将天区排序的[文章](http://adsabs.harvard.edu/abs/2017ApJ...838..108R)，感觉有点太简单，就转向了确定引力波事件的位置的方法。

![](/img/in-post/post-GW/1-position-1509.png)
*GW150914的位置概率分布*

确定引力波事件位置的方法有不少，比如上图中的cWB、LIB、BAYSTEAR和LALInforence。它们准确度依次上升，当然用时依次增加。cWB和LIB在引力波事件发生后的不久（17分钟和14小时后）就给出了天球上的位置概率分布(sky map)，并在检查完毕也就是事件发生的两天之后发给了准备做follow-up的天文台。BAYSTEAR和LALInforence用时比较长，特别是LALInforence一般要100个小时。虽然LIGO认为LALInforence的结果是最准的，但是这两个方法的sky map直到那次运行结束之后才被放出来；这导致了所有的follow-up都是根据cWB和LIB做的。

cWB、LIB和LALInforence的原理我不清楚，所以不敢说，但是BAYSTEAR用了贝叶斯方法去确定位置的概率分布；它具有比较强的适用性，可以在比较短的时间内得到和LALInforence差不多的效果。同时BAYSTEAR可并行，缩短运行时间；或者对结果精度不满意的话也可以把更完整的数据丢进去。（加上它不怎么涉及引力波理论:)）所以我仔细看了BAYSTEAR[这篇文章](http://arxiv.org/abs/1508.03634)，把其中的过程在这里说一下。

首先介绍一些基础概念：探测器收到的信号等于引力波源发出的信号加上探测器的噪音，也就是signal=source+noise。用数学语言描述的话就是

$$y_i(t)=x_i(t;\theta)+n_i(t)$$

当然我们之后主要会在频域说事，所以

$$Y_i(\omega)=X_i(\omega;\theta)+N_i(\omega)$$
