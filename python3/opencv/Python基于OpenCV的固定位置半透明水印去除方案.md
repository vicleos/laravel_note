from: https://my.oschina.net/u/2400083/blog/732321

OpenCV基础
OpenCV（Open Source Computer Vision Library）是一个跨平台计算机视觉库，实现了图像处理和计算机视觉方面的很多通用算法

#### 基于 inpaint 方法
- 算法理论：基于Telea在2004年提出的基于快速行进的修复算法（FMM算法），先处理待修复区域边缘上的像素点，然后层层向内推进，直到修复完所有的像素点
- 处理方式：由ui人员制作出黑底白色水印且相同位置的水印蒙版图(必须单通道灰度图)，然后使用inpaint方法处理原始图像，具体使用时可把水印区放粗，这样处理效果会好点
```python
# -*- coding: utf-8 -*-
import cv2


# mask.png 与src.jpg尺寸相同并且黑色背景，白色区域是要处理水印的区域
# https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html#gsc.tab=0
src = cv2.imread('src.jpg')  # 默认的彩色图(IMREAD_COLOR)方式读入原始图像

#mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)  # 灰度图(IMREAD_GRAYSCALE)方式读入水印蒙版图像
mask = cv2.imread('mask.png', 0)

# 参数：目标修复图像; 蒙版图（定位修复区域）; 选取邻域半径; 修复算法(包括INPAINT_TELEA/INPAINT_NS， 前者算法效果较好)
dst = cv2.inpaint(src, mask, 3, cv2.INPAINT_TELEA)

#cv2.imwrite('result.jpg', dst)
cv.imshow('dst',dst)
cv.waitKey(0)
cv.destroyAllWindows()
```
