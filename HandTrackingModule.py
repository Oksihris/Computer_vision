import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelCom=1, detectionConf=0.5, trackConf =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelCom = modelCom
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.modelCom, self.detectionConf,
                                        self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw= True):
        imgRGB =cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosotion(self, img, handNo=0, draw=True):
        lmList =[]

        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id,cx,cy])
                # if draw:
                #     cv.circle(img,  (cx, cy), 10, (250, 150, 150), cv.FILLED)
        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)

        lmList = detector.findPosotion(img)

        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_TRIPLEX, 3, (255, 122, 255), thickness=2)

        cv.imshow("Image", img)
        cv.waitKey(1)


if __name__ =="__main__":
    main()