import pygame
from pygame.locals import *
import random
import numpy as np

pygame.init()

total_number_of_rows = 11
total_number_of_columns = 9

# list of candy colors
candy_colors = ['blue', 'green', 'purple', 'red', 'yellow']
special_candies = ['rocket', 'bomb', 'magicball']
gimmicks = ['block', 'grass', 'cup']

# candy encodings
candy_encodings = {}
for i, c in enumerate(candy_colors+special_candies+gimmicks):
    candy_encodings[c] = i
candy_decodings = {v: k for k, v in candy_encodings.items()}

print("len(candy_encodings) : ", len(candy_encodings))

# candy size
candy_width = 40
candy_height = 40
candy_size = (candy_width, candy_height)


class Candies:
    def __init__(self, candy_colors=candy_colors, special_candies=special_candies, gimmicks=gimmicks):
        self.candy_images = {color : pygame.transform.smoothscale(\
            pygame.image.load(f'../python-match-three/swirl_{color}.png') \
                , candy_size) for color in candy_colors}
        # self.candy_images = {color : pygame.image.load(f'{color}.png') for color in special_candies}
        # self.candy_images = {color : pygame.image.load(f'{color}.png') for color in gimmicks}

        # self.candy_images = [pygame.transform.smoothscale(candy_image, candy_size) for candy_image in self.candy_images.items()]

    def draw(self, i, row_num, col_num):
        # candy 종류 확인
        candy = candy_decodings[i]
        # candy 이미지 가져오기
        candy_image = self.candy_images[candy]
        # candy 이미지 위치 조정
        rect = candy_image.get_rect()
        rect.left = col_num * candy_width
        rect.top = row_num * candy_height
        # 화면에 그리기
        screen.blit(candy_image, rect)

candies = Candies()


"""
## Candy class define
class Candy:
    
    def __init__(self, row_num, col_num, color='red'):
        
        # set the candy's position on the board
        self.row_num = row_num
        self.col_num = col_num
        
        # assign a random image
        self.color = color
        image_name = f'swirl_{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num * candy_height
        
    # draw the image on the screen
    def draw(self):
        screen.blit(self.image, self.rect)
        
    # 캔디가 그려지는 위치를 보드의 정확한 좌표에 맞춤
    def snap(self):
        self.snap_row()
        self.snap_col()
        
    def snap_row(self):
        self.rect.top = self.row_num * candy_height
        
    def snap_col(self):
        self.rect.left = self.col_num * candy_width

def draw_candy_at(i, row, col):
    candy = Candy(row, col, candy_decodings[i])
    candy.draw()

"""

# create a board (Generate random numbers between 0 and len(candy_colors)-1)
def generate_board(rows, cols):
    board = np.random.randint(0, len(candy_colors), size=(rows, cols))
    return board



score=0
moves=0


def draw():
    
    # draw the background
    pygame.draw.rect(screen, (173, 216, 230), (0, 0, width, height + scoreboard_height))
    
    # draw the candies
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            candies.draw(board[row][col], row, col)
    
    # display the score and moves
    font = pygame.font.SysFont('monoface', 18)
    score_text = font.render(f'Score: {score}', 1, (0, 0, 0))
    score_text_rect = score_text.get_rect(center=(width / 4, height + scoreboard_height / 2))
    screen.blit(score_text, score_text_rect)
    
    moves_text = font.render(f'Moves: {moves}', 1, (0, 0, 0))
    moves_text_rect = moves_text.get_rect(center=(width * 3 / 4, height + scoreboard_height / 2))
    screen.blit(moves_text, moves_text_rect)

### TODO: swap, find matches

# swap the positions of two candies
def swap(candy1, candy2):
    
    temp_row = candy1.row_num
    temp_col = candy1.col_num
    
    candy1.row_num = candy2.row_num
    candy1.col_num = candy2.col_num
    
    candy2.row_num = temp_row
    candy2.col_num = temp_col
    
    # update the candies on the board list
    board[candy1.row_num][candy1.col_num] = candy1
    board[candy2.row_num][candy2.col_num] = candy2
    
    # snap them into their board positions
    candy1.snap()
    candy2.snap()



# create the game window
width = total_number_of_columns * candy_width
height = total_number_of_rows * candy_height
scoreboard_height = 25
window_size = (width, height + scoreboard_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three')

# candy that the user clicked on
clicked_candy = None

# the adjacent candy that will be swapped with the clicked candy
swapped_candy = None

# coordinates of the point where the user clicked on
click_x = None
click_y = None

# game variables
score = 0
moves = 0

board = generate_board(total_number_of_rows, total_number_of_columns)
print(board)
# game loop
clock = pygame.time.Clock()
running = True
while running:
    draw()
    pygame.display.update()
    
    for event in pygame.event.get():
        # 1. detect  quiat
        if event.type == QUIT:
            running = False
            
        # 2. detect mouse click
        if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
            
            # get the candy that was clicked on
            click_x = event.pos[0]
            click_y = event.pos[1]
            row_num = click_y // candy_height
            col_num = click_x // candy_width

            if row_num < total_number_of_rows and col_num < total_number_of_columns:
                clicked_candy = (row_num, col_num)
                print(f'clicked_candy : {clicked_candy}')
    
        """
        # 3. detect mouse motion
        if clicked_candy is not None and event.type == MOUSEMOTION:
            
            # calculate the distance between the point the user clicked on
            # and the current location of the mouse cursor
            distance_x = abs(click_x - event.pos[0])
            distance_y = abs(click_y - event.pos[1])

            
            # reset the position of the swapped candy if direction of mouse motion changed
            if swapped_candy is not None:
                # swapped_candy.snap()
                pass

            # determine the direction of the neighboring candy to swap with
            if distance_x > distance_y and click_x > event.pos[0]:
                direction = 'left'
            elif distance_x > distance_y and click_x < event.pos[0]:
                direction = 'right'
            elif distance_y > distance_x and click_y > event.pos[1]:
                direction = 'up'
            else:
                direction = 'down'
                
                """        