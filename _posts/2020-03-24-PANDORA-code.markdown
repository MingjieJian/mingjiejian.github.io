---
layout:     post
title:      "PANDORA源码阅读备忘"
subtitle:   "Pandora and box"
date:       2020-03-24
author:     "mingjie"
header-img: "img/post-bg-achi.jpg"
tags:
    - learning

---

* any words
{:toc}

# `COMMON` block

`COMMON` block是Fortran中在不同函数之间传递变量的第二种方法（第一种是通过函数的输入参数）（但是我很讨厌这种方法）。它通过在不同函数中定义跟随在`COMMON`后的变量来传输。比如说在主程序中有

```
COMMON A, B, C

A = -2
B = 0.9
C = 66
```

然后在子程序中有

```
COMMON C, B, D
```

则子程序中`C`为-2、`B`为0.9、`D`为66。注意这和变量名无关，只和顺序有关。

[参考](https://www.obliquity.com/computer/fortran/common.html)
