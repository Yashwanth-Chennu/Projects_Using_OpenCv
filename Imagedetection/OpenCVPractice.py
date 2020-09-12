#Wrap Images

import cv2
import numpy as np

img = cv2.imread("Images/Cards.png")

print(img.shape)
width = int(img.shape[1]/2)
height = int(img.shape[0]/2)


plt = np.float32([[291, 23], [368, 23], [291, 128], [368, 128]])
plt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(plt, plt2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))


cv2.imshow("Cards", img)
cv2.imshow("Wrap", imgOutput)
cv2.waitKey(0)
