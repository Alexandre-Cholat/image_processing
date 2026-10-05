
import numpy as np
from PIL import Image

# takes as input the path to an image
# file, loads the image using Image module from Pillow and returns a Numpy array.
def imgArray(imgpath):
    with Image.open(imgpath) as im:
        return np.asarray(im)

# takes as input a Numpy array
# representing an image and saves it to a file using the Image module from Pillow.
def img2file(imgArray):
    if not (isinstance(imgArray, np.ndarray)):
        raise TypeError("Only np.ndarray are allowed") 

    # create pillow image
    im = Image.fromarray(imgArray)

    # save
    im.save("output_img")