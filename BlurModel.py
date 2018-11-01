# -*- coding:utf-8 -*-

import numpy as np
import cv2

class myBlur():
    def __init__(self, filename, style):
        self.img = cv2.imread(filename)
        self.style = style
        self.srcImg = self.img.copy() #tmpImg

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
        return self.ComicBlur()

    def SimpleStrokeModel(self):
        pass

    def PortraitModel(self):
        pass

    def applyModel(self):
        if self.style == "COMIC_STYLE":
            self.ComicModel()
        elif self.style == "SIMPLE_STROKE_STYLE":
            self.SimpleStrokeModel()
        elif self.style == "PORTRAIT_STYLE":
            self.PortraitModel()