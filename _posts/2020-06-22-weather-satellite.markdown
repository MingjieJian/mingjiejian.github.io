---
layout:     post
title:      "在气象卫星图里看日食"
subtitle:   ""
date:       2020-06-22
author:     "mingjie"
header-img: "img/post-bg-weather-satellite.png"
tags:
    - experience

---

中国区约15分钟间隔的风云四号真彩色图可以在[这里](http://data.cma.cn/dataGis/static/grid4/#/pcindex)爬到；图片被纵向分成了编号为5/6/7，横向分成了编号为10-14的小块，爬下来拼合就行。wget的时候要带上浏览器伪装。

全圆盘风云4/2号云图可以在[这里](http://rsapp.nsmc.org.cn/geofy/?i=15&isPlay=true&speed=2&sat=fy-4a&pro=geos&type=full_disk&band=1&overlay=&x=0&y=0&z=0&area=1&ll=0&county=0&duration=36&interval=1&c=false&cp=0.5&st=&et=&ac=110000&hide=1&s=1)下载，网站本身就有动图下载。

[这里](https://www.goes.noaa.gov/)汇总了美国GOES、欧盟Meteosat系列卫星和日本向日葵8号的图像；里面提供低分辨率的缩略动图。高分辨率的图要到各家自己的网站（图片下方链接）去下。

[向日葵8号](https://www.data.jma.go.jp/mscweb/data/himawari/index.html)的图片库。提供全圆盘和某些局部的图片下载。基本没有反爬虫措施，但是下载速度略慢。

印度的INSAT-3D图像可以[在这](https://mausam.imd.gov.in/imd_latest/contents/satellite.php#.)下载，不过我只找到了最近的。

欧盟Meteosat[在这](https://eumetview.eumetsat.int/mapviewer/?product=EO:EUM:DAT:MSG:NCL_ENH)可以下，爬虫就行。超级高清。

参考
https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481