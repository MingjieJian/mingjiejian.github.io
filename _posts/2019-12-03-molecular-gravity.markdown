---
layout:     post
title:      "分子线的gravity effect"
subtitle:   "好早就被人搞过啦"
date:       2019-12-03
author:     "mingjie"
header-img: "img/post-contri_func.png"
tags:
    - learning

---

* any words
{:toc}

## 缘起

现在不是在搞谱线的gravity effect嘛，发现一些被blend的谱线中有分子线的贡献，就得知道分子线会不会对gravity effect有贡献。从观测和合成光谱来看是有的，而且在4000-5000K上分子线和原子线有一样的gravity effect。但是为什么呢？

## 论文s

我是从查"molecular line gravity / molecular line spectral classification"之类的开始的。

[White & Wing 1978](https://ui.adsabs.harvard.edu/abs/1978ApJ...222..209W/abstract), section IV(c):

> Keenan (1963) has pointed out that the blue CN bands are a good luminosity indicator in late G and early K stars, but that they cannot be used alone because of abundance effects.

### CH

Keenan (1963), page 96:

> Since the association into molecules is favored by higher pressure, it is not surprising that the G band (mainly due to CH) has a negative luminosity effect and is too weak in supergiants to be useful as a temperature criterion.


### CN

Keenan (1963), page 96:

> About 1921, Lindblad recognized that the absorption (around 3883A) was due primarily to CN ans showed that the integrated absorption had a strong positive correlation with luminosity ([Lindblad 1922](https://ui.adsabs.harvard.edu/abs/1922ApJ....55...85L/abstract)). In the photometric classifications that grew out of this work, the intergrated CN absorption is the definitive criterion of luminosity (for summaries and references see Lindblad and Stenquist 1934, and [Lindblad 1946](https://ui.adsabs.harvard.edu/abs/1946ApJ...104..325L/abstract)).
> The $$\lambda$$ 4216 and $$\lambda$$ 3883 bands are scarcely noticeable in dwarfs of any type but are conspicuous in giants (G5-K3) and are even stronger in supergiants （Iwanowska 1936; Keenan 1941). They have accordingly been used generally to detect stars of high luminosity on even the shortest objective-prism spectra.
>

[Lançon et al. 2007](https://ui.adsabs.harvard.edu/abs/2007A%26A...468..205L/abstract)
> Strong CN bands are predicted for low gravity stars with temperatures around 4500 K, and are indeed observed in local red supergiants (Lançon & Wood 2000) and in extragalactic objects such as the bright star clusters of M 82 (Lançon et al. 2003).

### CO

[Ramirez et al. 1997](https://ui.adsabs.harvard.edu/abs/1997AJ....113.1411R/abstract):
> The CO absorption strength depends on both luminosity and effective temperature (Frogel 1971; Baldwin et al. 1973; McWilliam & Lambert 1984; Kleinmann & Hall 1986).

[Kleinmann & Hall 1986](https://ui.adsabs.harvard.edu/abs/1986ApJS...62..501K/abstract):
> The strengthening of CO absorption with decreasing temperature and increasing luminosity is well known;

[McWilliam & Lambert 1984](https://ui.adsabs.harvard.edu/abs/1984PASP...96..882M/abstract):
> The gravity and carbon abundance changes are expected because the cooler and more luminous giants are at a more advanced
stage of thermal pulsing and dredge-up of carbon. In general, microturbulence appears to increase with increasing luminosity.

[Baldwin et al. 1973](https://ui.adsabs.harvard.edu/abs/1973ApJ...184..427B/abstract):
> Several trends stand out in figure 3. The CO index increases with increasing luminosity. The giant and supergiant sequences are parallel, with a separation of about 0.04 in the index. The division between the dwarfs and giants for spectral types later than K0 is most pronounced.

> Calculations by V. G. Kunde (personal communication) have shown that changes of ~5 $$\mathrm{km\,s^{-1}}$$ in the microturbulent velocity can produce large changes in the strength of the CO absorption bands. These changes are considerably greater than any change produced by reasonable variations in any of the other parameters including CO abundance. An increase in microturbulence with decreasing temperature among the giants and supergiants, and a similar increase with increasing luminosity from dwarfs to supergiants, could then account for the observed variation of CO absorption. This effect would be strongest if the bands were saturated.

[Frogel 1971](https://ui.adsabs.harvard.edu/abs/1971PhDT........67F/abstract), page 91:
> The pressure operates vis-a-vis (face to face) collisional broadening in a manner which will increase line widths with increasing pressure. Since pressure decreases with increasing luminosity and both pressure and temperature decrease with advancing spectral type, these two parameters cannot account for the observed behavior of the CO bands.
