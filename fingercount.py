import os

import cv2
import time
import HandTrackingModule as htm


hcam,wcam=600,600


cap=cv2.VideoCapture(0)
cap.set(3,hcam)
cap.set(4,wcam)

folderpath="fingers"
mylist=os.listdir(folderpath)
overlaylist=[]

for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)


print(mylist)
print(len(overlaylist))

ptime=0

detector=htm.handDetector(detectionCon=0.8)

tipids=[4,8,12,16,20]

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        fingers=[]
        #for RIGHT THUMB
        if (lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        #FOR 4 FINGERS
        for id in range(1,5):
            if(lmlist[tipids[id]][2]<lmlist[tipids[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)

        Totalfingers=fingers.count(1)
        print(Totalfingers)
        h,w,c=overlaylist[Totalfingers].shape
        img[0:h,0:w]=overlaylist[Totalfingers]

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS: {int(fps)}',(1000,70),cv2.FONT_HERSHEY_SIMPLEX,
                1,(255,0,0),3)

    cv2.imshow("video",img)
    cv2.waitKey(1)