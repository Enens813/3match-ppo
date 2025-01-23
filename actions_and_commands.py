import subprocess
import time
import cv2
import random

"""
ADB input관련 참고 : https://hdblog.tistory.com/entry/ADB-InputKey-eventTapSwipeText-Command
"""


### ABD command 실행 
def execute_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


### Bluestacks 화면 관련
def get_screen_info():
    result = execute_adb_command(['adb', 'shell', 'wm', 'size'])
    return result

def take_screenshot(filename, foldername):
    # ADB command to take a screenshot
    execute_adb_command(['adb', 'shell', 'screencap', '-p', f'/sdcard/{filename}'])
    
    # Pull the screenshot file to your local machine
    execute_adb_command(['adb', 'pull', f'/sdcard/{filename}', f'{foldername}{filename}'])
    
    # Clean up: remove the screenshot from BlueStacks after pulling it
    execute_adb_command(['adb', 'shell', 'rm', f'/sdcard/{filename}'])



### Bluestacks 조작 관련

def click_on_bluestacks(x, y):
    command = [
        'adb', 'shell', 'input', 'tap',
        str(x), str(y)  # X and Y coordinates of the tap
    ]
    execute_adb_command(command)

def swipe_on_bluestacks(start_x, start_y, end_x, end_y, duration=1):
    command = [
        'adb', 'shell', 'input', 'swipe',
        str(start_x), str(start_y),  # Starting point (x, y)
        str(end_x), str(end_y),      # Ending point (x, y)
        str(duration)                # Duration of the swipe in milliseconds
    ]
    execute_adb_command(command)

def press_on_bluestacks(x, y, duration=50):
    command = [
        'adb', 'shell', 'input', 'swipe',
        str(x), str(y), str(x), str(y),
        str(duration)  # Duration of the swipe in milliseconds
    ]
    execute_adb_command(command)

def esc_on_bluestacks():
    # esc on bluestacks
    command = [
        'adb', 'shell', 'input', 'keyevent',
        'KEYCODE_ESCAPE'
    ]
    execute_adb_command(command)

def number_on_bluestacks(number):
    number = str(number)
    for digit in number:
        command = [
            'adb', 'shell', 'input', 'keyevent',
            f'KEYCODE_{digit}'
        ]
        execute_adb_command(command)

def move_cursor(direction):
    if direction in ['up', 'down', 'left', 'right']:
        command = [
            'adb', 'shell', 'input', 'keyevent',
            f'KEYCODE_DPAD_{direction.upper()}'
        ]
    else:
        print("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
        return
    execute_adb_command(command)
    
def delete_on_bluestacks():
    command = [
        'adb', 'shell', 'input', 'keyevent',
        'KEYCODE_DEL'
    ]
    execute_adb_command(command)



### 게임 실행 관련
# 게임 시작 (홈 화면에서)
def start_game():
    click_on_bluestacks(450, 1300) # level 써져있는 버튼
    time.sleep(0.5)
    click_on_bluestacks(400, 1100) # start

# 게임 포기 (게임 중)
def give_up():
    esc_on_bluestacks() # esc
    time.sleep(0.5)
    click_on_bluestacks(400, 1000) # 포기
    time.sleep(0.5)
    # 아래 두개는 38레벨부터 추가
    click_on_bluestacks(400, 1000) # 포기
    time.sleep(0.5)
    click_on_bluestacks(815, 170) # 트래블패스 포기
    time.sleep(0.5)
    press_on_bluestacks(810, 520, 1) # x 버튼

def move_level(next_level):
    press_on_bluestacks(830, 75, 10) # 설정
    time.sleep(0.5)
    click_on_bluestacks(600, 245) # othersettings
    time.sleep(0.5)
    click_on_bluestacks(500, 1100) # 빈 화면
    time.sleep(0.5)
    click_on_bluestacks(400, 200) # 레벨 이동(숫자만 입력)
    time.sleep(0.5)
    delete_on_bluestacks()
    time.sleep(0.1)
    delete_on_bluestacks()
    time.sleep(0.1)
    delete_on_bluestacks()
    time.sleep(0.1)
    delete_on_bluestacks()
    time.sleep(0.1)
    number_on_bluestacks(next_level)
    time.sleep(0.5)
    click_on_bluestacks(800, 190) # 이동 버튼
    time.sleep(0.5)
    click_on_bluestacks(835, 50) # 치트설정 x 버튼
    time.sleep(0.5)
    click_on_bluestacks(820, 75) # 설정 x 버튼



### config
cell_width = 95
cell_height = 95

image_path = "MPT/lv12.png"
image = cv2.imread(image_path)
height, width = image.shape[:2]

possible_x = [(width - cell_width*9)//2 + cell_width//2 + cell_width*i for i in range(9)] 
possible_y = [405 + cell_height//2 + cell_height*i for i in range(9)]

basic_action_space = {}
swipe_right, swipe_left, swipe_up, swipe_down = (+cell_width, 0), (-cell_width, 0), (0, +cell_height), (0, cell_height)
for i in range(9):
    for j in range(9):
        if i == 0 and j == 0:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_down]
        elif i == 0 and j == 8:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_up]
        elif i == 8 and j == 0:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_down]
        elif i == 8 and j == 8:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_up]
        elif i == 0:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_up, swipe_down]
        elif i == 8:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_up, swipe_down]
        elif j == 0:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_down]
        elif j == 8:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_up]
        else:
            basic_action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_up, swipe_down]



if __name__ == "__main__":
    # Start the game
    start_game()
    print("Game started!")
    time.sleep(3)
    idx = 0
    while True:
        # randomly select a cell
        x = possible_x[random.randint(0, 8)]
        y = possible_y[random.randint(0, 8)]

        action = random.choice(basic_action_space[(x,y)])
        target_x = x + action[0]
        target_y = y + action[1]

        
        print(x,y,target_x,target_y)
        idx += 1
        swipe_on_bluestacks(x,y,target_x,target_y, 100)
        time.sleep(1)

        if idx == 10:
            break
    print("Game over!")


