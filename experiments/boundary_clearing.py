import cv2
import numpy as np


def imreconstruct(marker: np.ndarray, mask: np.ndarray, radius: int = 1):
   kernel = np.ones((3,3),np.uint8)
   while True:
        marker_prev = marker
        dilation = cv2.dilate(marker, kernel, iterations=1)
        marker = np.minimum(dilation, mask)
        if np.array_equal(marker, marker_prev):
            break
   return marker

img=cv2.imread("box_27.jpg",cv2.IMREAD_GRAYSCALE)

img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] 

img=255-img


marker=np.zeros(img.shape)        
for i in range(img.shape[0]):
    marker[i,0]=img[i,0]
    marker[i,img.shape[1]-1]=marker[i,img.shape[1]-1]
    
for i in range(img.shape[1]):
    marker[0,i]=img[0,i]
    marker[img.shape[0]-1,i]=img[img.shape[0]-1,i]
    

cv2.waitKey(0)
        
mask=imreconstruct(marker, img)

img=img-mask

cv2.imshow("after border clearing",img)

cv2.imwrite("sad10.png",img)

cv2.waitKey(0)