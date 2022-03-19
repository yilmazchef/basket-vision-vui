import cvzone
import cv2

import mediapipe as mp
import math
from cvzone.HandTrackingModule import HandDetector

fhd_width = 1920
fhd_height = 1080

shd_width = 1280
shd_height = 720

screen_width = shd_width
screen_height = shd_height

cap = cv2.VideoCapture(0)
cap.set(3, screen_width)
cap.set(4, screen_height)
success, imgBack = cap.read()

total_no_of_cells = 12
cell_width = screen_width / total_no_of_cells * 0.65
cell_height = screen_height / total_no_of_cells * 0.65

imgLogo = cv2.imread("components/logo.png", cv2.IMREAD_UNCHANGED)
imgLogo = cv2.resize(imgLogo, (0, 0), None, 0.65, 0.65)

imgHeader = cv2.imread("components/header.png", cv2.IMREAD_UNCHANGED)
imgHeader = cv2.resize(imgHeader, (0, 0), None, 0.65, 0.65)

imgFooter = cv2.imread("components/footer.png", cv2.IMREAD_UNCHANGED)
imgFooter = cv2.resize(imgFooter, (0, 0), None, 0.65, 0.65)

imgPhotoXL = cv2.imread("components/large_product.png", cv2.IMREAD_UNCHANGED)
imgPhotoXL = cv2.resize(imgPhotoXL, (0, 0), None, 0.65, 0.65)

imgProductLeft01 = cv2.imread("components/product_left_01.png", cv2.IMREAD_UNCHANGED)
imgProductLeft01 = cv2.resize(imgProductLeft01, (0, 0), None, 0.65, 0.65)

imgProductLeft02 = cv2.imread("components/product_left_02.png", cv2.IMREAD_UNCHANGED)
imgProductLeft02 = cv2.resize(imgProductLeft02, (0, 0), None, 0.65, 0.65)

imgPreviousButton = cv2.imread("components/previous_button.png", cv2.IMREAD_UNCHANGED)
imgPreviousButton = cv2.resize(imgPreviousButton, (0, 0), None, 0.65, 0.65)

imgProductRight01 = cv2.imread("components/product_right_01.png", cv2.IMREAD_UNCHANGED)
imgProductRight01 = cv2.resize(imgProductRight01, (0, 0), None, 0.65, 0.65)

imgProductRight02 = cv2.imread("components/product_right_02.png", cv2.IMREAD_UNCHANGED)
imgProductRight02 = cv2.resize(imgProductRight02, (0, 0), None, 0.65, 0.65)

imgNextButton = cv2.imread("components/next_button.png", cv2.IMREAD_UNCHANGED)
imgNextButton = cv2.resize(imgNextButton, (0, 0), None, 0.65, 0.65)

hback, wback, cback = imgBack.shape
hlogo, wlogo, clogo = imgLogo.shape
hheader, wheader, cheader = imgHeader.shape
hfooter, wfooter, cfooter = imgFooter.shape
hphotoXL, wphotoXL, cphotoXL = imgPhotoXL.shape

hProdL01, wProdL01, cProdL01 = imgProductLeft01.shape
hProdL02, wProdL02, cProdL02 = imgProductLeft02.shape
hProdR01, wProdR01, cProdR01 = imgProductRight01.shape
hProdR02, wProdR02, cProdR02 = imgProductRight02.shape

hNextBtn, wNextBtn, cNextBtn = imgNextButton.shape
hPrevBtn, wPrevBtn, cPrevBtn = imgPreviousButton.shape

detector = HandDetector(detectionCon=0.8, maxHands=2)

while cap.isOpened() and success:
    success, imgBack = cap.read()
    imgBack = cv2.flip(imgBack, 1)

    # WebCam or Background Stream
    imgResult = cvzone.overlayPNG(imgBack, imgLogo, [0, 0])

    # Header and Footer
    imgResult = cvzone.overlayPNG(imgResult, imgHeader, [wback - wheader - 220, 0])
    imgResult = cvzone.overlayPNG(imgResult, imgFooter, [0, (hback - hfooter)])

    # XL Product Info Box
    imgResult = cvzone.overlayPNG(imgResult, imgPhotoXL, [(wback - wphotoXL) // 2, (hback - hphotoXL) // 2])

    # Products with Thumbnail Photos
    imgResult = cvzone.overlayPNG(imgResult, imgProductLeft01, [0, 200])
    imgResult = cvzone.overlayPNG(imgResult, imgProductLeft02, [0, 400])
    imgResult = cvzone.overlayPNG(imgResult, imgProductRight01, [1072, 200])
    imgResult = cvzone.overlayPNG(imgResult, imgProductRight02, [1072, 400])

    # detection hands
    hands, imgBack = detector.findHands(imgBack, flipType=False)

    if len(hands) == 1:
        landmarks = hands[0]["lmList"]
        distance, _, imgResult = detector.findDistance(landmarks[8][:2], landmarks[12][:2], imgResult)
        x, y = landmarks[8][:2]

    cv2.imshow("Image", imgResult)
    key = cv2.waitKey(1)
    if key == ord('q'):  # to stop the program
        cv2.destroyAllWindows()
        cap.release()
        exit(-1)