---
layout:     post
title:      "如何在Linux上制作延时摄影视频"
subtitle:   "几个命令的事情"
date:       2018-01-21
author:     "mingjie"
header-img: "img/post-bg-time-lapse-linux.jpg"
tags:
    - experience

---

在Windows上制作延时摄影有很多软件，AE、LRTimelapse（去闪）之类的；但是Linux上相关的制作软件虽然有，但是并不是很熟悉。隐约感觉Linux肯定能做，而且可以在命令行上面做，但是需要问问谷歌。结果来说的确可以做出来，这里就把相关的软件以及命令记录一下。

### 原材料

2017年底拍摄的东大赤门的100张照片，间隔大概在1秒左右，jpg格式。

### 处理jpg文件

因为拍摄的时候曝光有点不足，所以需要对每张照片进行亮度和对比度的处理。这里用的是GIMP；如果没有安装过的话先安装GIMP：

`sudo apt-get install gimp`

然后安装批处理的插件：

`sudo apt-get install gimp-plugin-registry`

![](/img/in-post/post-time-lapse-linux/batch-open.png)

安装之后打开GIMP，上方菜单栏里面会多了一些栏目。选择`Filters - Batch - Batch Process`：

![](/img/in-post/post-time-lapse-linux/batch-window.png)

这个批处理窗口提供了一些我们需要的功能。选择`Add Files`将要处理的照片都添加进去。简单的亮度对比度颜色处理在`Colour`里面，选择`Enable`和`Auto Levels`就可以了。最后在`Rename`里面选择要输出的文件夹，需要的话先测试一下(`Test`)，觉得没有问题的话`Start`就行。处理过程中可能会报错，但是只要能成功输出就不用管了。

![](/img/in-post/post-time-lapse-linux/comp.png)
*处理前后的对比*

### 将jpg转换成视频

所以我们现在有了一堆处理过的jpg文件，之后只要把它们拼成视频就行了。这一步需要保证文件的顺序是正确的，也就是没有从999到001的情况。如果有的话需要将它们按照正确的顺序重命名。另一个需要注意的细节是可以通过命令调节输出视频的分辨率，不过我一般按照源片的分辨率来，也不用调整了。拼合的命令如下：

`ffmpeg -r 24 -pattern_type glob -i '*.jpg' -c:v copy output.avi`

`-r`后面的数字是帧数，可以随意调整，最后的`output.avi`是输出的文件名字。我还没试过其他的格式，而这个命令会原原本本地将照片拼到一个视频里面，所以这个视频是没有被压缩过的，占用的空间和照片们的空间一样。

这里的视频大小是2.2G，只是100张照片。当然这个大小不能轻易地放到网上去共享，所以我们进行压缩：

`ffmpeg -i MVI_7274.MOV -vcodec libx264 -preset fast -crf 20 -y -vf "scale=1920:-1" -acodec libmp3lame -ab 128k a.mp4`

参考链接里面有很详细的介绍，这里不赘述了。最重要的是`-crf`后面的参数，数字越小视频质量越高。可以多试几个不同的数字然后取合适的大小和质量。最后的视频如下：

<iframe width="100%" height="400" src="/img/in-post/post-time-lapse-linux/cloud_tl.mp4" frameborder="0" allowfullscreen></iframe>


### 闲话

刚刚想到其实也有别的思路，比如在GIMP编辑照片的时候将分辨率降低，那么占用的空间和后续处理时间都会变小。另外GIMP也有命令行模式，应该可以更细致地控制参数；不过稍微有点复杂，还需要研究一下。

### Reference

[jpg转成视频](https://ubuntuforums.org/showthread.php?t=2022316)

[视频压缩](https://segmentfault.com/a/1190000002502526)
