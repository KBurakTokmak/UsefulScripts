import cv2
import numpy as np
import pyautogui
import time
from PIL import ImageGrab

# Load the template image
template = cv2.imread('template.png', cv2.IMREAD_GRAYSCALE)

while True:
    # Capture a screenshot of the entire screen
    screenshot = np.array(ImageGrab.grab())

    # Convert the screenshot to grayscale
    grayscale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Use matchTemplate to find the location of the template image in the screenshot
    result = cv2.matchTemplate(grayscale, template, cv2.TM_CCOEFF_NORMED)

    # Get the coordinates of the location with the highest similarity score
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the similarity score is above a certain threshold, click on the location
    if max_val > 0.9:
        # Move the mouse to the location and click on it
        pyautogui.moveTo(max_loc[0]+3, max_loc[1]+3)
        pyautogui.click()

    # Add some delay to avoid excessive CPU usage
    time.sleep(1)
