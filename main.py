import os

import cv2  # opencv-python
import pytesseract
from spellchecker import SpellChecker

import keras_ocr
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

import easyocr
import cv2
import re


input_directory_print = "gitexclude/example_imgs/printed/pre-processed-1"
input_directory_hand = "gitexclude/example_imgs/hand/unprocessed"
img_type = ".png"

# Get valid image paths from dir
img_files_print = []
for file in os.listdir(input_directory_print):
    f_path = os.path.join(input_directory_print, file)

    # Check if file as opposed to a dir
    if os.path.isfile(f_path):
        # Check if file has img_type extension:
        if file.endswith(img_type):
            print(f"Added: {file}")
            img_files_print.append(f_path)

        else:
            print(f"{file} is not of type: {img_type}")
    else:
        print(f"{file} is not a file")

print(img_files_print)

# Load images and process with tesseract:
print(" ")
print("Analysing image text")
print(20*"=")
for f_path in img_files_print:
    # Load img
    img = cv2.imread(f_path)

    # Run tesseract OCR (for printed characters)
    tesseract_config = r''
    tesseract_output = pytesseract.image_to_string(img, config=tesseract_config)
    #print(f"{f_path}: {tesseract_output}")

    # Strip characters from tesseract_output for spellchecker
    #tesseract_output = tesseract_output.strip()

    # Split output sentence into word list
    tesseract_output = tesseract_output.split()
    #print(tesseract_output)

    for word in tesseract_output:

        # Run spellcheck on tesseract output
        spell = SpellChecker()  # Init spellcheck class with default word frequency list
        spell_check_unknown = spell.unknown([word])
        # If tesseract cannot find a word:
        if not tesseract_output:
            print(f"{f_path}: Cannot find a word")
        # If word spelled correctly:
        elif not spell_check_unknown:
            print(f"{f_path}: Word found with a correct spelling: {word}")
        # If word spelled incorrectly:
        else:
            word_correction = spell.correction(word)
            print(f"{f_path}: Word with incorrect spelling: {word} - "
                  f"Suggested Word: {word_correction}")

"""
# Keras auto download pretrained weights for detector and recognizer
pipeline = keras_ocr.pipeline.Pipeline()

# Load the image
image = keras_ocr.tools.read(input_directory_hand)

# Perform OCR
prediction_groups = pipeline.recognize([image])

# Visualize results
keras_ocr.tools.drawAnnotations(image=image, predictions=prediction_groups[0])
"""
# EasyOCR
# Load OCR reader, exclude gpu for now
reader = easyocr.Reader(['en'])  #gpu=False

# Execute OCR on an image
image = ("gitexclude/testing-handwritten/img2.png")
result = reader.readtext(image, allowlist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                         rotation_info=1)
img = cv2.imread(image)

# Iterate over the OCR results
for res in result:
    print(res)
    # Get the bounding box coordinates, convert to integers
    top_left = tuple(map(int, res[0][0]))
    bottom_right = tuple(map(int, res[0][2]))

    # Extract and clean the text
    text = re.sub(r"""[."'}]""", "", res[1])

    # Define font and put a rectangle and text on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 100), 2)
    img = cv2.putText(img, text, bottom_right, font, 1.5, (0, 255, 0), 4, cv2.LINE_AA)

# Display the image
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

