---
layout:     post
title:      "别人的关于proposal的经验"
subtitle:   "提案があれば散歩しましょう。"
date:       2019-08-04
author:     "mingjie"
header-img: "img/post-contri_func.png"
tags:
    - learning

---

## AAS的proposal hints

这里以内容为标准将里面的hints分类列出。

1. 扩充经费/观测项目来源，多盯着各种各样的项目和望远镜
2. 阅读各个望远镜的网页、保持关注并熟悉申请程序
3. Proposal不是ApJ论文（报告发现的文章），而是去说服评审委员会的文件；它是专为评审委员会写的
- 评审委员会的人不一定（或者说基本上不是）自己这个领域的人，要关注big picture，不要写得太难
- 让信得过的同行评价你的proposal；如果其他人看不懂的话，评审委员会就肯定看不懂
4. 搞清楚为什么要去做这个研究，它对这个领域的重要性，它和其他研究的联系、相似和**不同**之处
- 最好让人过目不忘
6. proposal被否掉是正常的；接受它并让它作为你的经验
- 一个正向的方法是先去看看公开的proposal是长什么样子的
7. 有机会的话加入评审委员会
8. 注意proposal的排版，比如图片和表格
- 适当使用，让人精神一振以及强调独特之处
9. 做可行性分析并给出结果
10. 给自己充足的时间

## 实际的例子

### 是什么？
**我要解决什么问题？为了解决它具体要做什么？**

氦丰度的变化对10830的氦线有什么影响？
我想观测一个疏散星团、一个球状星团中恒星参数相似的恒星，来看看它们的He10830线有没有不同，或者通过He10830线拟合出来的氦丰度有没有不同。

### 为什么？
氦元素的丰度是一个很基本的物理量；它由宇宙大爆炸的物理过程决定，受恒星核合成过程影响。所以恒星之间的氦丰度差异反映了恒星形成的先后顺序，也就是具体的银河系恒星形成历史。
恒星形成的先后顺序也就是银河系恒星形成历史为我们了解银河系的形成提供了重要的信息：球状星团赫罗图中的多重主序/红巨星支改变了“星团成员星都是同时形成的”的结论，最近关于bulge红团簇星分布与形成的争论也可以由恒星探测恒星的氦丰度来解决。
但是恒星的氦丰度非常难测量，特别是作为银河系结构、演化探针在银河系中大量存在的低温恒星，因为低温恒星的温度不足以激发氦的共振线，所以它们的氦丰度一直都未被确定。
星震学观测可以确定恒星的氦丰度，但是需要长时间高精度的观测，在未来的10(**Really?**)年内只有Kepler天区的恒星可以进行这样的测量。
反之，氦元素在近红外唯一的谱线提供了测量氦丰度的可能性。这条谱线形成机制比较复杂，而且在色球层中形成，所以在一段时间内没有受到重视。
但是Dupree的系列研究和我的初步结果表明，只要恒星的色球层模型可以被其他的色球层谱线确定，He10830线的强度是和氦丰度有关系的。
为了进一步验证这个关系，我们需要一组有相似氦丰度和一组有明显不同的氦丰度的样本来研究He10830线的行为。Kepler天区中氦丰度被确定了的疏散星团以及有明显G2的球状星团巨星就是很好的候选源。

另一个东西是我们还可以统一地确定球状星团的元素丰度。

### 怎么做？
观测约各10颗球状星团和疏散星团的红巨星/红团簇星，通过附近的色球层线确定色球层模型，再通过He10830线的轮廓确定它们的氦丰度。

### 技术细节

#### 我们申请的是什么时间段什么望远镜的什么设备？

| 项目 | Subaru | IRTF |
|:--:|:--:|:--:|
|时间段| S20A: 2020.2.1-7.30 | S20A: 2020.2.1-7.30 |
| 设备 | IRCS | iSHELL |
|Ref| [Subaru](https://www.naoj.org/Observing/Proposals/Submit/call.html) | [IRTF](http://irtfweb.ifa.hawaii.edu/observing/applyingForTime.php) |

这个时间段以及地理位置决定了我们只能观测北半球的春季星空。可以接受的时间段是4.20-7.1，最好的时间段是5.15-7.1。

#### 我们需要观测哪些恒星？

这里我们用TOPCAT抽取Gaia数据来看看它们的颜色星等图，看看它们有多亮。

我们当然想观测NGC6791；它属于北半球春季星空，4-7月左右都可以观测。
除此之外我们需要一些有明显不同generation的球状星团。

NGC6656(good) - M22: complex star generation

NGC6838(good)

NGC6254(okay)

NGC5272(good) - M3：有明显的双red clump？

NGC5904(okay)

#### 它们之前被观测过吗？

| Cluster | Subaru<br>[website](https://smoka.nao.ac.jp/) | IRTF<br>[website](https://irsa.ipac.caltech.edu/applications/irtf/) |
|:--:|:--:|:--:|
|NGC6791|Only two stars, so not yet.|No.|
|NGC6656|No|No|
|NGC6838|Only 3 stars|No|
|NGC6254|No|No|
|NGC5272|No|No|
|NGC5904|Only observed as a whole once in 2016. |No|

#### 我们要观测多少颗星？

这是个大问题。

或者我们做HST的psf测光，直接挑出不同区域的恒星。
  -- 这应该可以；HST观测的是星团非常中心的部分(<3')，而2MASS在中心污染非常多。

从红外的CMD来看的话G1和G2的恒星应该是比较弥散的，所以只要在颜色方向上延伸得够长就可以了，不用具体区分G1G2。有一个担心的是中间的恒星会不会被污染，不过既然2MASS有那么应该就没问题。
在[IRAC finder chart](https://irsa.ipac.caltech.edu/applications/finderchart/)里面看2MASS的图像还是很可以的，污染不多。

#### 一共需要多长时间？

我们的观测时间是2月-7月之间，夜晚长度为8个小时.

##### Subaru

我们首先确定一个可观测星等的下限。

Subaru的proposal以四个小时和5晚为限，由短至长分别分为Service, Normal和Intensive program。我们这里先以normal program为限，也就是申请5晚的观测时间。这样一共是40个小时，除去目标不高以及overhead的时间，暂时以35个小时为限。我们希望总共能观测20颗星。那么每颗星的曝光时间为6300秒。
我们将使用zJ-band（[IRCS帮助文档](https://subarutelescope.org/Observing/Instruments/IRCS/IRCSum_1.0.1.pdf)P22）。从时间上来看我们只能用10000的分辨率，20000耗时太长。信噪比在50到100之间，达不到100；70应该是极限了。

NGC6791的红巨星星等为12.5，红团簇星星等为12.3。10颗星可以，每颗星大概5000秒

球状星团里面比较值得关注的是NGC6838以及NGC6656。NGC6838是因为它的年龄比较小，有清晰且较亮的red clump；而NGC6656整体较亮，可以观测更多的恒星。不过除了NGC6838之外其他球状星团的horizontal branch都太暗了，观测不了。

仅从RGB的比较来说的话我认为NGC6656是个更好的选择，因为HST的观测表明它有大于两个stellar generation，结果应该会更有趣。

姑且仍然按照NGC6791的设置，一颗12等的星需要3000秒；这么看来应该可以观测15到20颗星。足够了。

总计起来10颗5000s的加上20颗3000s的，一共是30个小时。

##### IRTF

似乎是IRTF容易申一点？

IRTF的分辨率在slit width 1.5"时为19000，所以我们就用1.5"。3000s的积分时间可以达到12.5等，参照Subaru的情况4晚上足够了。

从[用户手册](http://irtfweb.ifa.hawaii.edu/~ishell/iSHELL_observing_manual_22aug19.pdf)P5上可以得知slit长度最短可以为0.5角秒。


嘛事实证明Milone那帮人已经做了球状星团的He丰度。所以我们需要换一下目标，用他们的结果来。

我们要求有效温度大于4500，对应Gbp-Grp小于1.5.

[Subaru](https://www.naoj.org/Observing/Instruments/IRCS/echelle/IRCS_Echelle_ETC.html)
[IRTF](http://irtfweb.ifa.hawaii.edu/~ishell/iSHELL_Exposure_Time_Calculator/sn.php)

## Refs

https://aas.org/grants-and-prizes/hints-preparing-research-proposals
