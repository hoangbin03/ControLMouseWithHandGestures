import cv2
import time
import numpy as np
import module2 as m
import autopy
import pyautogui

wCam, hCam = 640, 480
pTime = 0
smoothenImg = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = m.handDetector(maxHands=1)
frameR = 100 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cap.set(10, 100)
wScr, hScr = autopy.screen.size()
prev_y = None

while True:
    # Tìm các điểm mốc trên tay
    success, imgO = cap.read()
    img = cv2.flip(imgO, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    # Lấy đầu ngón trỏ, ngón giữa và ngón cái
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # ngón trỏ
        x2, y2 = lmList[12][1:]  # ngón giữa
        x3, y3 = lmList[4][1:]  # ngón cái

        # Kiểm tra ngón tay nào đang giơ lên
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Chỉ ngón trỏ: chế độ di chuyển
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # Chuyển đổi tọa độ
            x4 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y4 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Làm mịn giá trị
            clocX = plocX + (x4 - plocX) / smoothenImg
            clocY = plocY + (y4 - plocY) / smoothenImg

            # Di chuyển chuột
            autopy.mouse.move(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), -1)
            plocX, plocY = clocX, clocY

        # Ngón trỏ và ngón giữa chạm nhau: chế độ nhấp chuột phải
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # Tìm khoảng cách giữa hai ngón tay
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # Nhấp chuột nếu khoảng cách ngắn
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), -1)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)

        # Ngón trỏ và ngón cái giơ lên: chế độ nhấp chuột trái
        elif fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # Tìm khoảng cách giữa hai ngón tay
            length, img, lineInfo = detector.findDistance(4, 8, img)
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), -1)
            autopy.mouse.click(autopy.mouse.Button.LEFT)

        # Ngón trỏ và ngón út giơ lên: cuộn chuột lên
        elif fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0:
            pyautogui.scroll(100)

        # Chỉ ngón út giơ lên: cuộn chuột xuống    
        elif fingers[1] == 0 and fingers[4] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0:
            pyautogui.scroll(-100)
        
  
    # Tốc độ khung hình
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
    #  Hiển thị
    cv2.imshow('Điều khiển chuột máy tính', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
