from ppadb.client import Client
from PIL import Image

# import numpy
import time
import os
from helpers import *
from cropping import *
from constants import *
from subprocess import check_output, CalledProcessError

# from telethon import TelegramClient
# from telethon import utils


try:
    # adb_ouput = check_output(["adb", "devices"])
    os.system('cmd /c "adb devices"')
except CalledProcessError as e:
    print(e.returncode)

adb = Client(host="127.0.0.1", port=5037)
# try:
devices = adb.devices()
if len(devices) == 0:
    print("No devices found.")
    print("Attempting to add bluestack...")
    try:
        os.system('cmd /c "adb connect 127.0.0.1:5555"')
        devices = adb.devices()
    except Exception as e:
        print("Error:", e)
        quit()
device = devices[0]

# try:
#     client = TelegramClient("me", api_id, api_hash)
# except Exception as e:
#     printLog(f"Connection to telegram failed. {e}")


def takeSS():
    image = device.screencap()
    with open("temp/screen.png", "wb") as f:
        f.write(image)


def takeSS2(num):
    image = device.screencap()
    with open(f"temp/puzzle{num}.png", "wb") as f:
        f.write(image)


def solveQuiz(quizType, quizOptions, thingsToSelect):
    printLog(f"Select all {quizType} detected")
    printLog("Attempting to solve Quiz Event ...")

    elliaCount = 0
    bossCount = 0
    normalCount = 0
    unknownCount = 0

    remainingSelection = thingsToSelect

    for i in range(len(quizOptions)):
        if str(quizOptions[i]) in ELLIA:
            elliaCount += 1
        elif str(quizOptions[i]) in BOSS:
            bossCount += 1
        elif str(quizOptions[i]) in NORMAL:
            normalCount += 1
        else:
            unknownCount += 1

    if quizType == ELLIA_QUIZ:
        for i in range(len(quizOptions)):
            if str(quizOptions[i]) in ELLIA:
                tapCoordinates = boxFormat[i]
                printLog(f"Selecting box{i}")
                device.shell(
                    f"input touchscreen tap {tapCoordinates[0]} {tapCoordinates[1]}"
                )

                elliaCount -= 1
            time.sleep(1)

    elif quizType == BOSS_QUIZ:
        for i in range(len(quizOptions)):
            if str(quizOptions[i]) in BOSS:
                tapCoordinates = boxFormat[i]
                printLog(f"Selecting box{i}")
                device.shell(
                    f"input touchscreen tap {tapCoordinates[0]} {tapCoordinates[1]}"
                )

                bossCount -= 1
            time.sleep(1)

    elif quizType == NON_BOSS_QUIZ:
        nonBossCount = numberOfQuizBox - bossCount
        for i in range(len(quizOptions)):
            if str(quizOptions[i]) not in BOSS:
                tapCoordinates = boxFormat[i]
                printLog(f"Selecting box{i}")
                device.shell(
                    f"input touchscreen tap {tapCoordinates[0]} {tapCoordinates[1]}"
                )

                nonBossCount -= 1
            time.sleep(1)

    # Select OK to solve quiz
    printLog("Selection of boxes complete... Submitting answers now...")
    device.shell("input touchscreen tap 645 600")


def checkAndSolveQuiz():
    tries = 3
    while tries > 0:
        time.sleep(5)
        takeSS()
        cropQuizEvent()
        cropQuizBoxes()
        quizType, quizOptions, thingsToSelect = checkQuizEvent()

        print(quizType, quizOptions, thingsToSelect)

        if quizType != -1:
            solveQuiz(quizType, quizOptions, thingsToSelect)

            # Give 5 Sec to load
            time.sleep(5)
            takeSS()
            cropQuizEvent()
            isSolved = checkQuizSolved()

            if isSolved and isSolved != -1:
                # Select OK to clear correct dialog
                device.shell("input touchscreen tap 645 440")
                solved = True
                printLog("Quiz Solved.")

                # Select +190 Recharge
                time.sleep(1)
                device.shell("input touchscreen tap 815 350")
                break

            elif not isSolved and isSolved != -1:
                # Select OK to clear wrong dialog
                device.shell("input touchscreen tap 645 440")
                printLog(f"Quiz NOT solved. Retrying... {tries} tries left.")
                # Retry solving

            else:
                print(isSolved)
                printLog("Something went wrong... Exiting Program...")
                quit()

            tries -= 1

        else:
            break


def refillRepeatEnergy():
    # Select Plus Icon
    time.sleep(1)
    device.shell("input touchscreen tap 770 170")

    # Select Shop
    time.sleep(1)
    device.shell("input touchscreen tap 525 445")

    # Select +190 Recharge
    time.sleep(1)
    device.shell("input touchscreen tap 815 350")

    # device.shell('input touchscreen tap 530 350')  # Cheap refill

    checkAndSolveQuiz()

    # Select Yes
    time.sleep(1)
    device.shell("input touchscreen tap 525 445")

    # Select OK
    time.sleep(1)
    device.shell("input touchscreen tap 645 435")

    # Select Close
    time.sleep(1)
    device.shell("input touchscreen tap 645 625")

    time.sleep(1)


def refillEnergy():
    # Select Shop
    time.sleep(1)
    device.shell("input touchscreen tap 525 445")

    # Select +190 Recharge
    time.sleep(1)
    device.shell("input touchscreen tap 815 350")

    # device.shell('input touchscreen tap 530 350')  # Cheap refill

    checkAndSolveQuiz()

    # Select Yes
    time.sleep(1)
    device.shell("input touchscreen tap 525 445")

    # Select OK
    time.sleep(2)
    device.shell("input touchscreen tap 645 435")

    # Select Close
    time.sleep(1)
    device.shell("input touchscreen tap 645 625")

    # Select Repeat Battle x10
    time.sleep(1)
    device.shell("input touchscreen tap 1080 510")

    time.sleep(1)


def handleSortRewards():
    print("sorting rewards...")
    time.sleep(1)
    device.shell("input touchscreen tap 530 435")
    time.sleep(1)
    device.shell("input touchscreen tap 1080 510")


def handleSellSelected():
    # select sell selected
    time.sleep(1)
    device.shell("input touchscreen tap 1130 635")
    time.sleep(1)
    device.shell("input touchscreen tap 970 640")
    time.sleep(1)
    device.shell("input touchscreen tap 635 435")
    time.sleep(1)
    device.shell("input touchscreen tap 530 440")
    time.sleep(1)
    device.shell("input touchscreen tap 530 480")


def replayRepeat():
    # Select Replay
    time.sleep(1)
    device.shell("input touchscreen tap 680 620")

    # Select Repeat Battle x10
    time.sleep(1)
    device.shell("input touchscreen tap 1080 510")

    printLog("Checking for sufficient energy...")
    time.sleep(5)
    takeSS()
    isEnergyEnough = checkEnergy()
    if not isEnergyEnough:
        printLog("Energy insufficient... Refilling energy...")
        refillEnergy()
    elif isEnergyEnough == SORT_REWARDS:
        handleSortRewards()
    else:
        printLog("Energy sufficient... Continuing to battle...")


def checkInRepeatWindow():
    takeSS()
    cropRepeatWindowTitle()
    inWindow = compareImage(
        "temp/repeatWindowTitle.png", "images/repeatWindowTitle.png"
    )
    return inWindow


def runRepeat():
    # Check repeat battle window open
    timesFailed = 0
    try:
        while True:
            # Timer to stop. Comment to remove.
            # addStopTimer(10,0)
            inWindow = checkInRepeatWindow()
            if inWindow:
                takeSS()
                cropRepeatWindow()
                checkRepeat = checkRepeatEnd()
                if REPEAT_BATTLE_ONGOING in checkRepeat:
                    printLog("Ongoing Battle")
                    time.sleep(checkDelay)
                    pass
                elif MAX_LEVEL in checkRepeat:
                    printLog("A monster has reached max level...")
                    printLog("Stopping repeat...")
                    break
                elif INSUFFICIENT_ENERGY in checkRepeat:
                    printLog("Insufficient energy. Refilling energy...")
                    # quit()
                    refillRepeatEnergy()
                    replayRepeat()
                    pass
                elif LOST_BATTLE in checkRepeat:
                    printLog("Lost in battle. Replaying...")
                    # client.send_message('me', f'Lost in battle. Times lost :{timesFailed}')
                    timesFailed += 1
                    printLog(f"Times failed since start of bot: {timesFailed}")
                    # sendEmail("Summoners war notification", f"Lost in battle, number of times lost: {timesFailed}")
                    # handleSellSelected()
                    replayRepeat()
                    pass
                else:
                    printLog("Battle ended. Replaying...")
                    # handleSellSelected()
                    replayRepeat()
                    pass
                time.sleep(10)
            else:
                printLog("Please open repeat battle window.")
                time.sleep(10)
    except KeyboardInterrupt:
        printLog(f"Times failed since start of bot: {timesFailed}")
        pass


def runRepeatDimensionalHole():
    # Check repeat battle window open
    timesFailed = 0
    try:
        while True:
            # Timer to stop. Comment to remove.
            # addStopTimer(10,0)
            inWindow = checkInRepeatWindow()
            if inWindow:
                takeSS()
                cropRepeatWindow()
                checkRepeat = checkRepeatEnd()
                if REPEAT_BATTLE_ONGOING in checkRepeat:
                    printLog("Ongoing Battle")
                    time.sleep(checkDelay)
                    pass
                elif MAX_LEVEL in checkRepeat:
                    printLog("A monster has reached max level...")
                    printLog("Stopping repeat...")
                    break
                elif INSUFFICIENT_ENERGY in checkRepeat:
                    printLog("Insufficient energy. Stopping BOT...")
                    break
                elif LOST_BATTLE in checkRepeat:
                    printLog("Lost in battle. Replaying...")
                    # client.send_message('me', f'Lost in battle. Times lost :{timesFailed}')
                    timesFailed += 1
                    printLog(f"Times failed since start of bot: {timesFailed}")
                    # sendEmail("Summoners war notification", f"Lost in battle, number of times lost: {timesFailed}")
                    replayRepeat()
                    pass
                else:
                    printLog("Battle ended. Replaying...")
                    replayRepeat()
                    pass
                time.sleep(10)
            else:
                printLog("Please open repeat battle window.")
                time.sleep(10)
    except KeyboardInterrupt:
        pass


def toaClimb():
    try:
        while True:
            takeSS()
            isVictory = checkVictory()
            if isVictory in VICTORY:
                # Click anywhere
                device.shell("input touchscreen tap 650 325")
                time.sleep(1)

                # Click anywhere for box
                device.shell("input touchscreen tap 650 325")
                time.sleep(2)

                # Click OK
                device.shell("input touchscreen tap 650 550")
                time.sleep(2)

                # Click Next Stage
                device.shell("input touchscreen tap 395 390")
                time.sleep(2)

                # Click Start Battle
                device.shell("input touchscreen tap 1090 515")
                time.sleep(1)
            elif isVictory in DEFEATED:
                printLog("Lost in battle... Exiting ToA climb...")
                break
            time.sleep(10)
            printLog("Ongoing battle...")

    except KeyboardInterrupt:
        pass


def main():
    while True:
        print("1. Normal BOT")
        print("2. Repeat Battle BOT")
        print("3. Repeat Battle for Dimensional Hole BOT")
        print("4. ToA Climbing")
        print("5. Quit")
        choice = input("Choice: ")

        if choice.isdigit():
            choice = int(choice)
        else:
            print("Enter a digit.")
            continue

        if choice == 1:
            print("Function not ready yet.")
        elif choice == 2:
            print("Entering repeat battle BOT...")
            runRepeat()
        elif choice == 3:
            print("Entering repeat battle BOT for Dimensional Hole...")
            runRepeatDimensionalHole()
        elif choice == 4:
            print("Entering ToA climb...")
            toaClimb()
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Enter digit 1 - 3.")


main()

# refillEnergy()

# takeSS()
# cropQuizEvent()
# checkQuizEvent()
# cropQuizBoxes()
# print(compareQuizBox())

# replayRepeat()

# checkAndSolveQuiz()

# takeSS()
# cropQuizEvent()
# checkQuizSolved()
