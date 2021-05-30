import cv2

image = cv2.imread('face.jpg')

image = image[:, ::-1, :]

cv2.imshow('preview', image)
cv2.waitKey()
