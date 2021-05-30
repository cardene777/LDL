import cv2

image = cv2.imread('face.jpg')
cv2.imshow('preview', image)
cv2.waitKey()
