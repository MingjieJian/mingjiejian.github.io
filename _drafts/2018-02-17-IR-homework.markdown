---
layout:     post
title:      "Homework of  Intro to IR astronomy"
subtitle:   "35-166358"
date:       2018-02-17
author:     "mingjie"
header-img: "img/post-bg-IR-homework.jpg"
tags:
    - learning

---

#### Category:
- [Question 1](#Q1)
  - [Answer 1](#A1)
- [Question 2](#Q2)
  - [Answer 2](#A2)
- [Question 3](#Q3)
  - [Answer 3](#A3)

<p id = "Q1"></p>
#### Question 1
Derive the conversion formula: $$ F_\lambda = \frac{3\times 10^{14} F_\nu}{\lambda^2_{\mathrm{\mu m}}} $$where $$ [F_\lambda] = \mathrm{Wm^{-2}\mu m^{-1}} $$, $$ [F_\nu] = \mathrm{Wm^{-2}Hz^{-1}} $$, $$ [\nu] = \mathrm{Hz} $$, $$ [\lambda_{\mathrm{\mu m}}] = \mathrm{\mu m} $$.

<p id = "A1"></p>
##### Answer 1:

The definition of $$ F_\lambda $$ and $$ F_\nu $$ are:

$$ F_\lambda = \frac{\mathrm{d}F}{\mathrm{d}\lambda}, F_\nu = \frac{\mathrm{d}F}{\mathrm{d}\nu} $$

so we can get:

$$ F_\lambda = \frac{\mathrm{d}F}{\mathrm{d}\lambda} = F_\lambda = \frac{\mathrm{d}F}{\mathrm{d}\nu} \frac{\mathrm{d}\nu}{\mathrm{d}\lambda} = F_\nu \frac{\mathrm{d}\nu}{\mathrm{d}\lambda} $$

From $$ \lambda \nu = c $$ we can derive:

$$ \frac{\mathrm{d}\nu}{\mathrm{d}\lambda} = |\mathrm{d}(\frac{c}{\lambda})| = \frac{c}{\lambda^2} $$

The absolute value sign is for preventing the negative wavelength or frequency. So we have

$$ F_\lambda = \frac{c}{\lambda^2} F_\nu $$

Take $$ [\lambda_{\mathrm{\mu m}}] = \mathrm{\mu m} $$ and $$ c = 3\times10^14 \mathrm{\mu m/s} $$, we finally Have

$$ F_\lambda = \frac{3\times 10^{14} F_\nu}{\lambda^2_{\mathrm{\mu m}}} $$

<p id = "Q2"></p>
#### Question 2
Asume you want to observe a G2 star ($$ T_\mathrm{eff} = 5800\,\mathrm{K} $$) behind a dark cloud with extinction $$ A_\nu = 7$$ mag. Which would you choose: A 10-m telescope observing as V ($$ 0.55\,\mathrm{\mu m} $$) or a 1-m telescope observing at K ($$ 2.2 \,\mathrm{\mu m} $$)? Justify your answer.

<p id = "A2"></p>
##### Answer 2:

Here we calculate the magnitude difference of the star observed in V and K. By definition, the flux emitted by a star of a band is:

$$ I_V = \int B_\lambda F_V(\lambda) d\lambda $$

$$ I_K = \int B_\lambda F_K(\lambda) d\lambda $$

and the flux observed by the telescopes (without extinction) are:

$$ E_V = \frac{\pi r_V^2}{4\pi d^2}I_V, E_K = \frac{\pi r_K^2}{4\pi d^2}I_K $$

where $$ r_V, r_K $$ are the radius of the telescopes, and $$ d $$ is the distance of the star. So the magnitude difference considering extinction can be express as:

$$ m_V - m_K = -2.5 \log{\frac{E_V}{E_K}} + A_V - A_K = -2.5 \log{\frac{r_V^2 I_V}{r_K^2 I_K}} + A_V - A_K \tag{1}$$

We have known that $$ \frac{r_V^2}{r_K^2} = 100 $$, $$ A_V = 7 $$ and $$ A_K = 7 \times 0.114 = 0.798 $$; now we consider $$ I_V $$ and $$ I_K $$.

V band profile is considered as a Gaussian function around the wavelength given, and the flux is simplified as the multiplication of flux at the central wavelength and the FWHM (from [Wikipedia](https://en.wikipedia.org/wiki/Photometric_system)); so we get:

$$ I_V = B_\lambda(0.55) \times 0.088 = 2.3\times 10^{13}\, \mathrm{erg\, s^{-1}\, cm^{-3}} $$

For K band, though the profile is flatter, a similar approximation is made with FWHM as $$ 0.39 \mathrm{\mu m} $$:

$$ I_K = B_\lambda(2.2) \times 0.39 = 4.3\times 10^{12}\, \mathrm{erg\, s^{-1}\, cm^{-3}} $$

Substitute these values into $$ (1) $$, we have

$$ m_V - m_K \approx -2.5 \log{530} +7 - 0.798 = -0.61 \, \mathrm{mag} $$

As the V magnitude is smaller than K magnitude, I will choose to observe in V band.

<p id = "Q3"></p>
#### Question 3
Compute the limiting flux density in Jy for the Thirty-Meter Telescope and the James Webb Space Telescope for a resolving power ($$ \lambda/\Delta\lambda $$) of $$ 5.0 $$, $$ 2.5\times 10^3 $$ and $$ 1\times 10^5 $$ at a wavelengthof $$ 2.2 \,\mathrm{\mu m} $$ and $$ 11.5\,\mathrm{\mu m} $$. Assume a $$ 0.45 \times 0.45" $$ field of view and a pixel size of $$ 0.15" $$ for both telescopes. For the calculation assume the following (a-j).

<p id = "A3"></p>
##### Answer 3:

The SNR formula in 6-3 can be used to calculate the limiting flux density:

$$ \mathrm{SNR} = \frac{N_T}{\sqrt{N_T+n_p(N_{rn}^2+N_b+N_d)}} \tag{2}$$

where

$$ \begin{align}
n_p &= 9 \\
N_T &= 3St \times A \times 0.2 \\
\mathrm{SNR} &= 5 \\
N_{rn} &=
  \begin{cases}
    7 ~ \mathrm{electron} & 2.2 \, \mathrm{\mu m} \\
    14 ~ \mathrm{electron} & 11.5\, \mathrm{\mu m} \\
  \end{cases}  \\
N_{d} &=
  \begin{cases}
    0.05t ~ \mathrm{electron} & 2.2 \, \mathrm{\mu m} \\
    0.2t ~ \mathrm{electron} & 11.5\, \mathrm{\mu m} \\
  \end{cases}  \\
b &=
  \begin{cases}
    14.75 ~ \mathrm{mag/arcsec^2} & 2.2 \, \mathrm{\mu m}, \text{TMT} \\
    10^8 ~ \mathrm{photons\,s^{-1}\,m^{-2}\mu m^{-1}arcsec^{-2}} & 11.5\, \mathrm{\mu m}, \text{TMT} \\
    3 \times 10^{-6} ~ \mathrm{Jy/arcsec^2} & 2.2 \, \mathrm{\mu m}, \text{JWST} \\
    3 \times 10^{-2} ~ \mathrm{Jy/arcsec^2} & 11.5 \, \mathrm{\mu m}, \text{JWST} \\
  \end{cases}  \\
\end{align} $$

Convert it into the unit of $$ \mathrm{electron \, s^{-1}m^{-2}\mu m^{-1}arcsec^{-2}} $$, using following relations:

$$ \begin{align}
F &= 645 \times 10^{-2/5(m-0.03)} \mathrm{Jy} \\
1 \, \mathrm{Jy} &= 10^{-19} \mathrm{\frac{erg}{s\,m^2\,Hz}} \\
F_\lambda &= 3 \times \frac{10^{14}}{\lambda_\mathrm{\mu m}^2} F_\nu \\
n_\mathrm{electron} &= 0.2 n_\mathrm{photon} = \frac{0.2\lambda}{hc}F \\
\end{align}$$

We can get

$$
b =
  \begin{cases}
    1.2 \times 10^{3} ~ \mathrm{electrons\,s^{-1}\,m^{-2}\mu m^{-1}arcsec^{-2}} & 2.2 \, \mathrm{\mu m}, \text{TMT} \\
    2.0 \times 10^{7} ~ \mathrm{electrons\,s^{-1}\,m^{-2}\mu m^{-1}arcsec^{-2}} & 11.5\, \mathrm{\mu m}, \text{TMT} \\
    2.5 ~ \mathrm{electrons\,s^{-1}\,m^{-2}\mu m^{-1}arcsec^{-2}} & 2.2 \, \mathrm{\mu m}, \text{JWST} \\
    2.5 \times 10^{4} ~ \mathrm{electrons\,s^{-1}\,m^{-2}\mu m^{-1}arcsec^{-2}} & 11.5 \, \mathrm{\mu m}, \text{JWST} \\
  \end{cases}
$$

Then the b value in electron can be express as:

$$ b \mathrm{(electron)} = b \times t \times A \times 9 \frac{\lambda}{\mathrm{R}} \times 0.45^2 $$

Then the b value (in electron) in each resolve power are:

$$ \mathrm{res} = 5 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 4.0 \times 10^{8} $$ | $$ 5.0 \times 10^{4} $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 3.5 \times 10^{13} $$ | $$ 5.0 \times 10^{8} $$ |

$$ \mathrm{res} = 2.5 \times 10^3 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 8.1 \times 10^{5} $$ | $$ 99 $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 7.4 \times 10^{10} $$ | $$ 9.9 \times 10^{5} $$ |

$$ \mathrm{res} = 10^5 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 2.0 \times 10^{4} $$ | $$ 2.5 $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 1.8 \times 10^{9} $$ | $$ 2.5 \times 10^{4} $$ |

Substitute them into formula (2) then convert the unit into Jy, we can get the limit flux density:

$$ \mathrm{res} = 5 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 1.2 \times 10^{-7} $$ | $$ 3.7 \times 10^{-8} $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 3.5 \times 10^{-5} $$ | $$ 3.7 \times 10^{-6} $$ |

$$ \mathrm{res} = 2.5 \times 10^3 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 2.7 \times 10^{-6} $$ | $$ 1.4  \times 10^{-6} $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 7.9 \times 10^{-4} $$ | $$ 8.3 \times 10^{-5} $$ |

$$ \mathrm{res} = 10^5 $$,

|       |  TMT  | JWST  |
|:-----:|:-----:|:-----:|
| $$ 2.2 \, \mathrm{\mu m} $$ | $$ 1.7 \times 10^{-5} $$ | $$ 4.2 \times 10^{-5} $$ |
| $$ 11.5 \, \mathrm{\mu m} $$   | $$ 5.0 \times 10^{-3} $$ | $$ 5.3 \times 10^{-4} $$ |
