import cv2  # opencv-python
import pytesseract
import os

input_directory = "gitexclude/example_imgs"
img_type = ".png"

# Get image paths from dir
img_files = []
for file in os.listdir(input_directory):
    f_path = os.path.join(input_directory, file)

    # Check if file as opposed to a dir
    if os.path.isfile(f_path):
        # Check if file has img_type extension:
        if file.endswith(img_type):
            print(f"Loaded: {file}")
            img_files.append(f_path)

        else:
            print(f"{file} is not of type: {img_type}")
    else:
        print("No files in input directory")

print(img_files)

# Load images and process with tesseract:
for f_path in img_files:
    img = cv2.imread(f_path)
    custom_config = r''
    txt = pytesseract.image_to_string(img, config=custom_config)
    print(f"{f_path}: {txt}")
