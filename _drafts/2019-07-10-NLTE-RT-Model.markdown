---
layout:     post
title:      "NLTE下的辐射转移和大气模型"
subtitle:   "Avrett 2008 Lecture Note"
date:       2019-07-10
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

$$ I_\nu = I_\nu(r, \nu) $$

平均辐射强度：

$$ J_\nu = \frac{1}{4\pi} \int I_\nu d\Omega = \frac{1}{2} \int_{-1}^1 I_\nu d\mu $$

单色能量密度：

$$ U_\nu = \frac{4\pi}{c} J_\nu $$

单色天文流量：

$$ \pi F_\nu = \int I_\nu \cos{\theta} d\Omega = 2\pi \int_{-1}^1 \mu I_\nu d\mu $$

斯特芬-玻尔兹曼定律：

$$ \pi F = \pi \int_{0}^\infty F_\nu d\nu = \sigma T_\mathrm{eff} $$

辐射转移方程(1)：

$$ \frac{dI_\nu}{dl} = -\kappa_\nu I_\nu + \eta_\nu $$

源函数、光深：

$$ S_\nu = \frac{\eta_\nu}{\kappa_\nu}, d\tau_\nu = -\kappa_\nu \mu dl $$

所以辐射转移方程(2)：

$$ \mu \frac{dI_\nu}{d\tau_\nu} = I_\nu - S_\nu $$
