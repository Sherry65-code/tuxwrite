import pyautogui
import platform
import os

def sus(text):
    pyautogui.typewrite(text)

def shoot():
    # Check the operating system
    system = platform.system()

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Define the desktop directory path based on the operating system
    if system == 'Windows':
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    elif system == 'Linux':
        desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    else:
        raise OSError("Unsupported operating system")

    # Save the screenshot to the desktop
    screenshot.save(os.path.join(desktop_path, 'screenshot.png'))

    print("Screenshot saved to desktop.")
more