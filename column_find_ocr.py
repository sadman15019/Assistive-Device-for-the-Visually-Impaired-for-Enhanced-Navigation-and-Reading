import cv2
import matplotlib.pyplot as plt
import numpy as np

img=cv2.imread("yoyo.jpeg",0)


img=255-img



binr = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] 


  
# define the kernel 
kernel = np.ones((3, 3), np.uint8) 

kernel2 = np.ones((20, 20), np.uint8) 
  
# opening the image 
img = cv2.morphologyEx(binr, cv2.MORPH_CLOSE, kernel, iterations=1) 
img = cv2.dilate(img, kernel2, iterations=1) 


 

img = cv2.Canny(img, 30, 200) 

cv2.imshow('image', img) 
cv2.waitKey(0) 
  
# Finding Contours 
# Use a copy of the image e.g. edged.copy() 
# since findContours alters the image 
contours, hierarchy = cv2.findContours(img,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
  
  
print("Number of Contours found = " + str(len(contours))) 
  
# Draw all contours 
# -1 signifies drawing all contours 
cv2.drawContours(img, contours, -1, (0, 255, 0), 3) 
  
cv2.imshow('Contours', img) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 
