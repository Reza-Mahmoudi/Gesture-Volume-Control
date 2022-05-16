#Importing the libraries we will need
import math
import cv2
import time
import numpy as np
import  HandTrackingModule as HTM

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##############################

withCam ,HightCam=640,480
##############################
cap=cv2.VideoCapture(0)
cap.set(3,withCam)
cap.set(4,HightCam)
PastTime=0
detector = HTM.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
volrange = volume.GetVolumeRange()
minVol = volrange[0]
maxvol=volrange[1]
vol=0
volbar=400
volper=0
while True:
    success ,img = cap.read()
    img = detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist) !=0:
        print(lmlist[4] ,lmlist[12])
        x1,y1= lmlist[4][1],lmlist[4][2]
        x2,y2= lmlist[12][1],lmlist[12][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),7,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 7, (255, 0, 0),cv2.FILLED)
        #distanse betwan two finger shat and esharo
        lenth = math.hypot(x2-x1,y2-y1)
            #print(lenth)

        #hand range minim = 50 , max : 300
        #vol range -65.5 - 0
        vol = np.interp(lenth,[50,300],[minVol,maxvol])
        volbar=np.interp(lenth,[50,300],[400,150])
        volper = np.interp(lenth, [50, 300], [0, 100])
        print( int(lenth) ,vol)
        volume.SetMasterVolumeLevel(vol, None)
        if lenth<50:
            cv2.circle(img, (cx, cy), 3, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    #for vol
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),3)
    curentTime=time.time()
    Fps=1/(curentTime-PastTime)
    PastTime =curentTime
    cv2.putText(img,f'Fps:{int(Fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Image" ,img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break