import subprocess
import time
import cv2
import random

# Function to execute an ADB command
def execute_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

# Function to perform a swipe on BlueStacks
def swipe_on_bluestacks(start_x, start_y, end_x, end_y, duration=1):
    # ADB command to simulate a swipe gesture
    command = [
        'adb', 'shell', 'input', 'swipe',
        str(start_x), str(start_y),  # Starting point (x, y)
        str(end_x), str(end_y),      # Ending point (x, y)
        str(duration)                # Duration of the swipe in milliseconds
    ]
    
    # Execute the swipe command
    execute_adb_command(command)

def click_on_bluestacks(x, y):
    # ADB command to simulate a tap (click) at (x, y)
    command = [
        'adb', 'shell', 'input', 'tap',
        str(x), str(y)  # X and Y coordinates of the tap
    ]
    
    # Execute the click command
    execute_adb_command(command)


def start_game():
    click_on_bluestacks(450, 1300)
    time.sleep(0.5)
    click_on_bluestacks(400, 1100)


### config
cell_width = 95
cell_height = 95

image_path = "MPT/lv12.png"
image = cv2.imread(image_path)
height, width = image.shape[:2]

possible_x = [(width - cell_width*9)//2 + cell_width//2 + cell_width*i for i in range(9)] 
possible_y = [405 + cell_height//2 + cell_height*i for i in range(9)]

action_space = {}
swipe_right, swipe_left, swipe_up, swipe_down = (+cell_width, 0), (-cell_width, 0), (0, +cell_height), (0, cell_height)
for i in range(9):
    for j in range(9):
        if i == 0 and j == 0:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_down]
        elif i == 0 and j == 8:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_up]
        elif i == 8 and j == 0:
            action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_down]
        elif i == 8 and j == 8:
            action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_up]
        elif i == 0:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_up, swipe_down]
        elif i == 8:
            action_space[(possible_x[i], possible_y[j])] = [swipe_left, swipe_up, swipe_down]
        elif j == 0:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_down]
        elif j == 8:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_up]
        else:
            action_space[(possible_x[i], possible_y[j])] = [swipe_right, swipe_left, swipe_up, swipe_down]



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

        action = random.choice(action_space[(x,y)])
        target_x = x + action[0]
        target_y = y + action[1]

        
        print(x,y,target_x,target_y)
        idx += 1
        swipe_on_bluestacks(x,y,target_x,target_y, 100)
        time.sleep(1)

        if idx == 10:
            break
    print("Game over!")


