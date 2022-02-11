from PIL import Image
from helpers import *
import cv2


def cropRepeatWindow():
    try:
        image = cv2.imread('temp/screen.png')

        y = 65
        x = 200
        h = 785
        w = 575

        crop_image = image[x:w, y:h]
        crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
        crop_pil = Image.fromarray(crop_image)
        crop_pil.save('temp/repeatWindow.png')

    except Exception as e:
        print(f"ERROR: {e} File not there yet - repeat window")


def cropRepeatWindowTitle():
    try:
        image = cv2.imread('temp/screen.png')

        y = 95
        x = 80
        h = 310
        w = 125

        crop_image = image[x:w, y:h]
        crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
        crop_pil = Image.fromarray(crop_image)
        crop_pil.save('temp/repeatWindowTitle.png')

    except:
        print("ERROR: File not there yet - repeat window title")


def cropQuizEvent():
    try:
        image = cv2.imread('temp/screen.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.save('temp/quizevent.png')
    except:
        print("ERROR: File not there yet. - crop quiz event")


def cropQuizBoxes():
    try:
        image = cv2.imread('temp/quizevent.png')

        for i in range(int(numberOfQuizBox/2)):
            top_x = 370 + i*145
            top_y = 280
            bottom_x = 475 + i*145
            bottom_y = 385

            crop_image = image[top_y:bottom_y, top_x:bottom_x]
            crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_image)
            crop_pil.save(f'temp/quizevent/box{i}.png')

        for i in range(int(numberOfQuizBox/2)):
            top_x = 370 + i*145
            top_y = 280 + 130
            bottom_x = 475 + i*145
            bottom_y = 385 + 130

            crop_image = image[top_y:bottom_y, top_x:bottom_x]
            crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_image)
            crop_pil.save(f'temp/quizevent/box{int(i+numberOfQuizBox/2)}.png')

    except:
        printLog("Error occured. - crop quiz boxes")


def cropQuizBoxesData(num):
    try:
        image = cv2.imread(f'temp/puzzle{num}.png')

        for i in range(int(numberOfQuizBox/2)):
            top_x = 370 + i*145
            top_y = 280
            bottom_x = 475 + i*145
            bottom_y = 385

            crop_image = image[top_y:bottom_y, top_x:bottom_x]
            crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_image)
            crop_pil.save(f'temp/quizevent/box{i}.png')

        for i in range(int(numberOfQuizBox/2)):
            top_x = 370 + i*145
            top_y = 280 + 130
            bottom_x = 475 + i*145
            bottom_y = 385 + 130

            crop_image = image[top_y:bottom_y, top_x:bottom_x]
            crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_image)
            crop_pil.save(f'temp/quizevent/box{int(i+numberOfQuizBox/2)}.png')

    except Exception as e:
        printLog(f"Error occured. {e}")


# cropQuizBoxesData(1)
# print(compareQuizBox())
# y = 65
# x = 200
# h = 785
# w = 575
# image = cv2.imread('temp/screen.png')
# print(image)
# crop_image = image[x:w, y:h]
# crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
# crop_pil = Image.
# crop_pil.save('temp/repeatWindow.png')
# cropRepeatWindow()