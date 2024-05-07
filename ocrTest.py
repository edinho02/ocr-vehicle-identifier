import pytesseract
import numpy as np
import imutils
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

readImg = cv2.imread('./placa.jpg')
finalImg = cv2.cvtColor(readImg, cv2.COLOR_RGB2GRAY)

# finalImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 2) # melhor 3°
cv2.imwrite('./outA.jpg', finalImg)

bfilter = cv2.bilateralFilter(finalImg, 11, 17, 17) # filtro de ruido

cv2.imwrite('./outB.jpg', bfilter)

edged = cv2.Canny(bfilter, 30, 200) #detecção de borda

cv2.imwrite('./out.jpg', edged)

#contornos
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
index = 0
for contour in contours:
    area = cv2.contourArea(contour)
    approx = cv2.approxPolyDP(contour, 10, True)
    print('area', area)
    # print('approx', approx)

    if (0 <= area <= 100000):
        location = approx
        mask = np.zeros(finalImg.shape, np.uint8)
        new_image = cv2.drawContours(mask, [approx], 0,255, 20)
        new_image = cv2.bitwise_and(finalImg, finalImg, mask=mask)

        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = finalImg[x1:x2+1, y1:y2+1]

        cv2.imwrite('./crops/' + str(index) +'.jpg', cropped_image)
        
        text = pytesseract.image_to_string(cropped_image, lang='por')
        print('text: ' + text)
        index = index + 1

    # if len(approx) == 4:
    #     location = approx

    #     mask = np.zeros(finalImg.shape, np.uint8)
    #     new_image = cv2.drawContours(mask, [approx], 0, 255, 20)
    #     new_image = cv2.bitwise_and(finalImg, finalImg, mask=mask)

    #     (x,y) = np.where(mask==255)
    #     (x1, y1) = (np.min(x), np.min(y))
    #     (x2, y2) = (np.max(x), np.max(y))
    #     cropped_image = finalImg[x1:x2+1, y1:y2+1]

    #     cv2.imwrite('./crops/' + str(index) +'.jpg', cropped_image)

    #     if (index == 2):
    #         break
        
    #     index = index + 1

# mask = np.zeros(finalImg.shape, np.uint8)
# new_image = cv2.drawContours(mask, [location], 0,255, 20)
# new_image = cv2.bitwise_and(finalImg, finalImg, mask=mask)

# (x,y) = np.where(mask==255)
# (x1, y1) = (np.min(x), np.min(y))
# (x2, y2) = (np.max(x), np.max(y))
# cropped_image = finalImg[x1:x2+1, y1:y2+1]

# cv2.imwrite('./outF.jpg', cropped_image)
