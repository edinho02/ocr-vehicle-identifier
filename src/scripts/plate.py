import cv2
import pytesseract
import re

def _readText(img, lang='por'):
    return "".join(filter(str.isalnum, pytesseract.image_to_string(img, lang=lang, config=r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6 --oem 3')))

def _findPlate(text):
    plates = re.findall(r'[A-Z]{3}\d{4}', text)
    
    if (len(plates) != 0):
        return plates[0]
    
    plates = re.findall(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}', text)
    
    if (len(plates) != 0):
        return plates[0]
    
    return None

def _limiarizeImage(img):
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImgFiltered = cv2.bilateralFilter(grayImg, 9, 75, 75)
    return cv2.adaptiveThreshold(grayImgFiltered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

def _trimPlates(img, imgFiltered):
    contours, _ = cv2.findContours(imgFiltered, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    plates = []

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        numberOfSides = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        area = cv2.contourArea(contour)
        x, y, width, height = cv2.boundingRect(contour)

        if height > width:
            continue

        if height < (width * 0.2):
            continue

        if area < 10000 or area > 70000:
            continue

        if len(numberOfSides) < 4 or len(numberOfSides) > 10:
            continue

        cv2.drawContours(img, [numberOfSides], -1, (0, 255, 0), 2)

        x, y, width, height = cv2.boundingRect(contour)
        
        trimPlate = cv2.cvtColor(img[y:y + height, x:x + width], cv2.COLOR_BGR2GRAY)
        _, trimPlate = cv2.threshold(trimPlate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        trimPlate = cv2.morphologyEx(trimPlate, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
        trimPlate = cv2.morphologyEx(trimPlate, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        trimPlate = cv2.dilate(trimPlate, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        trimPlate = cv2.erode(trimPlate, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        plates.append(trimPlate)

    return plates

def _readImagesText(plates):
    for plate in plates:
        x, y, w, h = cv2.boundingRect(plate)

        if(h > 120):
            plate = plate[30:]
            plate = plate[:-10]

        text = _findPlate(_readText(plate, 'por'))

        if (text):
            return text
        
        text = _findPlate(_readText(plate, 'eng'))
        
        if (text):
            return text

        return 'Placa não encontrada'


def readPlate(platePath):
    img = cv2.imread(platePath)
    limiarizedImg = _limiarizeImage(img)

    plates = _trimPlates(img, limiarizedImg)
    plates.append(limiarizedImg)

    return _readImagesText(plates)

def getOriginalPlateName(fileName):
    return fileName.split('.')[0]

def calcPrecision(baseTextStr, textStr):
    baseText = [*baseTextStr]
    text = [*textStr]

    baseTextCharsNum = len(baseText)
    correctCharsNum = 0

    if len(baseText) == 0:
        return '100.00%'

    for letter in baseText:
        index = baseText.index(letter)

        if (index > len(text) - 1):
            continue

        if letter.lower() == text[index].lower():
            correctCharsNum = correctCharsNum + 1

    return '{:.2f}%'.format((correctCharsNum / baseTextCharsNum) * 100)

def calcAveragePrecision(precisions):
    if (len(precisions) == 0):
        return '100.00%'
    
    sum = 0

    for precision in precisions:
        sum = sum + float(precision.replace('%', ''))

    return '{:.2f}%'.format(sum / len(precisions))
