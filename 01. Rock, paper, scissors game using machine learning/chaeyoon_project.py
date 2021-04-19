#20151661 김채윤
#가위바위보게임

import random
import cv2
import numpy as np
from rpscv import utils
from rpscv import imgproc as imp
import pickle

filename = 'cyk.pkl'    # 학습 모델 학습 시킨 후 웨이트랑 바이스가 저장된 파일입니다
with open(filename, 'rb') as f:
    cyk = pickle.load(f)
cam = utils.cameraSetup()
stop = False

cv2.namedWindow('ChaeYoon.K_Python_Project', cv2.WINDOW_AUTOSIZE) # 카메라 출력 화면 GUI 설정

print("\nImage recognition mode")

lastGesture = -1  # 마지막 제스처 벨류

Pscore = 0 # 사람 스코어
Cscore = 0 # 컴퓨터 스코어

while not stop:
    img = cam.getOpenCVImage() # 카메라
    img = imp.crop(img)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    gray = imp.getGray(imgRGB, threshold=17)

    nonZero = np.count_nonzero(gray)
    waitTime = 1

    gesture = None
    notify = False

    if nonZero > 9000: # 인식
        predGesture = clf.predict([gray])[0]  # 학습 시킨 파일의 (W,b가 포함된 파일을 통해 인식함)

        if predGesture == lastGesture:
            successive += 1
        else:
            successive = 0

        if successive == 2:
            print('Player: {}'.format(utils.gestureTxt[predGesture]))
            waitTime=3000
            gesture = predGesture

            computerGesture = random.randint(0,2)  # 가위바위보 랜덤 (컴퓨터 차례)
            print('Computer: {}'.format(utils.gestureTxt[computerGesture]))

            K = computerGesture - predGesture

            if K in [-2, 1]:  #W,b 값을 비교(W,b는 학습 시킨 모델에 있음)
                print('Computer wins!')
                Cscore += 1

            elif K in [-1, 2]:
                print('Player wins!')
                Pscore += 1

            else:
                print('Tie')

            print('Score: player {}, computer {}\n'.format(Pscore, Cscore))   # 스코어 출력

        lastGesture = predGesture

    else:
        lastGesture = -1

    imgFR = imp.fastRotate(img)
    txtPos = (5, imgFR.shape[0] - 10)
    cam.addFrameRateText(imgFR, txtPos, bgr=(0,0,255))

    cv2.imshow('ChaeYoon.K_Python_Project', imgFR)

    key = cv2.waitKey(waitTime)
    if key in [27, 113]:
        stop = True
    elif key == 114:
        gesture = utils.ROCK
        notify = True
    elif key == 112:
        gesture = utils.PAPER
        notify = True
    elif key in [115, 99]:
        gesture = utils.SCISSORS
        notify = True

    if Pscore == 3 or Cscore == 3:   # 둘 중에 3번 이기면 종료
        stop = True
        if Cscore > Pscore:
            print('Game over, computer wins...')
        else:
            print('Game over, player wins!!!')

f.close()
cv2.destroyAllWindows()
cam.close()