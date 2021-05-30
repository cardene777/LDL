import cv2

image = cv2.imread('face.jpg')

print("Before")
print(image.shape)
print(image.dtype)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("After")
print(image.shape)
print(image.dtype)

cv2.imshow('preview', image)
cv2.waitKey()
