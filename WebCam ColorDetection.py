import cv2
import numpy as np


def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


cv2.namedWindow("TrackerBars")
cv2.resizeWindow("TrackerBars", 640, 480)
cv2.createTrackbar("Hue MIN", "TrackerBars", 0, 179, empty)
cv2.createTrackbar("Hue MAX", "TrackerBars", 179, 179, empty)
cv2.createTrackbar("Saturation MIN", "TrackerBars", 0, 255, empty)
cv2.createTrackbar("Saturation MAX", "TrackerBars", 255, 255, empty)
cv2.createTrackbar("Value MIN", "TrackerBars", 172, 255, empty)
cv2.createTrackbar("Value MAX", "TrackerBars", 255, 255, empty)

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

while True:
    success, img = cap.read()
    #cv2.imshow("Virtual Paint", img)
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue MIN", "TrackerBars")
    h_max = cv2.getTrackbarPos("Hue MAX", "TrackerBars")
    s_min = cv2.getTrackbarPos("Saturation MIN", "TrackerBars")
    s_max = cv2.getTrackbarPos("Saturation MAX", "TrackerBars")
    v_min = cv2.getTrackbarPos("Value MIN", "TrackerBars")
    v_max = cv2.getTrackbarPos("Value MAX", "TrackerBars")

    print(h_min, h_max, s_max, s_min, v_max, v_min)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    print(h_min, h_max, s_max, s_min, v_max, v_min)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    imgStack = stackImages(0.3, ([img, imgHsv], [imgResult, mask]))
    cv2.imshow("Image Stack", imgStack)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()
