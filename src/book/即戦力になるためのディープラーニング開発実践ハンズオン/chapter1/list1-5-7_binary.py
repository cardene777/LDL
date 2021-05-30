import cv2

image = cv2.imread('face.jpg')

print("Before")
print(image.shape)
print(image.dtype)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

threshold = 128
_, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

print("After")
print(image.shape)
print(image.dtype)

cv2.imshow('preview', image)
cv2.waitKey()
