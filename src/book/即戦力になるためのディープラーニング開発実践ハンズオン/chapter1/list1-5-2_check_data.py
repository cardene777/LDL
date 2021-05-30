import cv2

image = cv2.imread('face.jpg')
print(len(image))
print(len(image[0]))
print(len(image[0][0]))
print(image.shape)
