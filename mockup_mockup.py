import numpy as np

# Sample candy colors (represented as integers for simplicity)
candy_colors = ['blue', 'green', 'purple', 'red', 'yellow'] # , 'rocket', 'bomb', 'magicball'

# Define the board dimensions
board_width = 8
board_height = 8

# Generate a random 2D board with numbers (representing candy colors)
def generate_board(rows, cols):
    return np.random.randint(0, len(candy_colors), size=(rows, cols))

# Create the board
board = generate_board(board_height, board_width)

# Function to find matches within a 5x5 region of the board
def find_matches_5x5(sub_board, start_row, start_col):
    matched_coordinates = set()
    print(sub_board)
    """
    # 1. Series of 5 or more identical candies (horizontal or vertical)
    for row in range(5):
        for col in range(1):  # Check horizontally
            if len(set(sub_board[row, col:col+5])) == 1:
                matched_coordinates.update([(start_row + row, start_col + col + i) for i in range(5)])
    
    for col in range(5):
        for row in range(1):  # Check vertically
            if len(set(sub_board[row:row+5, col])) == 1:
                matched_coordinates.update([(start_row + row + i, start_col + col) for i in range(5)])

    # 3. Series of 4 identical candies (either in a row or column)
    for row in range(5):
        for col in range(2):  # Check horizontally for 4 identical candies
            if len(set(sub_board[row, col:col+4])) == 1:
                matched_coordinates.update([(start_row + row, start_col + col + i) for i in range(4)])
                print([(start_row + row, start_col + col + i) for i in range(4)])

    for col in range(5):
        for row in range(2):  # Check vertically for 4 identical candies
            if len(set(sub_board[row:row+4, col])) == 1:
                matched_coordinates.update([(start_row + row + i, start_col + col) for i in range(4)])
                print([(start_row + row + i, start_col + col) for i in range(4)])

    # 4. 2x2 Box of identical candies
    for row in range(4):
        for col in range(4):
            if len(set(sub_board[row:row+2, col:col+2].flatten())) == 1:
                matched_coordinates.update([(start_row + row + i, start_col + col + j) for i in range(2) for j in range(2)])
                print([(start_row + row + i, start_col + col + j) for i in range(2) for j in range(2)])

    
    # 2. Series of 3 identical candies, with two series of 3 candies forming a total of 5 identical series
    for row in range(5):
        for col in range(1, 3):  # Check horizontally for 3 identical candies
            if len(set(sub_board[row, col:col+3])) == 1:
                matched_coordinates.update([(start_row + row, start_col + col + i) for i in range(3)])
                print([(start_row + row, start_col + col + i) for i in range(3)])

    for col in range(5):
        for row in range(1, 3):  # Check vertically for 3 identical candies
            if len(set(sub_board[row:row+3, col])) == 1:
                matched_coordinates.update([(start_row + row + i, start_col + col) for i in range(3)])
                print([(start_row + row + i, start_col + col) for i in range(3)])
    """
    three_matched_coordinates_row = set()
    three_matched_coordinates_col = set()
    # 5. Series of 3 identical candies (either in a row or column)
    for row in range(5):
        for col in range(3):  # Check horizontally for 3 identical candies
            if len(set(sub_board[row, col:col+3])) == 1:
                three_matched_coordinates_row.update([(start_row + row, start_col + col + i) for i in range(3)])
                print([(start_row + row, start_col + col + i) for i in range(3)])

    for col in range(5):
        for row in range(3):  # Check vertically for 3 identical candies
            if len(set(sub_board[row:row+3, col])) == 1:
                three_matched_coordinates_col.update([(start_row + row + i, start_col + col) for i in range(3)])
                print([(start_row + row + i, start_col + col) for i in range(3)])
    
    if len(three_matched_coordinates_row) * len(three_matched_coordinates_row) > 0:
        row_points = []
        col_points = []
        [row_points.extend(x) for x in three_matched_coordinates_row]
        [col_points.extend(x) for x in three_matched_coordinates_col]
        intersection_point = set(row_points) & set(col_points)
        if intersection_point:
            pass
            # row


    # Return the matched coordinates or None if no matches are found
    if matched_coordinates:
        return matched_coordinates
    else:
        return None

# Function to iterate over the whole board and call find_matches_5x5
def find_matches_all_board(board):
    for row in range(board_height - 4):  # Loop through 5x5 regions
        for col in range(board_width - 4):
            sub_board = board[row:row+5, col:col+5]
            matches = find_matches_5x5(sub_board, row, col)
            # matches = 1
            if matches:
                return matches  # Return the first match found
    return None  # Return None if no matches are found

# Example usage
print(board)
matches = find_matches_all_board(board)
if matches:
    print("Matches found at:", matches)
else:
    print("No matches found.")
