# -*- coding:utf-8 -*-

import numpy as np
import cv2

class myBlur(object):
    def __init__(self, filename, style):
        self.img = cv2.imread(filename)
        self.style = style
        if style == "SIMPLE_STROKE_STYLE" or style == 1:
            self.srcImg = cv2.imread(filename, 0)
        else:
            self.srcImg = self.img.copy() #tmpImg

########################################################################################################################
#                                                       COMIC_FITTER                                                   #
########################################################################################################################
    def skyRegion(self):
        lower_bound = np.array([100, 43, 46], np.uint8)
        upper_bound = np.array([124, 255, 255], np.uint8)
        srcImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        H, S, V = cv2.split(srcImg)
        V = cv2.equalizeHist(V)
        imgHSV = cv2.merge((H, S, V))
        imgThreshold = cv2.inRange(imgHSV, lower_bound, upper_bound)
        imgThreshold = cv2.medianBlur(imgThreshold, 9)
        kernel = np.ones((5, 5), np.uint8)

        imgThreshold = cv2.morphologyEx(imgThreshold, cv2.MORPH_OPEN, kernel, iterations=10)
        dstImg = cv2.medianBlur(imgThreshold, 9)
        cv2.imwrite('mask.jpg', dstImg)
        #####name
        return dstImg

    def seamClone(self, skyImg):
        width, height, channels = self.img.shape
        mask_0 = cv2.imread('mask.jpg', 0)
        mask_1 = cv2.imread("mask.jpg")
        img, contours, hierarchy = cv2.findContours(mask_0, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(img)
        #print(x, y, w, h)
        if w == 0 or h == 0:
            raise RuntimeError("cannot get suitable boundRect")
        skyImg = cv2.resize(skyImg, (height, width), interpolation=cv2.INTER_CUBIC)
        center = (int((x + w) / 2), int((y + h) / 2))
        dstImg = cv2.seamlessClone(skyImg, self.img, mask_1, center, cv2.NORMAL_CLONE)
        self.srcImg = dstImg

        return dstImg

    def ComicBlur(self):
        #ori_map = cv2.imread("original_table.png")
        new_map = cv2.imread("table2.jpg")
        # new_map = cv2.imread("trans_table.jpg")
        if new_map is None:
            raise RuntimeError("fuck")
        rows, cols, channels = self.srcImg.shape
        dstImg = self.srcImg.copy()
        for i in range(rows):
            for j in range(cols):
                # pos = findPos(srcImg[i][j], ori_map)
                x = int(self.srcImg[i][j][1] / 4) + int(self.srcImg[i][j][0] / 32) * 64
                y = int(self.srcImg[i][j][2] / 4) + int(self.srcImg[i][j][0] % 32 / 4) * 64
                if x >= 512:
                    x = 511
                if y >= 512:
                    y = 511
                dstImg[i][j] = new_map[int(x)][int(y)]
        return dstImg

    def ComicModel(self):
        skyImg = cv2.imread("cloud2.jpg")
        self.skyRegion()
        self.seamClone(skyImg)
        cv2.imwrite('dstImg.jpg',self.ComicBlur())
        return self.ComicBlur()

########################################################################################################################
#                                                 SIMPLE_STROKE__FITTER                                                #
########################################################################################################################

    def dodgeNaive(self, mix_img):
        return cv2.divide(self.srcImg, 255 - mix_img, scale=256)

    def GRAY2RGB(self, BaseImg):
        sx, sy = BaseImg.shape
        tx, ty, tz = self.img.shape

        # 复制灰度图的图层
        BaseImg2 = np.zeros((sx, sy, 3), np.uint8)
        BaseImg2[:, :, 0] = BaseImg
        BaseImg2[:, :, 1] = BaseImg
        BaseImg2[:, :, 2] = BaseImg

        # 转换颜色空间ycbcr color space
        nspace1 = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCrCb)
        nspace2 = cv2.cvtColor(BaseImg2, cv2.COLOR_BGR2YCrCb)

        ms = np.double(nspace1[:, :, 0])
        mt = np.double(nspace2[:, :, 0])
        m1 = ms.max()
        m2 = ms.min()
        m3 = mt.max()
        m4 = mt.min()
        d1 = m1 - m2
        d2 = m3 - m4

        # 归一化
        dx1 = ms
        dx2 = mt
        dx1 = cv2.divide(dx1 * 255, 255 - d1, scale=1)
        dx2 = cv2.divide(dx2 * 255, 255 - d2, scale=1)
        mx, my = dx2.shape

        # Luminance Comparison
        nimage = np.zeros((sx, sy, 3), np.uint8)
        for i in range(mx):
            for j in range(my):
                iy = dx2[i, j]
                tmp = abs(dx1 - iy)
                index = np.where(tmp == np.min(tmp))
                nimage[i, j, 1] = nspace1[index[0][0], index[1][0], 1]
                nimage[i, j, 2] = nspace1[index[0][0], index[1][0], 2]
                nimage[i, j, 0] = nspace2[i, j, 0]
        dstImg = cv2.cvtColor(nimage, cv2.COLOR_YCrCb2BGR)
        return dstImg

    def SimpleStrokeModel(self):
        RevImg = 255 - self.srcImg
        RevImg = cv2.GaussianBlur(RevImg, (15, 15), 0)
        dstImg = self.dodgeNaive(RevImg)
        return self.GRAY2RGB(dstImg)

########################################################################################################################
#                                                    PORTRAIT__FITTER                                                  #
########################################################################################################################
    def PortraitModel(self):
        pass



    def applyModel(self):
        if self.style == "COMIC_STYLE" or self.style == 0:
            self.ComicModel()
        elif self.style == "SIMPLE_STROKE_STYLE" or self.style == 1:
            self.SimpleStrokeModel()
        elif self.style == "PORTRAIT_STYLE" or self.style == 2:
            self.PortraitModel()