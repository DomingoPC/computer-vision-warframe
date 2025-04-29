import os # Get Files from "screenshots" Folder
import cv2 # Transform Images
import pytesseract # Image-to-Text
from PIL import Image # Binary Transformation (PIL)

# Tesseract Installation Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path as needed

# Load an image and extract text
def image_to_text(file_name, START_Y, START_X=97, WIDTH=182, HEIGHT=180, GAP_X=35, GAP_Y=22, NUM_ROWS=2, NUM_COLS=8):
    # Image path
    path = os.path.join('screenshots', file_name)

    # Load image
    img = cv2.imread(path)

    # Initialize empty list of names
    names = []

    # Get text of every item
    for idx_row in range(NUM_ROWS):
        for idx_col in range(NUM_COLS):
            # Square sides
            left_side = START_X + idx_col * (WIDTH + GAP_X)
            right_side = left_side + WIDTH
            top_side = START_Y + idx_row * (HEIGHT + GAP_Y)
            bottom_side = top_side + HEIGHT

            # Crop Image
            top_side += int(HEIGHT / 2) # Keep only the text
            cropped = img[top_side:bottom_side, left_side:right_side]
            cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)

            # Convert to grayscale
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

            # Apply thresholding
            _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # Convert the processed image back to a PIL image for pytesseract
            pil_img = Image.fromarray(thresholded)

            # Extract text using pytesseract
            text = pytesseract.image_to_string(pil_img, config=r'--oem 3 --psm 6')
            # pil_img.show()
            # print(text.lower())
            names.append(text.lower())
    return names

# --- First and last images have special cropping parameters ---
# File paths
paths = os.listdir('screenshots')

# First image
name_first = paths[0]

# Last image: find number (python sorts by name)
find_int = len(paths) - 1 # starts in 0
name_last = [name for name in paths if str(find_int) in name][0]

# Intermediate cases
names_middle = [name for name in paths if name not in (name_first, name_last)]

# --- Get names ---
# Initialize names list
names = []

# First Screenshot
names.extend(image_to_text(name_first, START_Y=460))

# Intermediate Screenshots
for file_name in names_middle:
    names.extend(image_to_text(file_name, START_Y=521))
    
# Last Screenshot
names.extend(image_to_text(name_last, START_Y=596))

# Save list
import pickle
with open('output/names.pkl', 'wb') as f:
    pickle.dump(names, f)
