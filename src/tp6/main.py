from tp6.utils import imgArray, img2file
import numpy as np



def main():
        img = imgArray("sample_images/small_image.bmp")
        print(img)
        print("shape : ", np.shape(img))
        print("h : ", np.shape(img)[0])
        print("w : ", np.shape(img)[1])
        print("color channels : ", np.shape(img)[2])

        img2file(img)


if __name__ == "__main__":
    main()