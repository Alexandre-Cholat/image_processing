
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
    
    # Ensure values are within 0-255
    # Convert to unsigned 8-bit integer (uint8)
    imgArray = np.clip(imgArray, 0, 255).astype(np.uint8)
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

# takes an image array and a 2D Numpy array representing the convolution kernel. The
# function should return the filtered image as a Numpy array.
def conv(imgArray, kernel):
    rows, cols, channels = imgArray.shape
    
    # calc padding
    k_w, k_h = kernel.shape
    p_w = k_w // 2
    p_h = k_h // 2
    
    paddded_img = np.pad(imgArray, pad_width = ((p_w, p_w),(p_h, p_h),(0,0)) )

    # build output:
    filtered_img = np.empty([rows, cols, channels])


    for i in range(rows):
        for j in range(cols):
            for color in range(channels):
                # sum weights of kernel * img vals
                sum = 0
                for x in range(k_w):
                    for y in range(k_h):
                        sum = sum + paddded_img[(i + x),(j + y),color] * kernel[x,y] 

                # save weighted sum to output pixel
                filtered_img[i, j, color] = sum



    
    return filtered_img

