import subprocess
import os
from time import sleep
import cv2
from actions_and_commands import execute_adb_command, get_screen_info, take_screenshot

# Main function
def main():
    # Ensure ADB is connected to BlueStacks
    adb_devices = execute_adb_command(['adb', 'devices'])
    if "List of devices attached" not in adb_devices or len(adb_devices.splitlines()) <= 1:
        print("No devices connected. Make sure BlueStacks is running and ADB is enabled.")
        return
    
    # Get screen info (resolution)
    screen_info = get_screen_info()
    print(f"Screen Info: {screen_info}")
    
    # Take a screenshot and save it
    foldername = 'MPT/'
    screenshot_filename = 'success.png'
    print("Taking screenshot...")
    take_screenshot(screenshot_filename, foldername)
    
    print(f"Screenshot saved as {screenshot_filename}")


if __name__ == "__main__":
    main()
