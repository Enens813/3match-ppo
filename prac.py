import cv2
import numpy as np
import math

def find_grid_parameters(image_path):
    """
    Attempts to locate the puzzle/grid in a screenshot and deduce:
      - board_x, board_y: top-left corner of the grid in pixels
      - cell_width, cell_height: approximate size of each cell in pixels
      - cols, rows: number of grid columns and rows

    Returns:
      (board_x, board_y, cell_width, cell_height, cols, rows)
    or None if detection fails.
    """

    # 1. Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image at path: {image_path}")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Detect edges (tune thresholds as needed)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

    # 3. Perform Hough line detection
    #    Note: you may need to adjust rho, theta, threshold, etc.
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)
    if lines is None:
        print("No lines detected—tweak your thresholds or method.")
        return None

    # Separate lines into near-horizontal and near-vertical
    # We'll store each line as the 'rho' and 'theta' from Hough
    #   line format: [[rho, theta]]
    horiz_rhos = []
    vert_rhos = []
    for line in lines:
        rho, theta = line[0]
        # Normalize angle to [0..pi)
        # near 0 or near pi => horizontal, near pi/2 => vertical
        # We'll define a tolerance (e.g. 10 degrees)
        deg = np.degrees(theta) % 180

        # near-horizontal if angle is within ~10 deg of 0 or 180
        if deg < 10 or deg > 170:
            horiz_rhos.append(rho)
        # near-vertical if angle is within ~10 deg of 90
        elif 80 < deg < 100:
            vert_rhos.append(rho)
        # else ignore diagonal lines, etc.

    # 4. Cluster lines that are nearly on top of each other
    #    For instance, we might have multiple lines for the same grid edge.
    def cluster_lines(rhos, cluster_dist=10):
        """
        Sort the rhos and merge lines that are within 'cluster_dist' of each other
        into a single representative location (the mean of their positions).
        """
        if not rhos:
            return []
        rhos = sorted(rhos)
        clusters = []
        current_cluster = [rhos[0]]
        for r in rhos[1:]:
            if abs(r - current_cluster[-1]) < cluster_dist:
                # same cluster
                current_cluster.append(r)
            else:
                # finish this cluster, start new
                clusters.append(np.mean(current_cluster))
                current_cluster = [r]
        # last cluster
        clusters.append(np.mean(current_cluster))
        return clusters

    horiz_positions = cluster_lines(horiz_rhos, cluster_dist=10)
    vert_positions  = cluster_lines(vert_rhos,  cluster_dist=10)

    # We expect multiple horizontal lines across the puzzle and multiple vertical lines
    if len(horiz_positions) < 2 or len(vert_positions) < 2:
        print("Not enough grid lines found to infer a grid.")
        return None

    # 5. The puzzle bounding box is roughly the min and max of each set
    min_h = min(horiz_positions)
    max_h = max(horiz_positions)
    min_v = min(vert_positions)
    max_v = max(vert_positions)

    # Because Hough lines in the (rho,theta) format measure the line’s
    # distance from origin, sign depends on quadrant. Let’s assume the puzzle
    # is in the positive quadrant. You may need extra checks/adjustments if
    # your lines have negative rho or your origin is top-left in pixel space.

    # Convert the Hough 'rho' for near-horizontal lines to approximate y-coordinates,
    # and near-vertical lines to approximate x-coordinates.
    # For near-horizontal lines: y ~ rho if theta ~ 0
    # For near-vertical lines:  x ~ rho if theta ~ 90 deg
    # *In reality, Hough’s reference is the image origin in top-left, but you may need
    #  more robust transforms if lines can come from all directions.

    # We'll take the clusters themselves as approximate pixel coordinates.
    # For a more correct approach, you'd solve for intersection points, but let's keep it simple.

    top_y    = min_h
    bottom_y = max_h
    left_x   = min_v
    right_x  = max_v

    # 6. Approximate the number of cells by counting the lines
    #    e.g. if we see 8 vertical lines, that might be 7 columns, etc.
    # But in many puzzle games, #lines = #cells + 1. 
    # We'll do:
    rows = len(horiz_positions) - 1
    cols = len(vert_positions) - 1

    if rows < 1 or cols < 1:
        print("Too few lines or ambiguous grid—cannot determine rows/columns.")
        return None

    # 7. Calculate cell width, height
    # Simple approach: 
    #   (right_x - left_x) / number_of_cols
    #   (bottom_y - top_y) / number_of_rows
    board_x = int(left_x)
    board_y = int(top_y)
    cell_width  = (right_x - left_x) / cols
    cell_height = (bottom_y - top_y) / rows

    # Round or int cast as needed
    cell_width  = int(round(cell_width))
    cell_height = int(round(cell_height))
    board_x     = int(round(board_x))
    board_y     = int(round(board_y))

    return board_x, board_y, cell_width, cell_height, cols, rows


if __name__ == "__main__":
    # Example usage
    image_path = "templates/lv111.png"
    result = find_grid_parameters(image_path)
    if result is not None:
        bx, by, cw, ch, c, r = result
        print("Detected grid parameters:")
        print(f"  board_x = {bx}")
        print(f"  board_y = {by}")
        print(f"  cell_width = {cw}")
        print(f"  cell_height = {ch}")
        print(f"  cols = {c}")
        print(f"  rows = {r}")
    else:
        print("Failed to detect grid parameters.")
