import pyautogui
import re
import time
import os
from os import system
import subprocess
import pygame
from colorama import init as colorama_init
from termcolor import cprint
import img2pdf

colorama_init()

system("title " + 'snatchur (by elevchyt)')

# Set the coordinates for the region you want to click and capture
click_x = 1732  # X-coordinate of the point you want to click
click_y = 524  # Y-coordinate of the point you want to click
screenshot_x = 378  # X-coordinate of the top-left corner of the screenshot region
screenshot_y = 164  # Y-coordinate of the top-left corner of the screenshot region
width = 1165  # Width of the screenshot region (number of pixels from the left of the screen to the start of the desired region)
height = 780  # Height of the screenshot region (number of pixels from the top of the screen to the start of the desired region)
scrollPixels = 100 # Amount of pixels to scroll before clicking

isClickEnabled = False # Determine if a click somewhere should happen before taking a screenshot
isScrollEnabled = False # Determine if a mousewheel scroll should happen before taking a screenshot
isPdfExportEnabled = False # Determine if a PDF should be generated using the screenshots
isSoundEnabled = True # Determine if sounds should be played (on screenshot)

delayInitial = 5
delayBeforeClick = 2
delayBeforeScreenshot = 4 # Increase this if pages take a while to load

screenshotCounter = 1 # Used to append page number at the end of every screenshot's filename
screenshotsDirectory = str(int(time.time())) # The name of the directory where screenshots will be saved (if no name is specified, the current Unix timestamp will be used)
screenshotFormat = '.png' # The file extension of the screenshots (can either be .png or.jpg)

numberOfScreenshots = 1 # The number of screenshots you want to save

def get_user_input():
    # Get name of the screenshots directory
    global screenshotsDirectory, isClickEnabled, screenshotFormat, screenshot_x, screenshot_y, click_x, click_y, width, height, isSoundEnabled, numberOfScreenshots, isPdfExportEnabled, isScrollEnabled, scrollPixels
    screenshotsDirectory = input("Enter the name of the screenshots directory: ")
    if screenshotsDirectory == "":
        screenshotsDirectory = str(int(time.time()))
        cprint("Screenshots directory name not specified. Using current Unix timestamp.", "yellow")
    time.sleep(1)

    # Get the number of screenshots to take
    numberOfScreenshots = input("How many screenshots do you want to take?: ")
    if numberOfScreenshots == "":
        numberOfScreenshots = 1
    else:
        numberOfScreenshots = abs(int(numberOfScreenshots))
    time.sleep(1)
    
    # Get the screenshot format
    screenshotFormat = input("Enter the file extension of the screenshots (png/jpg - default is png): ")
    if screenshotFormat == "png" or screenshotFormat == ".png":
        screenshotFormat = '.png'
    elif screenshotFormat == "jpg" or screenshotFormat == ".jpg":
        screenshotFormat = '.jpg'
    else:
        screenshotFormat = '.png'
        cprint('(Setting .png as screenshot format)', "yellow")
    time.sleep(1)

    # Get if a click should happen before taking a screenshot
    isClickEnabled = input("Do you want to click somewhere before taking a screenshot? (y/n): ")
    if isClickEnabled == "y" or isClickEnabled == "Y":
        isClickEnabled = True
    elif isClickEnabled == "n" or isClickEnabled == "N":
        isClickEnabled = False
    else:
        isClickEnabled = False
        cprint('(Disabling click)', "yellow")
    time.sleep(1)

    # Get click point coordinates (if isClickEnabled is True)
    if isClickEnabled:
        click_x = input("Enter the X-coordinate of the top-left corner of the point you want to click (in pixels): ")
        if click_x == "":
            click_x = 1732
        else:
            click_x = abs(int(click_x))
        time.sleep(1)
        
        click_y = input("Enter the Y-coordinate of the top-left corner of the point you want to click (in pixels): ")
        if click_y == "":
            click_y = 524
        else:
            click_y = abs(int(click_y))
        time.sleep(1)

    # Get if a scroll should happen before clicking or taking a screenshot
    isScrollEnabled = input("Do you want to scroll before taking a screenshot? (y/n): ")
    if isScrollEnabled == "y" or isScrollEnabled == "Y":
        isScrollEnabled = True
    elif isScrollEnabled == "n" or isScrollEnabled == "N":
        isScrollEnabled = False
    else:
        isScrollEnabled = False
        cprint('(Disabling scroll)', "yellow")
    time.sleep(1)

    # Get scroll amount (if isScrollEnabled is True)
    if isScrollEnabled:
        if isClickEnabled:
            scrollPixels = input("Enter the amount of pixels to scroll before clicking: ")
        else:
            scrollPixels = input("Enter the amount of pixels to scroll before taking screenshot: ")

        if scrollPixels == "":
            scrollPixels = 100
        else:
            scrollPixels = abs(int(scrollPixels))
        time.sleep(1)

    # Get screenshot region coordinates
    screenshot_x = input("Enter the X-coordinate of the top-left corner of the screenshot region (in pixels): ")
    if screenshot_x == "":
        screenshot_x = 378
    else:
        screenshot_x = abs(int(screenshot_x))
    time.sleep(1)
    
    screenshot_y = input("Enter the Y-coordinate of the top-left corner of the screenshot region (in pixels): ")
    if screenshot_y == "":
        screenshot_y = 164
    else:
        screenshot_y = abs(int(screenshot_y))
    time.sleep(1)

    # Get screenshot region width
    width = input("Enter the width of the screenshot region (in pixels): ")
    if width == "":
        width = 1165
    else:
        width = abs(int(width))
    time.sleep(1)

    # Get screenshot region height
    height = input("Enter the height of the screenshot region (in pixels): ")
    if height == "":
        height = 780
    else:
        height = abs(int(height))
    time.sleep(1)
    
    # Get if a PDF should be generated using the screenshots
    isPdfExportEnabled = input("Do you want to generate a PDF using the screenshots? (y/n): ")
    if isPdfExportEnabled == "y" or isPdfExportEnabled == "Y":
        isPdfExportEnabled = True
    elif isPdfExportEnabled == "n" or isPdfExportEnabled == "N":
        isPdfExportEnabled = False
    else:
        isPdfExportEnabled = False
        cprint('(Disabling PDF export)', "yellow")
    time.sleep(1)
    
    # Get if sound is enabled
    isSoundEnabled = input("Do you want to play a sound on screenshot capture? (y/n): ")
    if isSoundEnabled == "y" or isSoundEnabled == "Y":
        isSoundEnabled = True
    elif isSoundEnabled == "n" or isSoundEnabled == "N":
        isSoundEnabled = False
    else:
        isSoundEnabled = True
        cprint('(Enabling screenshot sound)', "yellow")
    time.sleep(1)

    print('Finished configuration.')
    print('')
    time.sleep(1)

    snatch_init()

def snatch_init():
    global screenshotCounter
    # Wait for a brief moment
    print('-- MAKE SURE THE PART OF THE SCREEN YOU WANT TO SNATCH IS VISIBLE -- ')
    cprint('MINIMIZE THIS WINDOW!', "yellow")
    time.sleep(5)
    cprint('Snatchur has started!', "green")
    time.sleep(delayInitial)

    # Perform action for how many screenshots you want to save
    for i in range(numberOfScreenshots):
        # Wait for a brief moment
        time.sleep(delayBeforeScreenshot)

        # Capture the screenshot of the specified region (make sure screnshots region exists)
        if not os.path.exists(screenshotsDirectory):
            os.makedirs(screenshotsDirectory)
        screenshot = pyautogui.screenshot(region=(screenshot_x, screenshot_y, width, height))
        cprint('| Took a screenshot!', 'yellow')
        play_beep()

        # Scroll before clicking (if isScrollEnabled is True)
        if isScrollEnabled:
            time.sleep(0.2)
            print('- Scroll...')
            pyautogui.scroll(-scrollPixels) # Use minus prefix to scroll down
            time.sleep(1.2)

        # Move the mouse to the desired location and click (if isClickEnabled is True)
        if isClickEnabled:
            print('- Click...')
            time.sleep(delayBeforeClick)
            pyautogui.moveTo(click_x, click_y)
            pyautogui.click()

        # If the selected screenshot format is .jpg, convert the screenshot to RGB format (aka .jpg)
        if screenshotFormat == 'jpg':
            screenshot = screenshot.convert('RGB')

        filename = screenshotsDirectory + '--' + str(screenshotCounter) + screenshotFormat
        screenshot.save(screenshotsDirectory + '/' + filename)
        screenshotCounter += 1
    
    if isPdfExportEnabled:
        images_to_pdf()

    # Finish!
    play_finish_audio()
    print('---------------------')
    cprint('Finished snatching!', 'green')
    print('---------------------')
    print('---------------------')
    cprint('Consider donating a tiny amount @ https://www.buymeacoffee.com/lehy', 'yellow')
    time.sleep(2)
    os.system("pause")

# Audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Play beep sound for screenshot
def play_beep():
    if isSoundEnabled:
        play_audio('beep600.ogg')

# Play the finish sound on successful completion
def play_finish_audio():
    play_audio('finish.ogg')

# Convert images to PDF
def images_to_pdf():
    cprint('Generating PDF...', 'yellow')
    image_directory = screenshotsDirectory
    image_files = [os.path.join(image_directory, file) for file in os.listdir(image_directory) if file.endswith((".jpg", ".png", ".jpeg"))]
    pattern = re.compile(r".*--(\d+)")
    sorted_files = sorted(image_files, key=lambda x: int(re.search(pattern, x).group(1)))
    pdf_bytes = img2pdf.convert(sorted_files)
    output_pdf = screenshotsDirectory + ".pdf"

    with open(output_pdf, "wb") as f:
        f.write(pdf_bytes)

# Begin by getting user input
subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
cprint('Snatchur', 'green')
print('---------------------')
time.sleep(0.5)
get_user_input()