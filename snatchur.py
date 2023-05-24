import pyautogui
import time
import os
import winsound

# Set the coordinates for the region you want to click and capture
click_x = 1732  # X-coordinate of the top-left corner of the point you want to click
click_y = 524  # Y-coordinate of the top-left corner of the point you want to click
screenshot_x = 378  # X-coordinate of the top-left corner of the screenshot region
screenshot_y = 164  # Y-coordinate of the top-left corner of the screenshot region
width = 1165  # Width of the screenshot region (number of pixels from the left of the screen to the start of the desired region)
height = 780  # Height of the screenshot region (number of pixels from the top of the screen to the start of the desired region)

shouldClick = True # Determine if a click somewhere should happen before taking a screenshot

delayInitial = 5
delayBeforeClick = 2
delayBeforeScreenshot = 4 # Increase this if pages take a while to load

screenshotCounter = 1 # Used to append page number at the end of every screenshot's filename
screenshotsDirectory = str(int(time.time())) # The name of the directory where screenshots will be saved (if no name is specified, the current Unix timestamp will be used)
screenshotFormat = '.png' # The file extension of the screenshots (can either be.jpg or.png)

numberOfScreenshots = 5 # The number of screenshots you want to save (use -1 for infinite)

def get_user_input():
    snatch_init()

def snatch_init():
    global screenshotCounter
    # Wait for a brief moment
    print('-- MAKE SURE THE PART OF THE SCREEN YOU WANT TO SNATCH IS VISIBLE -- ')
    time.sleep(2)
    print('Preparing to snatch...')
    time.sleep(delayInitial)

    # Perform action for how many screenshots you want to save
    for i in range(numberOfScreenshots):
        # Wait for a brief moment
        time.sleep(delayBeforeScreenshot)

        # Capture the screenshot of the specified region (make sure screnshots region exists)
        print('| Took a screenshot!')
        if not os.path.exists(screenshotsDirectory):
            os.makedirs(screenshotsDirectory)
        screenshot = pyautogui.screenshot(region=(screenshot_x, screenshot_y, width, height))
        play_beep()

        # Move the mouse to the desired location and click
        if shouldClick:
            print('Click...')
            time.sleep(delayBeforeClick)
            pyautogui.moveTo(click_x, click_y)
            pyautogui.click()

        # If the selected screenshot format is .jpg, convert the screenshot to RGB format (aka .jpg)
        if screenshotFormat == '.jpg':
            screenshot = screenshot.convert('RGB')

        filename = screenshotsDirectory + '--' + str(screenshotCounter) + screenshotFormat
        screenshot.save(screenshotsDirectory + '/' + filename)
        screenshotCounter += 1

# Play the system beep sound
def play_beep():
    winsound.Beep(920, 50)  # Frequency: 440 Hz, Duration: 1000 ms

# Begin by getting user input
get_user_input()