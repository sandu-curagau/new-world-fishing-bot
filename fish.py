import os
from pyautogui import *
import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController

# INDEX
# Section 1 - CHANGABLE VARIABLES
# Section 2 - DECLARATIONS AND METHODS
# Section 3 - Execution

def main():
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ START - CHANGABLE VARIABLES (section 1 of 3)

    # Max cast is 1.9 secs
    # Base time it will always cast at
    castingBaseTime = 1.0
    
    # Max random amount of time to add to the base
    castingRandom = .4

    # How long to slack the line
    lineSlackTime = 1.5

    # Adding randomness to the wait times for the animations
    animationSleepTime = .1 + (.1 * random.random())

    # Free cam key
    freeCamKey = "alt"

    # TYPE OF WATER USER IS FISHING IN. EXPECTING A STRING, 'FRESH' OR 'SALT'
    typeOfWater = "FRESH"

    # TO KILL THE SCRIPT BY DEFAULT PRESS DELETE, FEEL FREE TO CHANGE. 
    # SPECIAL KEYS DO EXAMPLE: keyboard.Key.delete or keyboard.Key.tab or keyboard.Key.f11
    # NORMAL KEYS DO EXAMPLE: keyboard.KeyCode('r')
    # MORE INFO AT https://pynput.readthedocs.io/en/latest/keyboard.html
    def on_press(key):
        if (key == keyboard.Key.delete):
            print("Killed fish bot.")
            keyboard.Listener.stop
            os._exit(1)  
    keyboardListener = keyboard.Listener(on_press=on_press)
    keyboardListener.start()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ END - CHANGABLE VARIABLES (section 1 of 3)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ START - DECLARATIONS AND METHODS (section 2 of 3)
    keyboardController = KeyboardController()
    timesToCastUntilRepair = 25

    # REUSABLE METHOD TO SIMULATE MOUSE CLICKS ON ANY POSITION WE WANT
    def click(x,y):
        pyautogui.moveTo(x, y, 0.5)
        pyautogui.click()
        time.sleep(1)

    # METHOD TO EXECUTE THE REPAIRING FISHING ROD ALGORITHM
    def repairRod():
        print("Repairing fishing rod.")

        # Open inventory
        keyboardController.press(Key.tab)
        time.sleep(0.05)
        keyboardController.release(Key.tab)
        time.sleep(1)

        # Click on fishing rod
        click(875, 520)
        time.sleep(1)

        # Click on repair
        click(970, 540)
        time.sleep(1)

        # Click on confirm
        click(955, 450)
        time.sleep(1)

        # Close inventory
        keyboardController.press(Key.tab)
        time.sleep(0.05)
        keyboardController.release(Key.tab)
        time.sleep(1)
    
    def equipRodAndBait():
        # Press F3 to pick up Fishing Rod
        keyboardController.press(Key.f3)
        time.sleep(0.05)
        keyboardController.release(Key.f3)
        time.sleep(1)

        # Press R to equip bait
        keyboardController.press('r')
        time.sleep(0.05)
        keyboardController.release('r')
        time.sleep(1)

        # Click on the 1st bait of Fresh/Salt water (option can be changed in section 1)
        if typeOfWater == "FRESH":
            click(1186, 453)
        elif typeOfWater == "SALT":
            click(1191, 591)
        else:
            click(1186, 453)
        time.sleep(1)
        
        # Click on equip bait button
        click(1492, 823)
        time.sleep(2)

    def antiAfkWalk(ignoreCondition):
        if random.randint(1, 5) == 5 | ignoreCondition:
            pyautogui.keyDown("a")
            time.sleep(.1)
            pyautogui.keyUp("a")
            time.sleep(.4)
            pyautogui.keyDown("d")
            time.sleep(.1)
            pyautogui.keyUp("d")

            time.sleep(.2)
            return True
        else:
            return False

    def fish():
        print(f"Casting {timesCasted} / {timesToCastUntilRepair} until repair.")

        # Screenshot
        sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
        # Calculating those times
        # castingTime = castingBaseTime + (castingRandom * random.random())
        castingTime = castingBaseTime

        # Hold the "Free Look" Button
        print("Holding Free Look Button")
        pydirectinput.keyDown(freeCamKey)
        time.sleep(0.5)

        # Like it says, casting
        print("Casting Line")
        pyautogui.mouseDown()
        time.sleep(1.3)
        pyautogui.mouseUp()

        # Looking for the fish icon, doing forced garbage collection
        while pyautogui.locate("imgs/fishIcon.png", sctImg, grayscale=True, confidence=.6) is None:
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

        # Hooking the fish
        print("Fish Hooked")
        pyautogui.click()
        time.sleep(animationSleepTime)

        # Keeps reeling into "HOLD Cast" text shows on screen
        while pyautogui.locate("imgs/holdCast.png", sctImg, grayscale=True, confidence=.55) is None:
            print("Reeling....")
            pyautogui.mouseDown()

            # If icon is in the orange area slack the line
            if pyautogui.locate("imgs/fishReelingOrange.png", sctImg, grayscale=True, confidence=.75) is not None:
                print("Slacking line...")
                pyautogui.mouseUp()
                time.sleep(lineSlackTime)

            # Uses a lot of memory if you don't force collection
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

            # Reel down time
            time.sleep(animationSleepTime)
            
        pyautogui.mouseUp()
        time.sleep(animationSleepTime)
        print("Caught Fish")

        time.sleep(animationSleepTime)

        # Release the "Free Look" Button
        print("Released Free Look Button")
        pydirectinput.keyUp(freeCamKey)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ END - DECLARATIONS AND METHODS (section 2 of 3)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ START - EXECUTION (section 3 of 3)

    # Finds all Windows with the title "New World"
    newWorldWindows = pyautogui.getWindowsWithTitle("New World")

    # Find the Window titled exactly "New World" (typically the actual game)
    for window in newWorldWindows:
        if window.title == "New World":
            newWorldWindow = window
            break

    # Select that Window
    newWorldWindow.activate()

    # Move your mouse to the center of the game window
    centerW = newWorldWindow.left + (newWorldWindow.width/2)
    centerH = newWorldWindow.top + (newWorldWindow.height/2)
    pyautogui.moveTo(centerW, centerH)

    # Clicky Clicky
    time.sleep(animationSleepTime)
    pyautogui.click()
    time.sleep(animationSleepTime)

    # Selecting the middle 3rd of the New World Window
    mssRegion = {"mon": 1, "top": newWorldWindow.top, "left": newWorldWindow.left + round(newWorldWindow.width/3), "width": round(newWorldWindow.width/3), "height": newWorldWindow.height}
 
    # Starting screenshotting object
    sct = mss.mss()

    # This should resolve issues with the first cast being short
    time.sleep(animationSleepTime * 3)

    while True:
        timesToCastUntilRepair = 30
        hasWalked = False
        repairRod()
        time.sleep(1)
        equipRodAndBait()
        while timesToCastUntilRepair > 0:
            try: 
                timesCasted = 0
                if hasWalked == False:
                    antiAfkWalk(True)
                    hasWalked = True
                time.sleep(2)

                while timesCasted < 5:
                    fish()
                    hasWalked = antiAfkWalk(False)
                    timesCasted += 1
                    timesToCastUntilRepair -= 1
            except Exception as e: print(e)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ END - EXECUTION (section 3 of 3)


# Runs the main function
if __name__ == '__main__':
    main()
