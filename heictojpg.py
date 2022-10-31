# Open the file
import pyheif
from PIL import Image
import piexif
import os
from os import listdir
import sys

# read every file in the directory './data/
# take in argument for directory
if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    directory = './data/dog'

for file in listdir(directory):
    print(file)
    if (file.endswith('.HEIC') or file.endswith('.heic')):
    # read the file
        heif_file = pyheif.read(directory + '/' + file)
        # convert to jpg
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        # save the file
        image.save(directory + '/' + file + '.jpg', 'jpeg', quality=100)
        # remove the original file
        os.remove(directory + '/' + file)
