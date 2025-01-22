import cv2
import numpy as np

def identify_piece(cell_img):
    """
    A toy function that identifies the piece in a cell image by
    checking its average color. In a real script, you would likely
    do template matching or more robust feature detection.
    Returns an integer code for the piece type.
    """
    # Compute average BGR color
    avg_color_per_row = np.average(cell_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    b, g, r = avg_color

    # Example thresholds: you will need to tune these
    # for your game's actual icons/colors.
    if r > 150 and g < 100 and b < 100:
        return 1  # e.g. "red G" piece
    elif b > 150 and r < 100 and g < 100:
        return 2  # e.g. "blue drop"
    elif g > 150 and r < 100 and b < 100:
        return 3  # e.g. "green arrow"
    elif r > 150 and g > 150 and b < 50:
        return 4  # e.g. "yellow star"
    else:
        return 0  # unrecognized (or blank)

def extract_grid_positions(img_path):
    """
    Given a 1600x900 screenshot, slice it into rows/columns
    for the puzzle area, identify each cell, and return a 2D list
    of integer codes.
    """
    # Load full screenshot
    full_img = cv2.imread(img_path)
    h, w, _ = full_img.shape
    assert h == 900 and w == 1600, "Screenshot must be 1600x900!"

    # Suppose the puzzle is 9 columns x 9 rows, starting at
    # (board_x, board_y) in the image. Adjust these values to match
    # the actual top-left corner and size of each cell in your game.
    board_x, board_y = 400, 150  # Example offsets
    cell_width, cell_height = 80, 80  # Example cell size
    cols, rows = 9, 9

    grid_codes = []

    for row in range(rows):
        row_codes = []
        for col in range(cols):
            x1 = board_x + col * cell_width
            y1 = board_y + row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # Crop out the cell
            cell_img = full_img[y1:y2, x1:x2]

            # Identify which piece is in this cell
            code = identify_piece(cell_img)
            row_codes.append(code)

        grid_codes.append(row_codes)

    return grid_codes

if __name__ == "__main__":
    image_path = "templates/lv111.png"  # path to your 1600x900 image
    codes = extract_grid_positions(image_path)

    # Print the 2D grid of codes
    for row in codes:
        print(row)
