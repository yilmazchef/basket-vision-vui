import os
from time import sleep

import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import products

import mediapipe as mp
import math
from bridge import Bridge


class Label:
    def __init__(self, x, y, w, h, v, s):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.s = s

    def draw(self, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)

    def resize(self, w, h, img):
        cv2.putText(img, self.v, (self.x + w, self.y + h), cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)

    def color(self, rgb, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, rgb, self.s)

    def text(self, value, img):
        cv2.putText(img, value, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)


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
        return self.x < cursorX < self.x + self.w and self.y < cursorY < self.y + self.h

    def clicked(self, cursorX, cursorY):
        if self.x < cursorX < self.x + self.w and self.y < cursorY < self.y + self.h:
            return True
        else:
            return False


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

footer = ImageButton("components/footer.png")
buttonXL = ImageButton("products/large_product.png")

prodLeft01 = ImageButton("products/product_left_01.png")
prodLeft02 = ImageButton("products/product_left_02.png")
prodRight01 = ImageButton("products/product_right_01.png")
prodRight02 = ImageButton("products/product_right_02.png")

prevBtn = ImageButton("components/previous_button.png")
nextBtn = ImageButton("components/next_button.png")

hback, wback, cback = imgBack.shape

button_components = [
    ImageButton("components/logo.png"),
    ImageButton("components/footer.png"),
    ImageButton("components/basket.png"),
    ImageButton("components/previous_button.png"),
    ImageButton("components/next_button.png"),
    ImageButton("products/product_left_01.png"),
    ImageButton("products/product_left_02.png"),
    ImageButton("products/product_right_01.png"),
    ImageButton("products/product_right_02.png"),
    ImageButton("products/large_product.png")
]

# to avoid duplicated value inside calculator in event writing
delay_counter = 0

detector = HandDetector(detectionCon=0.8, maxHands=1)

while cap.isOpened() and success:

    success, imgBack = cap.read()
    imgBack = cv2.flip(imgBack, 1)

    imgResult = logoBtn.overlay(imgBack, 0, 0)
    imgResult = basketBtn.overlay(imgResult, wback - basketBtn.w, 0)

    # Header and Footer
    for storeIndex, storeImgBtn in enumerate(headers):
        imgResult = storeImgBtn.overlay(imgResult, (200 * (storeIndex + 1)), 0)

    imgResult = footer.overlay(imgResult, 0, hback - footer.h)

    # XL Product Info Box
    imgResult = buttonXL.overlay(imgResult, (wback - buttonXL.w) // 2, (hback - buttonXL.h) // 2)

    # Products with Thumbnail Photos
    imgResult = prodLeft01.overlay(imgResult, 0, 140)
    imgResult = prodLeft02.overlay(imgResult, 0, 280)
    imgResult = prodRight01.overlay(imgResult, wback - prodRight01.w, 140)
    imgResult = prodRight02.overlay(imgResult, wback - prodRight02.w, 280)

    # prev and next buttons
    imgResult = prevBtn.overlay(imgResult, 0, 480)
    imgResult = nextBtn.overlay(imgResult, wback - nextBtn.w, 480)

    # detection hands
    hands, imgBack = detector.findHands(imgBack, flipType=False)

    if len(hands) == 1:
        landmarks = hands[0]["lmList"]
        distance, _, imgResult = detector.findDistance(landmarks[8][:2], landmarks[12][:2], imgResult)
        x, y = landmarks[8][:2]

        if distance < 70:
            # button click send event when focused
            for button in button_components:
                if button.clicked(x, y) and delay_counter == 0:
                    print(f"button on {x, y} clicked!")
                    cvzone.putTextRect(imgResult, "Added to basket", )
                    # backendAPI = Bridge("POST", 0)
                    # backendAPI.postBasket()
                    # sleep(1)

        # avoid duplicates
        if delay_counter != 0:
            delay_counter += 1
            # i did not add value into display calculator
            # after passing 10 frames
            if delay_counter > 20:
                delay_counter = 0

    cv2.imshow("Image", imgResult)
    key = cv2.waitKey(1)
    if key == ord('q'):  # to stop the program
        cv2.destroyAllWindows()
        cap.release()
        exit(-1)
