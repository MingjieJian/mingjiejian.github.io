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

最早是想讲讲EM观测的策略的，毕竟现在给出90%置信范围区域一般有几百平方度，如果有好的策略尽快找出对应体还是可以的。但是现在情况室各个天文台各自为战，有不同的策略（而且还没有结果）；还看了一篇教你如何将天区排序的[文章](http:\\adsabs.harvard.edu/abs/2017ApJ...838..108R)，感觉有点太简单，就转向了确定引力波事件的位置的方法。

![](/img/in-post/post-GW/1-position-1509.png)
*GW150914的位置概率分布; 来自参考文献X*

确定引力波事件位置的方法有不少，比如上图中的cWB、LIB、BAYSTEAR和LALInforence。它们准确度依次上升，当然用时依次增加。cWB和LIB在引力波事件发生后的不久（17分钟和14小时后）就给出了天球上的位置概率分布(sky map)，并在检查完毕也就是事件发生的两天之后发给了准备做follow-up的天文台。BAYSTEAR和LALInforence用时比较长，特别是LALInforence一般要100个小时。虽然LIGO认为LALInforence的结果是最准的，但是这两个方法的sky map直到那次运行结束之后才被放出来；这导致了所有的follow-up都是根据cWB和LIB做的。

cWB、LIB和LALInforence的原理我不清楚，所以不敢说，但是BAYSTEAR用了贝叶斯方法去确定位置的概率分布；它具有比较强的适用性，可以在比较短的时间内得到和LALInforence差不多的效果。同时BAYSTEAR可并行，缩短运行时间；或者对结果精度不满意的话也可以把更完整的数据丢进去。（加上它不怎么涉及引力波理论:)）所以我仔细看了BAYSTEAR[这篇文章](http:\\arxiv.org/abs/1508.03634)，把其中的过程在这里说一下。

首先介绍一些基础概念：探测器收到的信号等于引力波源发出的信号加上探测器的噪音，也就是signal=source+noise。用数学语言描述的话就是

$$y_i(t)=x_i(t;\textbf{\theta})+n_i(t)$$

当然我们之后主要会在频域说事，所以

$$Y_i(\omega)=X_i(\omega;\textbf{\theta})+N_i(\omega)$$

同时我们把所有探测器接收到的引力波集合称为

$$\textbf{Y}(\omega)={Y_i(\omega)}_i$$

这里的\\ \textbf{\theta} \\是引力波源的参数，包括位置、时间、质量、自转等等。如果我们忽略轨道偏心率、潮汐变形，认为两个子星的自转是平行的或者没有自转，那么

$$ \textbf{\theta} = [\alpha, \delta, r, t, l, \psi, \phi_c; m_1, m_2, \textbf{S}_1, \textbf{S}_2] $$

分别是赤经、赤纬、距离、引力波到达地球的时间、系统的倾斜角等外禀参数；双星的质量和它们各自的自转角动量（内禀参数）。我们关心的是前两个参数。

理论上，因为引力波干涉仪没有指向，所以一个探测器完全不能限制源的位置、两个可以限制到一个圆上、三个是对称的两个点。如果我们也考虑引力波的振幅和相位的话，这两个参数也能提供一些位置的限制，所以之前那幅图里面并不是一个完整的圆。实际上我们想要求的是一个在天上的概率分布图\\( f(\alpha, \delta) \\)，以\\( \alpha \\)和\\( \delta \\)为自变量。当然这个概率分布图是以观测为基础的，所以这是一个条件概率

$$ p(\alpha, \delta) = p(\alpha, \delta | \mathbf{Y}(\omega)) $$

这个概率并不好算，所以现在就是让贝叶斯出场的时候了

$$ p(\alpha, \delta | \mathbf{Y}(\omega)) = \frac{p(\mathbf{Y}(\omega) | \alpha, \delta)p(\alpha, \delta)}{p(\mathbf{Y}(\omega))} $$

留意到这里只有\\( \alpha, \delta \\)这两个参数，但是加上其他参数的条件概率会更容易被估计，所以我们将\\( \alpha, \delta \\)换成\\( \mathbf{\theta} \\)然后把不关心的参数全部积分掉，得到想要的条件概率；同时\\( \mathbf{Y}(\omega)\\)作为事件的先验是一个确定的数，在计算概率的时候并不关心，可以扔掉。所以

$$ p(\alpha, \delta | \mathbf{Y}(\omega)) \propto \int p(\mathbf{Y}(\omega) | \alpha, \delta, \mathbf{\theta}_\mathrm{other})p(\alpha, \delta, \mathbf{\theta}_\mathrm{other}) d\mathbf{\theta}_\mathrm{other} $$

之后的任务就是计算上式中的两个概率了。

### $$ p(\mathbf{Y}(\omega) | \alpha, \delta, \mathbf{\theta}_\mathrm{other}) $$

定义noise的one-sided power spectral density为

$$ S_i(\omega) = 2\mathrm{E}[|N_i(\omega)|^2] $$

假设noise是高斯分布，而且不同探测器的noise是互不关联的，我们有

$$ p(\mathbf{Y}(\omega)|\mathbf{\theta}) = \prod_i p(Y_i|\theta) \propto \exp[-\frac{1}{2} \sum_i \int_0^\infty \frac{|Y_i(\omega)-X_i(\omega;\mathbf{\theta})|^2}{S_i(\omega)}d\omega] $$

频率中的连乘变成了\\( e \\)指数中的求和，然后将\\( N_i \\)消掉就行。现在一个概率变成了三项，\\( S_i \\)已经有定义了，要求的是\\Y_i(\omega)\\和\\( X_i(\omega;\mathbf{\theta}) \\)

#### $$ X_i(\omega;\mathbf{\theta}) $$

我们进一步简化模型：假设并合的双星拥有一个稳定轨道，那么根据（一篇我没有读过的）文献，

$$ X_i(\omega;\mathbf{\theta}) = \frac{r_{1,i}}{r}e^{-i\omega(t-\mathbr{d_i}\dot\mathbf{n})}e^{2i\phi_c}[\frac{1}{2}(1+\cos{l}^2)\Re(\zeta)-i\cos{l}\Im(\zeta)]H(\omega;\mathbf{\theta}_\mathrm{in}) $$

这里我们把\\( X_i(\omega;\mathbf{\theta}) \\)分成了两部分，前面一长串只跟外禀参数有关，后面的\\( H \\)只和内禀参数有关。但是在观测的时候比较容易得出的是波形的振幅\\( \rho_i \\)、相位\\( \gamma_i \\)和时间\\( \tau_i \\)，所以我们可以用这三个参数代替原来的7个外禀参数，使得，

$$ X_i(\omega; \mathbf{\theta}_mathrm{ex}, \mathbf{\theta}_\mathrm{in} = $$
$$  X_i(\omega; \rho_i, \gamma_i, \tau_i, \mathbf{\theta}_\mathrm{in})) =\frac{\rho_i}{\sigma_i(\mathbf{\theta}e^{i(\gamma_i-\omega\tau_i)}H(\omega; \mathbf{\theta}_\mathrm{in})} $$

$$ \sigma_i(\mathbf{\theta}) = (\int_0^\infty\frac{|H(\omega;\mathbf{\theta}_\mathrm{in})|^2}{S_i(\omega)}d\omega)^\frac{1}{2} = \frac{1}{r_{1,i}} $$

现在\\( X_i \\)的表达式就有了。
