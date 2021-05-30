import cv2

image = cv2.imread('face.jpg')

height, width = image.shape[:2]
center = (width / 2, height / 2)
angle = 30
scale = 1
mat = cv2.getRotationMatrix2D(center, angle, scale)
image = cv2.warpAffine(image, mat, (width, height))

cv2.imshow('preview', image)
cv2.waitKey()
