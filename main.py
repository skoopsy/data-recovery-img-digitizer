import os

import cv2  # opencv-python
import pytesseract
from spellchecker import SpellChecker

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


