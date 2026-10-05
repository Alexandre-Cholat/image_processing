from tp6.utils import imgArray, img2file, grayscale, convolution, gaussianBlur, edgeDetect
import numpy as np



def main():
        img = imgArray("sample_images/060811_131006_GM6A0103.jpg")

        print(img)
        print("shape : ", np.shape(img))
        print("h : ", np.shape(img)[0])
        print("w : ", np.shape(img)[1])
        print("color channels : ", np.shape(img)[2])
        
        #img = grayscale(img)
        # print("shape : ", np.shape(imgG))

        # img2file(imgG)

        # k = np.full((3,3), 1/9)

        # conv_res = convolution(img, k)
        # img2file(conv_res)

        #img = gaussianBlur(img, size = 9)
        img = edgeDetect(img)
        img2file(img)


        

if __name__ == "__main__":
    main()