import cv2 # opencv-python
import pytesseract

img = cv2.imread("img1.png")

custom_config = r' --oem 1 --psm 8'
pytesseract.image_to_string(img, config=custom_config)
