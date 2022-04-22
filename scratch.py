import cv2
import numpy as np
import math
img = np.zeros((480,640), np.uint8)

# Distance between two lines
def getDistance(Mx1,My1,Mx2,My2,Nx1,Ny1,Nx2,Ny2):
    #Ax+By+c=0
    AM = My1-My2
    BM = Mx2-Mx1
    CM = Mx1*My2-Mx2*My1
    #Nx+My+d=0
    AN = My1-My2
    BN = Nx2-Nx1
    CN = Nx1*My2-Nx2*My1
    dist = abs(CN-CM)/math.sqrt(AM*AM+BM*BM)
    return dist




# Line perpendicular to the line
def getPerpCoord(aX, aY, bX, bY, length):
    vX = bX-aX
    vY = bY-aY
    #print(str(vX)+" "+str(vY))
    # if(vX == 0 or vY == 0):
    #     return 0, 0, 0, 0
    mag = math.sqrt(vX*vX + vY*vY)
    vX = vX / mag
    vY = vY / mag
    temp = vX
    vX = 0-vY
    vY = temp
    cX = bX + vX * length
    cY = bY + vY * length
    dX = bX - vX * length
    dY = bY - vY * length
    return int(cX), int(cY), int(dX), int(dY)
    
x1,y1,x2,y2 = getPerpCoord(100,1,100,478,100)
print(x1,y1,x2,y2)

l1 = [(100,1), (100,478)]
l2 = [(120,1), (120,478)]

cv2.line(img, (x1,y1), (x2,y2), (255,100,255), 5)
cv2.line(img, l1[0], l1[1], (255,255,255), 1)
cv2.line(img, l2[0], l2[1], (255,0,255), 1)

print("Distance",   getDistance(100,1,100,478,120,1,120,478))

cv2.imshow('image', img)
cv2.waitKey(0)