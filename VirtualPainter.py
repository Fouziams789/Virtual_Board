import cv2
import HandTrackingModule as htm
import numpy as np
import os
import pyautogui
import speech_converter as ttos
import uuid
from datetime import datetime
import numpy


def airoboard(session_start_time, name, image):

    cnt = 0
    flag = 0
    uu_id = uuid.uuid1()
    os.makedirs(str(uu_id))
    overlayList = []  # list to store all the images

    brushThickness = 25
    eraserThickness = 100
    drawColor = (0, 0, 255)  # setting red color

    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # defining canvas

    # images in header folder
    folderPath = "Header"
    myList = os.listdir(folderPath)  # getting all the images used in code
    # print(myList)
    open_cv_image = numpy.array(image)
    # Convert RGB to BGR
    ith = open_cv_image[:, :, ::-1].copy()
    print(ith)
    for imPath in myList:  # reading all the images from the folder
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)  # inserting images one by one in the overlayList
    header = overlayList[0]  # storing 1st image
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)  # height

    detector = htm.handDetector(detectionCon=0.85, maxHands=1)  # making object
    screen_size = pyautogui.size()
    # initialize the object
    video = cv2.VideoWriter('Recording.avi',
                           cv2.VideoWriter_fourcc(*'MJPG'),
                           20, screen_size)

    print("Recording.....")
    while True:

        # click screen shot
        screen_shot_img = pyautogui.screenshot()

        # convert into array
        frame = np.array(screen_shot_img)

        # change from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # write frame
        video.write(frame)

        # 1. Import image
        success, img = cap.read()
        img = cv2.flip(img, 1)  # for neglecting mirror inversion

        # 2. Find Hand Landmarks
        img = detector.findHands(img)  # using functions fo connecting landmarks
        lmList, bbox = detector.findPosition(img,
                                             draw=False)  # using function to find specific landmark position,draw false means no circles on landmarks

        if len(lmList) != 0:
            # print(lmList)
            x1, y1 = lmList[8][1], lmList[8][2]  # tip of index finger
            x2, y2 = lmList[12][1], lmList[12][2]  # tip of middle finger

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            # print(fingers)

            # 4. If Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                # print("Selection Mode")
                # checking for click
                if y1 < 125:
                    if 0 < x1 < 200:
                        print(x1)
                        # take screenshot using pyautogui
                        im = pyautogui.screenshot()
                        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                        # writing it to the disk using opencv
                        # cv2.imwrite("image1.jpg", image)
                        t = datetime.now()
                        t = str(t).replace(" ", "")
                        im.save("{}/{}.jpg".format(uu_id, t))
                        # from PIL import ImageGrab
                        # ss_region = (300, 300, 600, 600)
                        # ss_img = ImageGrab.grab(ss_region)
                        # ss_img.save("SS3.jpg")
                    if 250 < x1 < 450:  # if i m clicking at red brush
                        header = overlayList[0]
                        drawColor = (0, 0, 255)
                        if not flag == 1:
                            flag = 1
                            cnt = 0
                        if flag == 1:
                            cnt += 1
                        if cnt == 5:
                            ttos.text_to_speech("Red")
                            cnt = 0
                    elif 550 < x1 < 750:  # if i m clicking at blue brush
                        header = overlayList[1]
                        drawColor = (255, 0, 100)
                        if not flag == 1:
                            flag = 1
                            cnt = 0
                        if flag == 1:
                            cnt += 1
                        if cnt == 5:
                            ttos.text_to_speech("Blue")
                            cnt = 0
                    elif 800 < x1 < 950:  # if i m clicking at green brush
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                        if not flag == 1:
                            flag = 1
                            cnt = 0
                        if flag == 1:
                            cnt += 1
                        if cnt == 5:
                            ttos.text_to_speech("Green")
                            cnt = 0
                    elif 1050 < x1 < 1200:  # if i m clicking at eraser
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                        if not flag == 1:
                            flag = 1
                            cnt = 0
                        if flag == 1:
                            cnt += 1
                        if cnt == 5:
                            ttos.text_to_speech("Eraser")
                            cnt = 0
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor,
                              cv2.FILLED)  # selection mode is represented as rectangle

            # 5. If Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)  # drawing mode is represented as circle
                # print("Drawing Mode")
                if xp == 0 and yp == 0:  # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                    xp, yp = x1, y1  # so to avoid that we set xp=x1 and yp=y1
                # till now we are creating our drawing but it gets removed as everytime our frames are updating so we have to define our canvas where we can draw and show also

                # eraser
                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor,
                             brushThickness)  # gonna draw lines from previous coodinates to new positions
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp, yp = x1, y1  # giving values to xp,yp everytime

            # merging two windows into one imgcanvas and img

        # 1 converting img to gray
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

        # 2 converting into binary image and thn inverting
        _, imgInv = cv2.threshold(imgGray, 50, 255,
                                  cv2.THRESH_BINARY_INV)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

        imgInv = cv2.cvtColor(imgInv,
                              cv2.COLOR_GRAY2BGR)  # converting again to gray bcoz we have to add in a RGB image i.e img

        # add original img with imgInv ,by doing this we get our drawing only in black color
        img = cv2.bitwise_and(img, imgInv)

        # add img and imgcanvas,by doing this we get colors on img
        img = cv2.bitwise_or(img, imgCanvas)

        # setting the header image
        img[0:128, 0:1280] = header
        # ith = cv2.resize(ith, (300, 200))
        ith = cv2.resize(ith, (300, 200))
        ith = ith / 255.0
        ith = np.reshape(ith, (1, 300, 200, 1))
        # print(header)
        img[130:330, 0:300] = ith # on our frame we are setting our JPG image acc to H,W of jpg images
        cv2.putText(img, str(name), (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.putText(img, "Session_Started: "+str(name) + " "+str(session_start_time), (50, 700), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        # x, y, w, h = 0, 0, 175, 75
        # cv2.rectangle(img, (100, 70), (x + w, y + h), (0, 0, 0), -1)
        # cv2.rectangle(img, pt1=(200, 300), pt2=(100, 100), color=(255, 255, 0), thickness=-1)

        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)

        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break
    cv2.destroyAllWindows()
    video.release()