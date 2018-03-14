---
layout:     post
title:      "BAYESTAR：用贝叶斯方法确定引力波事件位置"
subtitle:   "选课手贱的后果"
date:       2017-06-12
author:     "Mingjie"
header-img: "img/post-bg-GW.jpg"
tags:
    - astro-ph
---

**我不是做引力波的，所以以下写的可能有错误，请留意。**

手贱选了物理系的一门引力波课（只要4周！两学分！）；最后要做个报告，看了两周微分几何之后原理方面还是不会，就只能讲观测的了。现在天文方面的引力波观测不外乎两个方面：确定事件的位置和电磁波谱(EM)的跟踪观测。

最早是想讲讲EM观测的策略的，毕竟现在给出90%置信范围区域一般有几百平方度，如果有好的策略尽快找出对应体还是可以的。但是现在情况是各个天文台各自为战，有不同的策略（而且还没有结果）；还看了一篇教你如何将天区排序的[文章](http:\\adsabs.harvard.edu/abs/2017ApJ...838..108R)，感觉有点太简单，就转向了确定引力波事件的位置的方法。

![](/img/in-post/post-GW/1-position-1509.png)
*GW150914的位置概率分布； 来自参考文献1*

确定引力波事件位置的方法有不少，比如上图中的cWB、LIB、BAYSTEAR和LALInforence。它们准确度依次上升，当然用时依次增加。cWB和LIB在引力波事件发生后的不久（17分钟和14小时后）就给出了天球上的位置概率分布(sky map)，并在检查完毕也就是事件发生的两天之后发给了准备做follow-up的天文台。BAYSTEAR和LALInforence用时比较长，特别是LALInforence一般要100个小时。虽然LIGO认为LALInforence的结果是最准的，但是这两个方法的sky map直到那次运行结束之后才被放出来；这导致了所有的follow-up都是根据cWB和LIB做的。

cWB、LIB和LALInforence的原理我不清楚，所以不敢说，但是BAYSTEAR用了贝叶斯方法去确定位置的概率分布；它具有比较强的适用性，可以在比较短的时间内得到和LALInforence差不多的效果。同时BAYSTEAR可并行，缩短运行时间；或者对结果精度不满意的话也可以把更完整的数据丢进去。（加上它不怎么涉及引力波理论:)）所以我仔细看了BAYSTEAR[这篇文章](http:\\arxiv.org/abs/1508.03634)，把其中的过程在这里说一下。

### 基础

首先介绍一些基础概念：探测器收到的信号等于引力波源发出的信号加上探测器的噪音，也就是signal=source+noise。用数学语言描述的话就是

$$y_i(t)=x_i(t;\boldsymbol{\theta})+n_i(t)$$

当然我们之后主要会在频域说事，所以

$$Y_i(\omega)=X_i(\omega;\boldsymbol{\theta})+N_i(\omega)$$

同时我们把所有探测器接收到的引力波集合称为

$$\textbf{Y}(\omega)={Y_i(\omega)}_i$$

这里的$$ \boldsymbol{\theta} $$是引力波源的参数，包括位置、时间、质量、自转等等。如果我们忽略轨道偏心率、潮汐变形，认为两个子星的自转是平行的或者没有自转，那么

$$ \boldsymbol{\theta} = [\alpha, \delta, r, t, l, \psi, \phi_c; m_1, m_2, \textbf{S}_1, \textbf{S}_2] $$

前七个分别是赤经、赤纬、距离、引力波到达地球的时间、系统的倾斜角等外禀参数；后面四个双星的质量和它们各自的自转角动量（内禀参数）。我们关心的是前两个参数。

理论上，因为引力波干涉仪没有指向，所以一个探测器完全不能限制源的位置、两个可以限制到一个圆上、三个是对称的两个点。如果我们也考虑引力波的振幅和相位的话，这两个参数也能提供一些位置的限制，所以之前那幅图里面并不是一个完整的圆。实际上我们想要求的是一个在天上的概率分布图\\( f(\alpha, \delta) \\)，以\\( \alpha \\)和\\( \delta \\)为自变量。当然这个概率分布图是以观测为基础的，所以这是一个条件概率

$$ p(\alpha, \delta) = p(\alpha, \delta | \boldsymbol{Y}(\omega)) $$

这个概率并不好算，所以现在就是让贝叶斯出场的时候了

$$ p(\alpha, \delta | \boldsymbol{Y}(\omega)) = \frac{p(\boldsymbol{Y}(\omega) | \alpha, \delta)p(\alpha, \delta)}{p(\boldsymbol{Y}(\omega))} $$

留意到这里只有\\( \alpha, \delta \\)这两个参数，但是加上其他参数的条件概率会更容易被估计，所以我们将\\( \alpha, \delta \\)换成\\( \boldsymbol{\theta} \\)然后把不关心的参数全部积分掉，得到想要的条件概率；同时\\( \boldsymbol{Y}(\omega)\\)作为事件的先验是一个确定的数，在计算概率的时候也并不关心，可以扔掉。所以

$$ p(\alpha, \delta | \boldsymbol{Y}(\omega)) \propto \int p(\boldsymbol{Y}(\omega) | \alpha, \delta, \boldsymbol{\theta}_\mathrm{other})p(\alpha, \delta, \boldsymbol{\theta}_\mathrm{other}) d\boldsymbol{\theta}_\mathrm{other} $$

之后的任务就是计算上式中的两个概率了。

### $$ p(\boldsymbol{Y}(\omega) | \alpha, \delta, \boldsymbol{\theta}_\mathrm{other}) $$

定义noise的one-sided power spectral density为

$$ S_i(\omega) = 2\mathrm{E}[|N_i(\omega)|^2] $$

假设noise是高斯分布，而且不同探测器之间的noise是互不关联的，我们有

$$ p(\boldsymbol{Y}(\omega)|\boldsymbol{\theta}) = \prod_i p(Y_i|\theta) \propto \exp[-\frac{1}{2} \sum_i \int_0^\infty \frac{|Y_i(\omega)-X_i(\omega;\boldsymbol{\theta})|^2}{S_i(\omega)}d\omega] $$

频率中的连乘变成了\\( e \\)指数中的求和，然后将\\( N_i \\)消掉就行。现在一个概率变成了三项，\\( S_i \\)已经有定义了，要求的是\\( Y_i(\omega) \\)和\\( X_i(\omega;\boldsymbol{\theta}) \\)。

#### $$ X_i(\omega;\boldsymbol{\theta}) $$

我们进一步简化模型：假设并合的双星拥有一个稳定轨道，那么根据（一篇我没有读过的）文献，

$$ X_i(\omega;\boldsymbol{\theta}) = \frac{r_{1,i}}{r}e^{-i\omega(t-\boldsymbol{d}_i\boldsymbol{n})}e^{2i\phi_c}[\frac{1}{2}(1+\cos{l}^2)\Re(\zeta)-i\cos{l}\Im(\zeta)]H(\omega;\boldsymbol{\theta}_\mathrm{in}) $$

这里我们把\\( X_i(\omega;\boldsymbol{\theta}) \\)分成了两部分，前面一长串只跟外禀参数有关，后面的\\( H \\)只和内禀参数有关。但是在观测的时候比较容易得出的是波形的振幅\\( \rho_i \\)、相位\\( \gamma_i \\)和时间\\( \tau_i \\)，所以我们可以用这三个参数代替原来的7个外禀参数，使得，

$$ X_i(\omega; \boldsymbol{\theta}_\mathrm{ex}, \boldsymbol{\theta}_\mathrm{in} =  X_i(\omega; \rho_i, \gamma_i, \tau_i, \boldsymbol{\theta}_\mathrm{in})) = \frac{\rho_i}{\sigma_i(\boldsymbol{\theta})}e^{i(\gamma_i-\omega\tau_i)}H(\omega; \boldsymbol{\theta}_\mathrm{in}) $$

$$ \sigma_i(\boldsymbol{\theta})^2 = \int_0^\infty\frac{|H(\omega;\boldsymbol{\theta}_\mathrm{in})|^2}{S_i(\omega)}d\omega = \frac{1}{r_{1,i}^2} $$

现在\\( X_i \\)的表达式就有了。

#### $$ Y_i(\omega) $$

这里就是BAYESTAR方法很快的原因：我们用从观测到的波形中用最大似然方法(maximum likehood method)得出的参数$$ \hat{\rho}_i, \hat{\gamma}_i, \hat{\tau}_i, \hat{\boldsymbol{\theta}}_\mathrm{in} $$去代替波形；然后用和刚才对\\( X_i \\)相同的方法展开，得到，

$$ Y_i(\hat{\rho}_i, \hat{\gamma}_i, \hat{\tau}_i, \hat{\boldsymbol{\theta}}_\mathrm{in}) = \frac{\hat{\rho}_i}{\sigma_i(\boldsymbol{\hat{\theta}_\mathrm{in}})}e^{i(\hat{\gamma}_i-\omega\hat{\tau}_i)}H(\omega; \boldsymbol{\hat{\theta}_\mathrm{in}})$$

因为我们并不关心内禀参数究竟是什么，所以令\\( \boldsymbol{\theta_\mathrm{in}} = \boldsymbol{\hat{\theta}_\mathrm{in}} \\)，并将\\( X_i, Y_i \\)代入\\( p(Y_i(\omega)\|\boldsymbol{\theta}) \\)中，会得到自相关函数：

$$ p(Y_i(\omega)|\boldsymbol{\theta}) = p(\hat{\rho}_i, \hat{\gamma}_i, \hat{\tau}_i | \rho_i, \gamma_i, \tau_i) \propto \exp{[-\frac{1}{2}\hat{\rho}_i^2 -\frac{1}{2}\rho_i^2} + \hat{\rho}_i\rho_i\Re{\{e^{i \tilde{\gamma}_i}a_i^*(\tilde{\tau_i})\}}] $$

其中

$$ \tilde{\gamma}_i = \hat{\gamma}_i - \gamma_i, \tilde{\tau}_i = \hat{\tau}_i - \tau_i $$

$$ a_i(t;\boldsymbol{\theta}_\mathrm{in}) = \frac{1}{\sigma_i^2(\boldsymbol{\theta}_\mathrm{in})} \int_0^\infty \frac{|H(\omega;\boldsymbol{\hat{\theta}}_\mathrm{in})|^2}{S_i(\omega)}e^{i\omega t}d\omega $$

这只是一个探测器的，将所有探测器的概率乘起来就等于在指数函数中的每一项加上一个求和号；同时留意到\\( \hat{\rho}_i \\)是一个常数，所以也可以扔掉：

$$ p(\hat{\rho}_i, \hat{\gamma}_i, \hat{\tau}_i | \rho_i, \gamma_i, \tau_i) \propto \exp{[-\frac{1}{2}\sum_i\rho_i^2} + \sum_i\hat{\rho}_i\rho_i\Re{\{e^{i \tilde{\gamma}_i}a_i^*(\tilde{\tau_i})\}}] $$

一半搞定。

### $$ p(\alpha, \delta, \boldsymbol{\theta}_\mathrm{other}) d\boldsymbol{\theta}_\mathrm{other} $$

取得\\( \boldsymbol{\theta} \\)的先验并不明确，因为我们并不知道引力波事件在参数空间的哪些参数中比较常见。那就平均呗，在所有可能的取值中平均就好了。所以先验可以表为：

$$ r^md\phi_cdrdtd\cos{l}d\psi $$

### 结果

把这两个概率的结果塞进去原来的\\( p(\alpha,\delta) \\)里面就得到最终的结果：

$$ p(\alpha,\delta) = \int_0^\pi \int_{-1}^1 \int_{-T}^T \int_{r_{min}}^{r_{max}} \int_0^{2\pi} \exp{[-\frac{1}{2}\sum_i\rho_i^2 + \sum_i\hat{\rho}_i\rho_i\Re{\{e^{i \tilde{\gamma}_i}a_i^*(\tilde{\tau_i})\}}]} r^md\phi_cdrdtd\cos{l}d\psi $$

把它用计算机算出来就行了。

### 一些比较

![](/img/in-post/post-GW/2-cumu-p.png)
*BAYSTAR（紫色）和LALInference（蓝色）的在不同年份不同探测器组合下模拟的累计概率。H：LIGO Hanford，L：LIGO Livingston，V：Virgo；来自参考文献1*

根据上图可以看到BAYSTAR和LALInference基本上有相似的表现，除了16年HLV的组合之外。作者认为这是因为三个探测器的信号都进入了LALInference，但是某一个信号太弱，没有进到BAYESTAR里面，所以BAYSTAR的表现比较差。但是如果去点掉这些情况的话，两个方法的表现回到了相似的水平。

![](/img/in-post/post-GW/3-time.png)
*BAYESTAR在不同线程数下的用时；来自参考文献1*

时间方面，BAYESTAR的用时要远远短于LALInference。单线程的话仅需100秒左右，如果32线程的话时间会缩减到4秒到10秒；而LALInference的用时在100个小时左右。但是BAYESTAR需要先计算出\\( Y_i \\)的参数，不知道这个时间有没有算在内。当然如果不用参数直接用信号来计算的话时间应该会变长，但是我觉得还是会比LALInference短。

### 后记

打公式真累。不过要是今天不搞完以后可能就忘了。Stefen Ballmer教授的讲课比较清晰，跟上并不太难；不过由于自己水平太渣加上教授的字迹太瞎眼（无论板书还是笔记），最终决定从微分几何开始学起，最后对引力波原理也不怎么熟悉，只能挑一篇简单的论文讲一讲。不过也算是趁此机会看了看梁灿彬老师的[视频课](https://www.bilibili.com/video/av1157024/?from=search&seid=10126358752879864979)和书（也很清晰易懂！)，准备pre的时候各种用贝叶斯，也是学到了不少东西。

### 参考文献

1.  Singer, L. P. & Price, L. R. Rapid Bayesian position reconstruction for gravitational-wave transients. *Physical Review D* **93**, (2016).
2.  Abbott, B. P. et al. Localization and Broadband Follow-up of the Gravitational-wave Transient GW150914. *The Astrophysical Journal Letters* **826**, L13 (2016).
3.  Aasi, J. et al. First Searches for Optical Counterparts to Gravitational-wave Candidate Events. *The Astrophysical Journal Supplement Series* **211**, 7 (2014).
