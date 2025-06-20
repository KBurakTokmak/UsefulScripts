"""
Print mouse coordinates when 'J' is pressed.

Dependencies
------------
pip install pyautogui keyboard
"""

import pyautogui
import keyboard

print("Press J to print mouse coordinates.  Ctrl+C to quit.")

keyboard.add_hotkey("j", lambda: print(pyautogui.position()))

keyboard.wait()  # keep script alive until interrupted
