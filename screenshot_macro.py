import subprocess
import os
from time import sleep, time
import cv2
from tqdm import tqdm
from get_screenshot import take_screenshot, execute_adb_command, get_screen_info
from actions_and_commands import click_on_bluestacks, start_game, esc_on_bluestacks, give_up, press_on_bluestacks, number_on_bluestacks, move_level

# 21레벨에서 팀에 들어가라고 뜸
# 38레벨에서 슈퍼매직볼? 안아쉽냐고 한번더 giveup 뜸, 패스 첫보상 줌
# Main function
def main():
    # Ensure ADB is connected to BlueStacks
    adb_devices = execute_adb_command(['adb', 'devices'])
    if "List of devices attached" not in adb_devices or len(adb_devices.splitlines()) <= 1:
        print("No devices connected. Make sure BlueStacks is running and ADB is enabled.")
        return
    
    # Take a screenshot and save it
    foldername = 'MPT/levels/'
    for i in tqdm(range(40,1000)):
        click_on_bluestacks(500, 1500) # 홈화면 설정
        sleep(0.5)
        click_on_bluestacks(500, 1500) # 홈화면 설정
        sleep(0.5)
        move_level(i)
        sleep(0.5)

        # 홈화면 사진
        screenshot_filename1 = f'lv{i}_home.png'
        take_screenshot(screenshot_filename1, foldername)
        sleep(1)

        # 게임화면 사진
        start_game()
        sleep(4)
        screenshot_filename2 = f'lv{i}_game.png'
        take_screenshot(screenshot_filename2, foldername)
        sleep(1)

        # 게임 포기
        give_up()
        sleep(1)
        i=i+1
        # break
        


if __name__ == "__main__":
    main()
