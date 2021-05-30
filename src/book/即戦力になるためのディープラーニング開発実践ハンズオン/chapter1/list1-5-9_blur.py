import cv2

image = cv2.imread('face.jpg')

image = cv2.blur(image, (5, 5))

cv2.imshow('preview', image)
cv2.waitKey()
