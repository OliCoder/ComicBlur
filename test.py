# -*- coding:utf-8 -*-

import numpy as np
import cv2
from tqdm import tqdm

def Sobel(srcImg):
	if srcImg is None:
		raise RuntimeError("This image does not exist")
	x = cv2.Sobel(srcImg, cv2.CV_16S, 1, 0)
	y = cv2.Sobel(srcImg, cv2.CV_16S, 0, 1)
	absX = cv2.convertScaleAbs(x)
	absY = cv2.convertScaleAbs(y)
	dstImg = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
	return dstImg

def test_sobel(filename):
	img = cv2.imread(filename)

	gray = img.copy()
	cv2.imshow("img", img)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	dst = Sobel(img)
	dst = 255 - dst
	cv2.imshow("dst", dst)
	ret, dst = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	cv2.imshow("bw", dst)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def skyRegion(srcImg):
	lower_bound = np.array([100, 43, 46], np.uint8)
	upper_bound = np.array([124, 255, 255], np.uint8)
	srcImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2HSV)

	H, S, V = cv2.split(srcImg)
	V = cv2.equalizeHist(V)
	imgHSV = cv2.merge((H, S, V))
	imgThreshold = cv2.inRange(imgHSV, lower_bound, upper_bound)
	imgThreshold = cv2.medianBlur(imgThreshold, 9)
	kernel = np.ones((5, 5), np.uint8)
	imgThreshold = cv2.morphologyEx(imgThreshold, cv2.MORPH_OPEN, kernel, iterations = 10)
	dstImg = cv2.medianBlur(imgThreshold, 9)
	cv2.imwrite('mask.jpg', dstImg)
	#####name
	return dstImg

def seamClone(srcImg, skyImg):
	width, height, channels = srcImg.shape
	mask_0 = cv2.imread('mask.jpg', 0)
	mask_1 = cv2.imread("mask.jpg")
	img, contours, hierarchy = cv2.findContours(mask_0, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]
	x, y, w, h = cv2.boundingRect(img)
	print(x, y, w, h)
	if w == 0 or h == 0:
		return srcImg
	skyImg = cv2.resize(skyImg, (height, width), interpolation = cv2.INTER_CUBIC)
	center = (int((x + w) / 2), int((y + h) / 2))
	dstImg = cv2.seamlessClone(skyImg, srcImg, mask_1, center, cv2.NORMAL_CLONE)

	return dstImg

"""def findPos(pix, map):

	rows, cols, channels = map.shape
	for i in tqdm(range(rows)):
		for j in range(cols):
			if pix.all() == map[i][j].all():
				return [i, j]"""

def myBlur(srcImg):
	ori_map = cv2.imread("original_table.png")
	new_map = cv2.imread("table2.jpg")
	#new_map = cv2.imread("trans_table.jpg")
	if new_map is None:
		raise RuntimeError("fuck")
	rows, cols, channels = srcImg.shape
	dstImg = srcImg.copy()
	for i in range(rows):
		for j in range(cols):
			#pos = findPos(srcImg[i][j], ori_map)
			x = int(srcImg[i][j][1] / 4) + int(srcImg[i][j][0] / 32) * 64
			y = int(srcImg[i][j][2] / 4) + int(srcImg[i][j][0] % 32 / 4) * 64
			if x >= 512:
				x = 511
			if y >= 512:
				y = 511
			dstImg[i][j] = new_map[int(x)][int(y)]
	return dstImg



if __name__ == "__main__":
	img = cv2.imread('pic6.jpg')
	sky = cv2.imread('cloud2.jpg')
	tmp = seamClone(img, sky)
	dst =myBlur(tmp)

	cv2.imshow("s", img)
	cv2.waitKey(0)
	"""np.set_printoptions(threshold=np.nan)
	img = cv2.imread('original_table.png')
	g,b,r = cv2.split(img)
	x = b/4+g/32*64
	y = r/4+g%32/4*64

	dst = cv2.merge((x,y))
	print(dst[-1])"""
