import os
import cv2
from src.scripts.plate import readPlate, calcPrecision, calcAveragePrecision, getOriginalPlateName
from src.scripts.printer import printAndReadPlateNum, printPlateResult, printPlateAveragePrecision
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

platesFolder = "src/images"
plates = os.listdir(platesFolder)

option = printAndReadPlateNum(len(plates))

def readPlateData(plateFileName):
    originalPlateName = getOriginalPlateName(plateFileName)
    resultPlateName = readPlate(os.path.join(platesFolder, plateFileName))
    precision = calcPrecision(originalPlateName, resultPlateName)

    return originalPlateName, resultPlateName, precision

if (int(option) >= 1 and int(option) <= len(plates)):
    plateFileName = plates[int(option) - 1]
    originalPlateName, resultPlateName, precision = readPlateData(plateFileName)

    printPlateResult(originalPlateName, resultPlateName, precision)
else:
    precisions = []

    for plateFileName in plates:
        originalPlateName, resultPlateName, precision = readPlateData(plateFileName)

        precisions.append(precision)
        printPlateResult(originalPlateName, resultPlateName, precision)

    averagePrecision = calcAveragePrecision(precisions)
    printPlateAveragePrecision(averagePrecision)
