import os

import cvzone
import cv2

import mediapipe as mp
import math
from cvzone.HandTrackingModule import HandDetector


class ImageButton:
    def __init__(self, imageUrl):
        self.img = cv2.imread(imageUrl, cv2.IMREAD_UNCHANGED)
        self.img = cv2.resize(self.img, (0, 0), None, 0.65, 0.65)
        self.h, self.w, c = self.img.shape
        self.x = 0
        self.y = 0
        self.clickEvent = print
        self.v = -1

    def text(self, v, img):
        self.v = v
        cv2.putText(img, self.v, (self.x + 25, self.y + 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    def defaultClick(self, img):
        self.text("click!", img)

    def overlay(self, imgBack, posX, posY):
        self.x = posX
        self.y = posY
        return cvzone.overlayPNG(imgBack, self.img, [posX, posY])

    def focused(self, cursorX, cursorY):
        self.img = cv2.resize(self.img, (0, 0), None, 1.20, 1.20)
        return self.x < cursorX < self.x + self.w and self.y < cursorY < self.y + self.h

    def onClick(self, clickEvent):
        self.clickEvent = clickEvent


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
cell_width = int(screen_width / total_no_of_cells * 0.65)
cell_height = int(screen_height / total_no_of_cells * 0.65)

logoBtn = ImageButton("components/logo.png")
basketBtn = ImageButton("components/basket.png")

storesPath = "stores"
storeNameList = os.listdir(storesPath)
headers = []
for storeImagePath in storeNameList:
    storeBtn = ImageButton(f"{storesPath}/{storeImagePath}")
    headers.append(storeBtn)

# imgLogo = cv2.imread("components/logo.png", cv2.IMREAD_UNCHANGED)
# imgLogo = cv2.resize(imgLogo, (0, 0), None, 0.65, 0.65)

# imgBasket = cv2.imread("components/basket.png", cv2.IMREAD_UNCHANGED)
# imgBasket = cv2.resize(imgBasket, (0, 0), None, 0.65, 0.65)

imgHeader = cv2.imread("components/header.png", cv2.IMREAD_UNCHANGED)
imgHeader = cv2.resize(imgHeader, (0, 0), None, 0.65, 0.65)

imgFooter = cv2.imread("components/footer.png", cv2.IMREAD_UNCHANGED)
imgFooter = cv2.resize(imgFooter, (0, 0), None, 0.65, 0.65)

imgPhotoXL = cv2.imread("products/large_product.png", cv2.IMREAD_UNCHANGED)
imgPhotoXL = cv2.resize(imgPhotoXL, (0, 0), None, 0.65, 0.65)

imgProductLeft01 = cv2.imread("products/product_left_01.png", cv2.IMREAD_UNCHANGED)
imgProductLeft01 = cv2.resize(imgProductLeft01, (0, 0), None, 0.65, 0.65)

imgProductLeft02 = cv2.imread("products/product_left_02.png", cv2.IMREAD_UNCHANGED)
imgProductLeft02 = cv2.resize(imgProductLeft02, (0, 0), None, 0.65, 0.65)

imgPreviousButton = cv2.imread("components/previous_button.png", cv2.IMREAD_UNCHANGED)
imgPreviousButton = cv2.resize(imgPreviousButton, (0, 0), None, 0.65, 0.65)

imgProductRight01 = cv2.imread("products/product_right_01.png", cv2.IMREAD_UNCHANGED)
imgProductRight01 = cv2.resize(imgProductRight01, (0, 0), None, 0.65, 0.65)

imgProductRight02 = cv2.imread("products/product_right_02.png", cv2.IMREAD_UNCHANGED)
imgProductRight02 = cv2.resize(imgProductRight02, (0, 0), None, 0.65, 0.65)

imgNextButton = cv2.imread("components/next_button.png", cv2.IMREAD_UNCHANGED)
imgNextButton = cv2.resize(imgNextButton, (0, 0), None, 0.65, 0.65)

hback, wback, cback = imgBack.shape

# hlogo, wlogo, clogo = imgLogo.shape
# hbasket, wbasket, cbasket = imgBasket.shape

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

    # using OOP components
    imgResult = logoBtn.overlay(imgBack, 0, 0)
    imgResult = basketBtn.overlay(imgResult, wback - basketBtn.w, 0)

    # WebCam or Background Stream
    # imgResult = cvzone.overlayPNG(imgBack, imgLogo, [0, 0])
    # imgResult = cvzone.overlayPNG(imgResult, imgBasket, [wback - wbasket, 0])

    # Header and Footer
    for storeIndex, storeImgBtn in enumerate(headers):
        imgResult = storeImgBtn.overlay(imgResult, (200 * (storeIndex + 1)), 0)

    imgResult = cvzone.overlayPNG(imgResult, imgFooter, [0, hback - hfooter])

    # XL Product Info Box
    imgResult = cvzone.overlayPNG(imgResult, imgPhotoXL, [(wback - wphotoXL) // 2, (hback - hphotoXL) // 2])

    # Products with Thumbnail Photos
    imgResult = cvzone.overlayPNG(imgResult, imgProductLeft01, [0, 200])
    imgResult = cvzone.overlayPNG(imgResult, imgProductLeft02, [0, 400])
    imgResult = cvzone.overlayPNG(imgResult, imgProductRight01, [wback - wProdR01, 200])
    imgResult = cvzone.overlayPNG(imgResult, imgProductRight02, [wback - wProdR02, 400])

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
