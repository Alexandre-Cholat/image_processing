from tp6.utils import imgArray, img2file, grayscale
import numpy as np



def main():
        img = imgArray("sample_images/bmp_24.bmp")

        print(img)
        print("shape : ", np.shape(img))
        print("h : ", np.shape(img)[0])
        print("w : ", np.shape(img)[1])
        print("color channels : ", np.shape(img)[2])
        
        imgG = grayscale(img)
        print("shape : ", np.shape(imgG))

        img2file(imgG)


        

if __name__ == "__main__":
    main()