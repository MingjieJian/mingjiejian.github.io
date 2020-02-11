---
layout:     post
title:      "NLTE下的辐射转移和大气模型"
subtitle:   "Avrett 2008 Lecture Note"
date:       2020-02-05
author:     "mingjie"
header-img: "img/post-bg-achi.jpg"
tags:
    - learning

---

* any words
{:toc}

# 基本概念/方程

参考[OASP5](https://mingjiejian.github.io/2017/12/18/OASP5/)。

$$ \mu = \cos{\theta} $$

在各向同性下辐射强度$$ I_\mu $$：

$$ I_\nu = I_\nu(r, \mu) $$

平均辐射强度：

$$ J_\nu = \frac{1}{4\pi} \int I_\nu d\Omega = \frac{1}{2} \int_{-1}^1 I_\nu d\mu $$

单色能量密度：

$$ U_\nu = \frac{4\pi}{c} J_\nu $$

单色天文流量（还是各向同性）：

$$ \pi F_\nu = \int I_\nu \cos{\theta} d\Omega = 2\pi \int_{-1}^1 \mu I_\nu d\mu $$

流量的另一个定义：

$$ H_\nu = \frac{1}{2} \int I_\nu \mu d\mu = \frac{\pi F_\nu}{4\pi} $$

斯特芬-玻尔兹曼定律：

$$ \pi F = \pi \int_{0}^\infty F_\nu d\nu = \sigma T_\mathrm{eff} $$

辐射转移方程(1)：

$$ \frac{dI_\nu}{dl} = -\kappa_\nu I_\nu + \eta_\nu $$

源函数、光深：

$$ S_\nu = \frac{\eta_\nu}{\kappa_\nu}, d\tau_\nu = -\kappa_\nu \mu dl $$

所以辐射转移方程(2)：

$$ \mu \frac{dI_\nu}{d\tau_\nu} = I_\nu - S_\nu $$

这里的$$ \kappa_\nu $$是OASP5中的$$ \kappa_\nu \rho $$。

对上式在$$ \mu $$方向上积分，有：

$$ \frac{dH_\nu}{d\tau_\nu} = J_\nu - S_\nu $$

辐射转移方程的解为（忽略频率下标）：

$$ I(\tau, \mu) =I(0,\mu)e^{-\frac{(0-\tau)}{\mu}} - \frac{1}{\mu} \int_0^\tau e^{-\frac{t-\tau}{\mu}} S(t) dt, ~ \text{inward}$$

$$ I(\tau, \mu) =I(\tau_m,\mu)e^{-\frac{(\tau_m-\tau)}{\mu}} + \frac{1}{\mu} \int_\tau^{\tau_m} e^{-\frac{t-\tau}{\mu}} S(t) dt, ~ \text{outward} $$

因为$$ \tau_m=\infty $$时光射不出来，$$ I(\tau_m,\mu) $$一般不会为指数增长，则在恒星表面向外的光强为

$$ I(0, \mu) = \frac{1}{\mu} \int_0^{\infty} e^{-\frac{t}{\mu}} S(t) dt $$

可以推出当$$ S $$是$$ t $$的线性函数的时候有$$ I(0,\mu) = S(\tau=\mu) $$，这是Eddington-Barbier关系。

参考OASP7的$$ (7.16) $$，引入$$ E $$积分之后平均光强为：

$$ J(\tau) = \frac{1}{2} \int_0^{\tau_m} E_1(|t-\tau|) S(t)dt = \Lambda\{S\} $$

$$ \Lambda $$叫做Lambda opeartor。

$$ \int_0^\infty E_1(t)dt = 1 $$（未证实），所以当$$ S $$为常数的时候在光深大的地方有$$ J=S $$（未证实），在表面有$$ J=\frac{1}{2}S $$。

参考OASP7$$ (7.14) $$，$$ H $$也可以写成$$ E $$积分，以及$$ H(\tau) = \Phi\{S\} $$；同时$$ \int_0^\infty E_2(t)dt = 0.5 $$（未证实），所以当$$ S $$为常数的时候在光深大的地方有$$ H=0 $$（未证实），在表面有$$ H=\frac{1}{4}S $$。当$$ S(\tau) = C_0 + C_1 \tau $$时光深大的时候$$ H \rightarrow (1/3)C_1 $$。

当热动平衡的时候，光强各向同性且由普朗克函数$$ B_\nu(T) $$描述。所有的粒子速度由麦克斯韦分布描述、跃迁由玻尔兹曼方程描述、电离由萨哈-玻尔兹曼方程描述。

LTE下不同层上有不同的温度，所以这个时候只有$$ S_\nu = B_\nu $$，而光强$$ I_\nu $$必须由辐射转移方程通过$$ S_\nu $$计算出来。但是这里讨论的是NLTE，$$ S_\nu \ne B_\nu $$，那么我们如何获得$$ S_\nu $$呢？这就是这个Note要解决的事情了。

# 单色散射

我们先看一个简单的例子，看看怎么从$$ B $$求出$$ S $$来。这里假设原子的散射是各向同性以及不改变光子的频率的，那么根据OASP5中的“纯各向同性散射”有$$ S_\nu = J_\nu $$。我们将辐射转移方程写成LTE部分以及散射部分：

$$
\begin{align}
\frac{dI}{dl} & = -\kappa^{ab} (I-S^{ab}) \\
\frac{dI}{dl} & = -\kappa^{sc} (I-S^{sc}) \\
S^{ab} &= B_\nu, ~ \text{LTE part}\\
S^{ab} &= J_\nu, ~ \text{scatter part}\\
\end{align}
$$

所以

$$ \frac{dI}{dl} = -\kappa^{ab} (I-B) - \kappa^{sc} (I-J) $$

然后我们凑辐射转移方程的形式，令：

$$ d\tau = - (\kappa^{ab} + \kappa^{sc}) \mu dl, \epsilon = \frac{\kappa^{ab}}{\kappa^{ab}+\kappa^{sc}} $$

则有

$$ \mu \frac{dI}{d\tau} = I - S $$

$$
\begin{align}
S &= \epsilon B + (1-\epsilon) J \\
&= \epsilon B + (1-\epsilon) \Lambda\{S\}
\end{align}
$$

这个时候我们发现上式中只有$$ B, S $$，那么我们就可以从$$ B $$求出$$ S $$了。

我们来看看$$ S $$的一些解。将$$ E_1(x) $$用1阶近似$$ \sqrt{3} e^{-\sqrt{3}x} $$代替，有

$$ S(\tau) = (1-\epsilon) \int_0^\infty \frac{\sqrt{3}}{2} e^{-\sqrt{3}|t-\tau|}S(t)dt + \epsilon B $$

当$$ S, \epsilon $$都为常数的时候，有解：

$$ S(\tau) = B [1-(1-\sqrt{\epsilon})e^{-\sqrt{3\epsilon}\tau}] $$

可以代进去验证。它说明了1)$$ S(0) = \sqrt{\epsilon} B $$，2)仅当$$ \tau > 1 / \sqrt{\epsilon} $$的时候（量级上）$$ S \rightarrow B $$。

上述的论证说明了尽管吸收是LTE的，当散射比例比较高的时候（$$ \epsilon $$较小），$$ S $$是不等于$$ B $$的，而是小于$$ B $$，导致了更深处的光也能射出来。同时$$ \frac{1}{\sqrt{\epsilon}} $$为热化长度（LTE与否的判据），虽然下一节会说谱线的热化长度实际上是$$ \frac{1}{\epsilon} $$。

# 谱线辐射 （二能级原子）

这一部分的内容在TSA的14.2中有更详细的描述，这里有的描述会参考那一章。

思路是一样的，从LTE到NLTE。我们从包含辐射以及碰撞平衡的统计平衡方程开始：

$$ n_2(A_{21} + B_{21}\bar{J} + C_{21}) = n_1 (B_{12} \bar{J} + C_12) $$

这里$$ \bar{J} = \int_0^\infty J_\nu \phi_\nu d\nu $$是经过谱线轮廓函数$$ \phi_\nu $$调制的平均光强。在CDR的情况下，$$ \phi_\nu = \frac{1}{\Delta\nu_D \sqrt{\pi}} e^{-\left(\frac{\nu-\nu_0}{\Delta\nu_D}\right)^2}$$是一个高斯函数，并且$$ \Delta\nu_D = \frac{\nu_0}{c} \sqrt{\frac{2kT}{m_a}} $$，$$ m_a $$是吸收光子的原子的质量。$$ A, B, C $$为自发、受激辐射以及碰撞跃迁的爱因斯坦系数。

此时的辐射转移方程为

$$ \frac{dI_\nu}{dl} = -\frac{h\nu}{4\pi} \phi_\nu [(n_1B_{12} - n_2B_{21})I_\nu - n_2 A_{21}] $$

定义光深、吸收系数以及源函数：

$$
\begin{align}
d\tau_\nu &= -\kappa_\nu \mu dl \\
\kappa_\nu &= \frac{h\nu}{4\pi} (n_1B_{12} - n_2B_{21}) \phi_nu = \frac{h\nu}{4\pi} n_1B_{12} (1 - \frac{n_2g_1}{n_1g_2}) \phi_nu \\
S_\nu &= \frac{2h\nu^3}{c^2} \frac{1}{\frac{n_2g_1}{n_1g_2}-1} \\
\end{align}
$$

在热动平衡的情况下，上式的$$ A, B $$系数项相等，有$$ \frac{n_2}{n_1} = \frac{n_2^*}{n_1^*} = \frac{C_{12}}{C_{21}} $$，源函数就退成了$$ B $$。但是我们现在关心的是NLTE的情况，$$ A, B $$系数项不相等导致$$ n $$和$$ C $$的关系不是LTE的情况，所以我们需要把整个统计平衡方程代到源函数里面。经过一段运算之后（我算不出来，TSA说里面的参考文献[721]中有，但是我还没找到），我们可以得出：

$$
\begin{align}
S &= \frac{\bar{J} + \varepsilon B}{1 + \varepsilon} \\
\varepsilon &= \frac{C_{21}}{A_{21}}{1-e^{-\frac{h\nu}{kT}}}\\
\end{align}
$$

以及

$$
\begin{align}
S &= (1-\epsilon)\bar{J} + \epsilon B \\
\epsilon &= \frac{\varepsilon}{1+\varepsilon}\\
\end{align}
$$

这个形式就和上一节散射的源函数一致了。最后有（未确认）：

$$ \bar{J} = \int_0^\infty \int_0^\infty \phi^2 E_1(\phi |t-\tau|) d\nu S(t) dt $$

## 二能级原子的解

具体的解方法在TSA书中，这里抛开所有的推到过程定性地看看在某些特定的$$ B $$下源函数和光强是什么样子的。

为了简化我们定义：

$$ x = \frac{\nu - \nu_0}{\Delta \nu_D} $$
