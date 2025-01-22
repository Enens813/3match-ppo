import subprocess
import os
from time import sleep
import cv2

# Function to execute ADB commands and get output
def execute_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

# Function to get the screen information
def get_screen_info():
    # ADB command to get screen dimensions
    result = execute_adb_command(['adb', 'shell', 'wm', 'size'])
    return result

# Function to take a screenshot and save it as a file
def take_screenshot(filename, foldername):
    # ADB command to take a screenshot
    execute_adb_command(['adb', 'shell', 'screencap', '-p', f'/sdcard/{filename}'])
    
    # Pull the screenshot file to your local machine
    execute_adb_command(['adb', 'pull', f'/sdcard/{filename}', f'{foldername}{filename}'])
    
    # Clean up: remove the screenshot from BlueStacks after pulling it
    execute_adb_command(['adb', 'shell', 'rm', f'/sdcard/{filename}'])

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
    screenshot_filename = 'before_gamestart.png'
    print("Taking screenshot...")
    take_screenshot(screenshot_filename, foldername)
    
    print(f"Screenshot saved as {screenshot_filename}")


if __name__ == "__main__":
    main()
