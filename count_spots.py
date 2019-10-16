import cv2
import numpy as np
#import matplotlib.pyplot as plt
import math
import pandas as pd

def notInList(newObject, detectedObjectList, thresholdDist):
    for detectedObject in detectedObjectList:
        if math.hypot(newObject[0]-detectedObject[0],newObject[1]-detectedObject[1]) < thresholdDist:
            return False
    return True

def templateMatch (imagePath, templateImagePath):
    img_rgb = cv2.imread(imagePath)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templateImagePath,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = -10000000
    loc = np.where( res >= threshold)

    detectedObjects=[]
    thresholdDist=30

    for pt in zip(*loc[::-1]):
        if len(detectedObjects) == 0 or notInList(pt, detectedObjects, thresholdDist):
            detectedObjects.append(pt)
            cellImage=img_rgb[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
            cv2.imwrite("results/"+str(pt[1])+"_"+str(pt[0])+".jpg",cellImage,
            [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    return len(detectedObjects)


df = pd.read_csv("lot_data_with_capacity.csv")
lotNames = list(df["Parking Lots"])
print(lotNames)

for i in range (0, len(lotNames)):
    spaces = templateMatch("lot_images/" + lotNames[i] + ".png", "lot_images/template.png")
    df.at[i, "Total Max Spots"] = spaces
    #print(lotNames[i], spaces)

print(df)
df.to_csv("lot_data_with_capacity.csv")