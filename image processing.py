import cv2
import numpy as np
 
# Reading the image from the present directory

def clahe():
    image = cv2.imread("test2.jpeg",0)
    # Resizing the image for compatibility
    #image = cv2.resize(image, (500, 600))
     
    # The initial processing of the image
    image = cv2.medianBlur(image,3)

     
    # The declaration of CLAHE
    # clipLimit -> Threshold for contrast limiting
    clahe = cv2.createCLAHE(clipLimit=5)
    final_img = clahe.apply(image) + 30
     
    # Ordinary thresholding the same image
    #_, ordinary_img = cv2.threshold(image_bw, 155, 255, cv2.THRESH_BINARY)
     
    # Showing the two images
    #cv2.imshow("ordinary threshold", ordinary_img)
    cv2.imshow("CLAHE image", final_img)

    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    
def highboostfilter(img):
    # Read the image


    # Define the High Boost Filter with central value=4 and A=1.
    HBF = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    # Convolve the image 'a' with HBF.
    img = cv2.filter2D(img, -1, HBF, borderType=cv2.BORDER_CONSTANT)
    

    # Normalize the intensity values.
    img = np.uint8(img)
    
    return img

    # Display the sharpened image.
   

def superhighboost(img):
    # Define the HBF with Central value=8 and A=1.
    SHBF = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    # Convolve the image 'a' with HBF.
    img = cv2.filter2D(img, -1, SHBF, borderType=cv2.BORDER_CONSTANT)

    # Normalize the intensity values.
    img = np.uint8(img)

    # Display the sharpened image.
    return img
    
def bilateral(img):
    img = cv2.bilateralFilter(img, 5, 30, 30) 
    
    return img


def perspective(img):
    pts1 = np.float32([[20, 20], [img.shape[0], 260],
                      [0, 400], [img.shape[0], img.shape[1]]])
    pts2 = np.float32([[0, 0], [img.shape[0], 0],
                      [0, img.shape[1]], [img.shape[0], img.shape[1]]])
    
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix,(img.shape[0],img.shape[1]))
    
    return result
  

img = cv2.imread("test2.jpeg", cv2.IMREAD_GRAYSCALE) 
img=perspective(img)
img2 = cv2.imread("test2.jpeg", cv2.IMREAD_GRAYSCALE)   
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows() 

img=highboostfilter(img)

cv2.imshow("High Boost Filter", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img=bilateral(img)

cv2.imshow("bilateral on highboost",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img2=superhighboost(img2)

cv2.imshow("superHigh Boost Filter", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

img2=bilateral(img2)

cv2.imshow("bilateral on highboost",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("yoyo.jpeg",img2)

    