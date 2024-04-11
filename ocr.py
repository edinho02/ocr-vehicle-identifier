import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

readImg = cv2.imread('./1.png')
# readImg = cv2.imread('./placa.jpg')
img = cv2.cvtColor(readImg, cv2.COLOR_RGB2GRAY)

cv2.imwrite('./out/t.jpg', img)

_, finalImg = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY) # melhor 1°
finalAdT = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 32) # melhor 2°
finalAdTG = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 2) # melhor 3°

cv2.imwrite('./out/trashold.jpg', finalImg)
cv2.imwrite('./out/trasholdAdT.jpg', finalAdT)
cv2.imwrite('./out/trasholdAdTG.jpg', finalAdTG)

text0 = pytesseract.image_to_string(img, lang='por')
text = pytesseract.image_to_string(finalImg, lang='por')
text2 = pytesseract.image_to_string(finalAdT, lang='por')
text3 = pytesseract.image_to_string(finalAdTG, lang='por')

print('0 - ', text0)
print('1 - ', text)
print('2 - ', text2)
print('3 - ', text3)