
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
    im.save("output.jpg")

# returns a Numpy array representing the grayscale
# Gray = 0.2989 × R + 0.5870 × G + 0.1140 × B
def grayscale(imgArray):
    rows, cols, channels = imgArray.shape
    grayscale_img = np.empty([rows, cols])

    for r in range(rows):
        for c in range(cols):
            pixel = imgArray[r, c]
            val = 0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2]
            grayscale_img[r,c] = val
            
    return grayscale_img.astype(np.uint8)

