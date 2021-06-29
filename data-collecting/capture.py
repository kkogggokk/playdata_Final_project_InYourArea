#-*- coding: utf-8 -*-

import cv2
import time
 
starttime = time.time()

# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
vidcap = cv2.VideoCapture('input video path')
 
count = 0
 
while(vidcap.isOpened()):
    # read()는 grab()와 retrieve() 두 함수를 한 함수로 불러옴
    # 두 함수를 동시에 불러오는 이유는 프레임이 존재하지 않을 때 grab() 함수를 이용하여 return false 혹은 NULL 값을 넘겨 주기 때문
    ret, image = vidcap.read()

    # 지정된 프레임마다 이미지를 캡쳐하고 저장
    if(int(vidcap.get(1)) % 15 == 0):
        cv2.imwrite("save image path" % count, image)
        print('Saved frame%d.jpg' % count)
        starttime = time.time()
        count += 1
        
vidcap.release()
exit()
