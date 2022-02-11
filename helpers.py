from PIL import Image
import cv2
import os
import pytesseract
from constants import *
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def printLog(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{current_time}: {message}")


def formatSeconds(s):
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def compareImage(img1, img2):
    image = cv2.imread(img1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    image = cv2.imread(img2)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])

    percentageSimilarity = cv2.compareHist(histogram, histogram1, 0)
    # print(img1, img2, percentageSimilarity)
    if percentageSimilarity > similarityTreshhold:
        return True
    else:
        return False


def compareImage2(img1, img2):
    image = cv2.imread(img1)
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

    image = cv2.imread(img2)
    histogram1 = cv2.calcHist([image], [0], None, [256], [0, 256])

    percentageSimilarity = cv2.compareHist(histogram, histogram1, 0)
    # print(img1, img2, percentageSimilarity)
    if percentageSimilarity > similarityTreshholdQuiz:
        return True
    else:
        return False


def addStopTimer(hour, minue):
    now = datetime.now()
    later = now.replace(hour=hour, minute=minue, second=0, microsecond=0)
    time_diff = later - now
    later_time = time_diff.seconds
    hours, minutes, seconds = formatSeconds(later_time)
    printLog(
        f"Timer will stop program in {hours} hours, {minutes} minute and {seconds} seconds..."
    )
    if now > later:
        printLog("Timer time is up. Quitting program...")
        quit()


def checkRepeatEnd():
    # Get string from SS
    image = cv2.imread("temp/repeatWindow.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")

    # Process Strings
    if REPEAT_BATTLE_RESULTS in data:
        if MAX_LEVEL in data:
            return MAX_LEVEL
        elif INSUFFICIENT_ENERGY in data:
            return INSUFFICIENT_ENERGY
        elif LOST_BATTLE in data:
            return LOST_BATTLE
        else:
            return REPEAT_BATTLE_RESULTS
    else:
        return REPEAT_BATTLE_ONGOING


def checkEnergy():
    # Get string from SS
    image = cv2.imread("temp/screen.png")

    top_x = 375
    top_y = 225
    bottom_x = 900
    bottom_y = 335

    image = image[top_y:bottom_y, top_x:bottom_x]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")

    print(data)
    if NOT_ENOUGH_ENERGY in data:
        return False
    elif SORT_REWARDS in data:
        return SORT_REWARDS
    else:
        return True


def checkQuizEvent():
    try:
        # Get string from SS
        image = cv2.imread("temp/quizevent.png")

        top_x = 340
        top_y = 110
        bottom_x = 915
        bottom_y = 230

        image = image[top_y:bottom_y, top_x:bottom_x]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        data = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")
        # print("Quiz event data: ", data)

        if QUIZ_EVENT in data or MANA_REWARD in data:
            printLog("Quiz Event detected.")

            boxOptions = compareQuizBox()

            try:
                index = data.index(IN_TOTAL)
                thingsToSelect = int(data[index - 2])
            except Exception as e:
                printLog(f"Error finding number. {e}")
                printLog("Attempting backup check for number...")
                index = data.index(LEFT_BRACKET)
                thingsToSelect = int(data[index + 1])

            printLog(f"Number of items to select: {thingsToSelect}")

            quizType = None

            if ELLIA_PUZZLE in data or ELLIA_PUZZLE_2 in data:
                quizType = ELLIA_QUIZ
            elif EXCLUDING_BOSS in data:
                quizType = NON_BOSS_QUIZ
            elif ALL_BOSS in data or ALL_BOSS_2 in data:
                quizType = BOSS_QUIZ
            else:
                printLog("Puzzle does no match any case.")

            return quizType, boxOptions, thingsToSelect

        else:
            printLog("No quiz event detected. Continuing to refill energy...")
            return -1, -1, -1
    except Exception as e:
        printLog(f"Check quiz event error. {e}")


def compareQuizBox():
    # Get full path
    pathToDir = os.getcwd()

    # Get number of boss images
    file_path_boss = pathToDir + "/quizeventdata/boss"
    files_boss = os.listdir(file_path_boss)
    file_count_boss = len(files_boss)

    # Get number of ellia images
    file_path_ellia = pathToDir + "/quizeventdata/ellia"
    files_ellia = os.listdir(file_path_ellia)
    file_count_ellia = len(files_ellia)

    # Get number of normal images
    file_path_normal = pathToDir + "/quizeventdata/normal"
    files_normal = os.listdir(file_path_normal)
    file_count_normal = len(files_normal)

    checkList = []

    try:
        # Loop through 8 boxes from event to check against data
        for i in range(numberOfQuizBox):
            imageToCheck = rf"{pathToDir}\temp\quizevent\box{i}.png"
            found = False

            # Check normal
            if file_count_normal != 0 and found != True:
                for count, filename in enumerate(os.listdir(file_path_normal)):
                    imageDataPath = rf"{pathToDir}\quizeventdata\normal\{filename}"
                    issimilar = compareImage2(imageToCheck, imageDataPath)
                    # print (f"box{i}" ,filename, issimilar)
                    if issimilar:
                        found = True
                        checkList.append(NORMAL)
                        print(f"box{i} --- {filename}")
                        break

            # Check boss
            if file_count_boss != 0 and found != True:
                for count, filename in enumerate(os.listdir(file_path_boss)):
                    imageDataPath = rf"{pathToDir}\quizeventdata\boss\{filename}"
                    issimilar = compareImage2(imageToCheck, imageDataPath)
                    # print (f"box{i}" ,filename, issimilar)
                    if issimilar:
                        found = True
                        checkList.append(BOSS)
                        print(f"box{i} --- {filename}")
                        break

            # Check ellia
            if file_count_ellia != 0 and found != True:
                for count, filename in enumerate(os.listdir(file_path_ellia)):
                    imageDataPath = rf"{pathToDir}\quizeventdata\ellia\{filename}"
                    issimilar = compareImage2(imageToCheck, imageDataPath)
                    # print (f"box{i}" ,filename, issimilar)
                    if issimilar:
                        found = True
                        checkList.append(ELLIA)
                        print(f"box{i} --- {filename}")
                        break

            if found != True:
                checkList.append(-1)

        return checkList

    except Exception as e:
        printLog(f"Error checking. {e}")


def checkQuizSolved():
    image = cv2.imread("temp/quizevent.png")

    top_x = 320
    top_y = 220
    bottom_x = 925
    bottom_y = 350

    image = image[top_y:bottom_y, top_x:bottom_x]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")
    print("Quiz event result data: ", data)

    if QUIZ_SOLVED_SUCCESS in data:
        return True
    elif QUIZ_SOLVED_FAIL in data:
        return False
    else:
        return -1


def checkVictory():
    image = cv2.imread("temp/screen.png")

    top_x = 400
    top_y = 40
    bottom_x = 865
    bottom_y = 165

    image = image[top_y:bottom_y, top_x:bottom_x]
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")
    # print(data)
    if VICTORY in data:
        return VICTORY
    elif DEFEATED in data:
        return DEFEATED
    else:
        return "blank"


# print(compareQuizBox())
