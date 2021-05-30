import cv2

image = cv2.imread('face.jpg')

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for xmin, ymin, width, height in detector.detectMultiScale(image):
    cv2.rectangle(
        image,
        (xmin, ymin),
        (xmin + width, ymin + height),
        (0, 0, 255),
        3
    )

cv2.imshow('preview', image)
cv2.waitKey()
